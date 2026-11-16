const ALLOWED_ORIGINS = new Set([
  "https://administradorgeral.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Vary": "Origin",
  };
}

function jsonResponse(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders(origin) },
  });
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    if (!ALLOWED_ORIGINS.has(origin)) return new Response("Origin not allowed", { status: 403 });

    const url = new URL(request.url);
    if (url.pathname !== "/api/argon") return jsonResponse({ error: "Not found" }, 404, origin);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders(origin) });
    if (request.method !== "POST") return jsonResponse({ error: "Method not allowed" }, 405, origin);
    if (!env.GEMINI_API_KEY) return jsonResponse({ error: "Gemini is not configured" }, 503, origin);

    const length = Number(request.headers.get("Content-Length") || 0);
    if (length > 1_000_000) return jsonResponse({ error: "Request too large" }, 413, origin);

    let payload;
    try {
      payload = await request.json();
    } catch {
      return jsonResponse({ error: "Invalid JSON" }, 400, origin);
    }
    if (!payload || !Array.isArray(payload.contents) || payload.contents.length === 0) {
      return jsonResponse({ error: "Invalid Gemini request" }, 400, origin);
    }

    const upstream = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent?key=${encodeURIComponent(env.GEMINI_API_KEY)}`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) },
    );
    return new Response(upstream.body, {
      status: upstream.status,
      headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders(origin) },
    });
  },
};
