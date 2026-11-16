const ALLOWED_ORIGINS = new Set([
  "https://administradorgeral.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

const TRUSTED_EVIDENCE_HOSTS = new Set([
  "www.planalto.gov.br", "planalto.gov.br", "www.gov.br", "www.al.sp.gov.br",
  "www.tjsp.jus.br", "www.ipt.br", "www.cprm.gov.br", "www.daee.sp.gov.br",
  "www.cemaden.gov.br", "www.mpsp.mp.br", "g1.globo.com", "www.saoroque.sp.gov.br",
  "www.camarasaoroque.sp.gov.br", "cidades.ibge.gov.br", "www.habitacao.sp.gov.br",
]);

function plainText(value, maxLength = 700) {
  return (value || "")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, maxLength);
}

function extractEvidence(html, fallbackTitle) {
  const title = plainText(html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1], 180) || fallbackTitle;
  const description = plainText(
    html.match(/<meta[^>]+(?:name|property)=["'](?:description|og:description)["'][^>]+content=["']([^"']+)["']/i)?.[1]
      || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+(?:name|property)=["'](?:description|og:description)["']/i)?.[1],
    700,
  );
  return { title, excerpt: description || plainText(html, 700) };
}

async function verifyEvidence(source) {
  let evidenceUrl;
  try {
    evidenceUrl = new URL(source.url);
  } catch {
    return null;
  }
  if (evidenceUrl.protocol !== "https:" || !TRUSTED_EVIDENCE_HOSTS.has(evidenceUrl.hostname)) return null;

  try {
    const response = await fetch(evidenceUrl.toString(), {
      redirect: "manual",
      headers: { "User-Agent": "SaoRoqueGISHubEvidence/1.0", "Accept": "text/html,application/xhtml+xml" },
    });
    if (!response.ok || response.status >= 300) return null;
    const contentType = response.headers.get("content-type") || "";
    if (!/text\/html|application\/xhtml\+xml/i.test(contentType)) return null;
    const html = await response.text();
    const evidence = extractEvidence(html.slice(0, 750_000), source.title);
    if (!evidence.excerpt) return null;
    return {
      ...source,
      title: evidence.title,
      snippet: evidence.excerpt,
      domain: evidenceUrl.hostname,
      url: evidenceUrl.toString(),
      verifiedAt: new Date().toISOString(),
      retrieval: "Página oficial consultada agora",
    };
  } catch {
    return null;
  }
}

function decodeXml(value) {
  return plainText((value || "").replace(/^<!\[CDATA\[|\]\]>$/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&"));
}

function pillarForHost(host) {
  if (["www.planalto.gov.br", "planalto.gov.br", "www.al.sp.gov.br", "www.tjsp.jus.br"].includes(host)) return ["juridico", "⚖️", "Direito e normas"];
  if (["www.ipt.br", "www.cprm.gov.br", "www.daee.sp.gov.br", "www.cemaden.gov.br"].includes(host)) return ["cientifico", "🔬", "Ciência e território"];
  if (host === "g1.globo.com") return ["noticias", "📰", "Notícia verificada"];
  return ["local", "🏛️", "Fonte institucional"];
}

async function discoverEvidence(query) {
  if (typeof query !== "string" || !query.trim()) return [];
  try {
    const searchUrl = `https://www.bing.com/search?format=rss&q=${encodeURIComponent(`São Roque SP ${query.slice(0, 180)}`)}`;
    const response = await fetch(searchUrl, { headers: { "Accept": "application/rss+xml,application/xml" } });
    if (!response.ok) return [];
    const xml = await response.text();
    const entries = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/gi)].slice(0, 10);
    const results = [];
    for (const [, item] of entries) {
      const link = decodeXml(item.match(/<link>([\s\S]*?)<\/link>/i)?.[1]);
      const title = decodeXml(item.match(/<title>([\s\S]*?)<\/title>/i)?.[1]);
      if (!link || !title) continue;
      let parsed;
      try { parsed = new URL(link); } catch { continue; }
      if (!TRUSTED_EVIDENCE_HOSTS.has(parsed.hostname)) continue;
      const [pillar, pillarIcon, pillarName] = pillarForHost(parsed.hostname);
      results.push({
        id: `live-${parsed.hostname}-${results.length}`,
        pillar,
        pillarName,
        pillarIcon,
        orientation: "EVIDENCIA_ATUAL",
        orientationLabel: "Descoberta na busca atual",
        domain: parsed.hostname,
        title,
        url: parsed.toString(),
        category: "Resultado atual de busca web",
      });
      if (results.length === 4) break;
    }
    return results;
  } catch {
    return [];
  }
}

async function handleEvidence(request, origin) {
  let payload;
  try {
    payload = await request.json();
  } catch {
    return jsonResponse({ error: "Invalid JSON" }, 400, origin);
  }
  const sources = Array.isArray(payload?.sources) ? payload.sources.slice(0, 4) : [];
  const discovered = await discoverEvidence(payload?.query);
  const unique = [...sources, ...discovered].filter((source, index, list) =>
    source?.url && list.findIndex(other => other?.url === source.url) === index,
  );
  const verified = (await Promise.all(unique.map(verifyEvidence))).filter(Boolean).slice(0, 8);
  return jsonResponse({ sources: verified }, 200, origin);
}

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
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: corsHeaders(origin) });
    if (request.method !== "POST") return jsonResponse({ error: "Method not allowed" }, 405, origin);

    if (url.pathname === "/api/evidence") return handleEvidence(request, origin);
    if (url.pathname !== "/api/argon") return jsonResponse({ error: "Not found" }, 404, origin);
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
