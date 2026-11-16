const MODEL = "gemini-4-argon";
const MAX_BODY_BYTES = 256_000;
const MAX_CONTENTS = 40;
const MAX_TEXT_CHARS = 220_000;

function jsonResponse(data, status, origin) {
  const headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store"
  };
  if (origin) {
    headers["Access-Control-Allow-Origin"] = origin;
    headers["Access-Control-Allow-Methods"] = "POST, OPTIONS";
    headers["Access-Control-Allow-Headers"] = "Content-Type";
    headers["Vary"] = "Origin";
  }
  return new Response(JSON.stringify(data), { status, headers });
}

function isValidContents(contents) {
  if (!Array.isArray(contents) || contents.length === 0 || contents.length > MAX_CONTENTS) {
    return false;
  }

  let totalChars = 0;
  for (const item of contents) {
    if (!item || !["user", "model"].includes(item.role) || !Array.isArray(item.parts)) {
      return false;
    }
    for (const part of item.parts) {
      if (typeof part?.text !== "string") return false;
      totalChars += part.text.length;
      if (totalChars > MAX_TEXT_CHARS) return false;
    }
  }
  return true;
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin");
    const allowedOrigin = env.ALLOWED_ORIGIN;

    if (!allowedOrigin || origin !== allowedOrigin) {
      return jsonResponse({ error: "Origem não autorizada." }, 403);
    }

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": allowedOrigin,
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
          "Access-Control-Max-Age": "86400",
          "Vary": "Origin"
        }
      });
    }

    const url = new URL(request.url);
    if (url.pathname !== "/api/argon") {
      return jsonResponse({ error: "Rota não encontrada." }, 404, allowedOrigin);
    }
    if (request.method !== "POST") {
      return jsonResponse({ error: "Método não permitido." }, 405, allowedOrigin);
    }
    if (!env.GEMINI_API_KEY) {
      return jsonResponse({ error: "A chave do Gemini não está configurada no Worker." }, 503, allowedOrigin);
    }

    const contentLength = Number(request.headers.get("Content-Length") || 0);
    if (contentLength > MAX_BODY_BYTES) {
      return jsonResponse({ error: "A consulta excede o tamanho permitido." }, 413, allowedOrigin);
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return jsonResponse({ error: "O corpo da consulta não contém JSON válido." }, 400, allowedOrigin);
    }

    if (!isValidContents(payload?.contents)) {
      return jsonResponse({ error: "O conteúdo da consulta Gemini é inválido." }, 400, allowedOrigin);
    }

    if (JSON.stringify(payload.contents).length > MAX_BODY_BYTES) {
      return jsonResponse({ error: "A consulta excede o tamanho permitido." }, 413, allowedOrigin);
    }

    const clientIp = request.headers.get("CF-Connecting-IP") || "unknown";
    const { success } = await env.AI_RATE_LIMITER.limit({ key: clientIp });
    if (!success) {
      return jsonResponse({ error: "Limite de consultas atingido. Aguarde um minuto e tente novamente." }, 429, allowedOrigin);
    }

    const generationConfig = payload.generationConfig || {};
    const temperature = Number(generationConfig.temperature);
    const maxOutputTokens = Number(generationConfig.maxOutputTokens);
    const body = {
      contents: payload.contents,
      generationConfig: {
        temperature: Number.isFinite(temperature) ? Math.min(Math.max(temperature, 0), 1) : 0.45,
        maxOutputTokens: Number.isFinite(maxOutputTokens)
          ? Math.min(Math.max(Math.floor(maxOutputTokens), 1), 3500)
          : 3500
      }
    };

    let upstream;
    try {
      upstream = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${encodeURIComponent(env.GEMINI_API_KEY)}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
          signal: AbortSignal.timeout(70_000)
        }
      );
    } catch {
      return jsonResponse({ error: "Não foi possível conectar à API Gemini." }, 502, allowedOrigin);
    }

    let responseBody;
    try {
      responseBody = await upstream.json();
    } catch {
      return jsonResponse({ error: "A API Gemini retornou uma resposta inválida." }, 502, allowedOrigin);
    }

    if (!upstream.ok) {
      const message = responseBody?.error?.message || `A API Gemini respondeu com HTTP ${upstream.status}.`;
      return jsonResponse({ error: message }, 502, allowedOrigin);
    }

    return jsonResponse(responseBody, 200, allowedOrigin);
  }
};
