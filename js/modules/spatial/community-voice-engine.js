/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE INTELIGÊNCIA COMUNITÁRIA (VOZ DO BAIRRO)
 * ===============================================================================
 * Integra em tempo real:
 *  1. Banco da Câmara Municipal (EPROCLEG): 22.468 proposições reais de vereadores
 *     com data/hora exata do protocolo, autor, macrotema e link auditável.
 *  2. Vinculação Espacial: Identificação da Região Parlamentar (11 Perfis Regionais),
 *     busca em raio de 1.800m de proposições georreferenciadas e busca textual
 *     (logradouro / referência de bairro) em TODAS as 22.468 ementas do banco,
 *     inclusive nas que não possuem pino GPS.
 *  3. Sugestões dos Moradores no Plano Diretor (Audiências Públicas 2024-2026)
 *     com deliberação e resposta técnica da Prefeitura na Minuta 2026.
 * ===============================================================================
 */

export class CommunityVoiceEngine {
  constructor() {
    this.data = null;
    this.isLoaded = false;
    this.perfisRegionais = [];
    this.proposicoesGeo = [];
    this.proposicoesPorRegiao = {};
    this.streets = null;
    this.streetsTree = new Set();
    this.pedidosAudiencias = [];
  }

  async init(dataSource = null) {
    try {
      if (dataSource) {
        this.data = dataSource;
      } else {
        this.data = await this.fetchJson("data/voz_do_bairro_resumo.json");
      }

      if (this.data && typeof this.data === "object" && (this.data.perfis_regionais || this.data.proposicoes_catalogo)) {
        this.perfisRegionais = this.data.perfis_regionais || [];
        this.proposicoesGeo = this.data.proposicoes_geolocalizadas || [];
        this.pedidosAudiencias = this.data.pedidos_audiencias_publicas || [];
        // Catálogo único (uma linha por proposição) + índices por região e logradouro
        this.catalogo = this.data.proposicoes_catalogo || [];
        this.porId = new Map(this.catalogo.map((p) => [p.id, p]));
        this.idsPorRegiao = this.data.proposicoes_por_regiao || {};
        this.proposicoesPorRegiao = {};
        for (const [regId, ids] of Object.entries(this.idsPorRegiao)) {
          this.proposicoesPorRegiao[regId] = ids.map((id) => this.porId.get(id)).filter(Boolean);
        }
        this.streets = this.buildStreetIndex(this.data.logradouros_indexados || {});
        this.streetsTree = new Set((this.data.logradouros_arvore || []).map((n) => this.normalizeText(n)));
        this.isLoaded = true;
        console.log("[CommunityVoiceEngine] Base Voz do Bairro carregada:", {
          perfis: this.perfisRegionais.length,
          catalogo: this.catalogo.length,
          por_regiao: Object.values(this.proposicoesPorRegiao).reduce((n, l) => n + l.length, 0),
          geolocalizadas: this.proposicoesGeo.length,
          logradouros: this.streets.size,
          pedidos: this.pedidosAudiencias.length
        });
        return true;
      }
      return false;
    } catch (err) {
      console.warn("[CommunityVoiceEngine] Erro ao carregar base de voz comunitária:", err);
      return false;
    }
  }

  async fetchJson(url) {
    if (typeof process !== "undefined" && process.versions && process.versions.node) {
      const fs = await import("fs");
      const cleanPath = url.split("?")[0];
      if (fs.existsSync(cleanPath)) {
        return JSON.parse(fs.readFileSync(cleanPath, "utf8"));
      }
    }
    if (typeof fetch !== "undefined") {
      const resp = await fetch(`${url}?v=${Date.now()}`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status} em ${url}`);
      return await resp.json();
    }
    return null;
  }

  haversineM(lat1, lon1, lat2, lon2) {
    const R = 6371000; // Raio da Terra em metros
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  normalizeText(str) {
    if (!str) return "";
    return str
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      // Apóstrofo/travessão/ponto não separam palavras: "Del'Acqua" === "Delacqua"
      .replace(/['\u2019`]/g, "")
      .replace(/[\s]+/g, " ")
      .trim();
  }

  /**
   * Identifica a Região Parlamentar correspondente ao ponto por distância e palavras-chave
   */
  matchRegionalProfile(lat, lng, addressText = "") {
    if (!this.perfisRegionais.length) return null;
    const addrNorm = this.normalizeText(addressText);

    const scored = [];
    for (const pf of this.perfisRegionais) {
      const cLat = pf.centroide_lat != null ? pf.centroide_lat : -23.5289;
      const cLon = pf.centroide_lon != null ? pf.centroide_lon : -47.1353;
      const distM = this.haversineM(lat, lng, cLat, cLon);
      const raio = pf.raio_m || 2500;

      // Verifica correspondência de palavras-chave no endereço
      let kwHit = false;
      if (addrNorm && pf.palavras_chave) {
        for (const kw of pf.palavras_chave) {
          if (kw && addrNorm.includes(this.normalizeText(kw))) {
            kwHit = true;
            break;
          }
        }
      }

      // Se houver correspondência com o nome do bairro, aplica bônus de proximidade de 1.800m
      const effectiveScore = distM - (kwHit && distM <= raio * 2.5 ? 1800 : 0);
      scored.push({
        profile: pf,
        distanceM: Math.round(distM),
        effectiveScore,
        kwHit
      });
    }

    scored.sort((a, b) => a.effectiveScore - b.effectiveScore);
    const primary = scored[0] || null;
    const secondary = scored.length > 1 && scored[1].distanceM <= 3200 ? scored[1] : null;

    return {
      primaryRegion: primary ? primary.profile : null,
      distanceToCenterM: primary ? primary.distanceM : 0,
      keywordMatch: primary ? primary.kwHit : false,
      secondaryRegion: secondary ? secondary.profile : null
    };
  }

  /**
   * Busca proposições georreferenciadas no entorno imediato (raio default 1.800m)
   */
  /**
   * Extrai o nome da via do texto livre do ponto (ex.: "Rua Bandeirantes, 120, Centro").
   * Usa o índice de logradouros como dicionário: casa pelo maior prefixo conhecido.
   */
  extractStreetName(text) {
    // Nomes de logradouro são nomes próprios: não são normalizados aqui, senão
    // "Rua Enricco Delacqua" viraria "rua enricco delacqua" e nunca casaria no índice.
    const normalized = String(text || "").trim();
    if (!normalized || !this.streets) return "";

    const STOP = new Set(["rua", "r", "av", "avenida", "travessa", "tv", "alameda", "estrada", "estr", "rodovia", "rod", "praca", "largo", "viela", "beco"]);
    const words = normalized
      .split(/[^A-Za-zÀ-ÿ0-9]+/)
      .filter((w) => w.length >= 2 && !STOP.has(this.normalizeText(w)));
    if (!words.length) return "";

    // 1. Prefixo mais longo a partir do início: "rua enricco delacqua" -> "enricco delacqua"
    for (let len = Math.min(5, words.length); len >= 1; len--) {
      const candidato = this.normalizeText(words.slice(0, len).join(" "));
      if (candidato.length >= 4 && (this.streets.has(candidato) || this.streetsTree.has(candidato))) return candidato;
    }

    // 2. N-gramas em qualquer posição: "bairro centro rua pedro vaz" -> "pedro vaz"
    for (let len = Math.min(5, words.length); len >= 1; len--) {
      for (let start = 0; start + len <= words.length; start++) {
        const candidate = words.slice(start, start + len).join(" ");
        const key = this.normalizeText(candidate);
        if (key.length < 4) continue;
        if (this.streets.has(key)) return key;
        // Taxa de ruas com apenas 1 protocolo (só existem na árvore)
        if (this.streetsTree.has(key)) return key;
      }
    }

    // Fallback: maior prefixo de logradouro conhecido (ex.: "pedro vaz com" -> "pedro vaz")
    for (let len = Math.min(5, words.length); len >= 2; len--) {
      const candidate = this.normalizeText(words.slice(0, len).join(" "));
      if (candidate.length < 4) continue;
      for (const chave of this.streets.keys()) {
        if (chave.endsWith(candidate) && chave.length - candidate.length <= 12) return chave;
      }
    }
    return "";
  }

  /** Compara duas palavras por similaridade (até 2 letras de diferença total). */
  similarWord(a, b, limite = 2) {
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > limite) return false;
    let i = 0, j = 0, diff = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++diff > limite) return false;
      if (a.length > b.length) i++;
      else if (b.length > a.length) j++;
      else { i++; j++; }
    }
    return diff + (a.length - i) + (b.length - j) <= limite;
  }

  /**
   * Resolve a chave de logradouro tolerando grafia divergente (Enrico/Enricco).
   * Devolve { key, nome } — a chave é a do dicionário usado nas ementas.
   */
  findClosestStreetKey(key, original = "") {
    let alvo = key.split(/[^a-z0-9]+/).filter((w) => w.length >= 3);
    if (!alvo.length) return null;

    // Grafia colada/separada: "delacqua" x "del acqua" -> compara sem espaços.
    const alvoColado = alvo.join("");

    // Rótulo bonito: usa a grafia do mapa (grafo) ou o texto original do usuário.
    const bonito = (String(original || "")
      .replace(/^(rua|r\.?|avenida|av\.?|travessa|tv\.?|alameda|estrada|estr\.?|rodovia|rod\.?|pra[çc]a|largo|viela|beco)\s+/i, "")
      .replace(/['"\u2019`]/g, "")
      .trim()) || key;

    for (const [k, st] of this.streets) {
      const partes = k.split(/[^a-z0-9]+/).filter((w) => w.length >= 1);
      const colado = partes.join("");
      if (partes.length === alvo.length && partes.every((w, i) => this.similarWord(w, alvo[i]))) {
        return { key: k, nome: st.nome, rotulo: st.nome };
      }
      if (this.similarWord(colado, alvoColado, 3) && this.similarWord(partes[0], alvo[0])) {
        return { key: k, nome: st.nome, rotulo: st.nome };
      }
    }
    // A árvore só é consultada como último recurso: milhares de nomes, muitos
    // genéricos ("Manoel", "Sao Jose"), então exigimos palavra inicial igual.
    for (const nome of this.streetsTree || []) {
      const partes = nome.split(/[^a-z0-9]+/).filter((w) => w.length >= 1);
      const colado = partes.join("");
      if (!partes.length || !this.similarWord(partes[0], alvo[0])) continue;
      if (partes.length === alvo.length && partes.every((w, i) => this.similarWord(w, alvo[i]))) {
        return { key: nome, nome, rotulo: nome };
      }
      if (this.similarWord(colado, alvoColado, 3) && this.similarWord(partes[0], alvo[0])) {
        return { key: nome, nome, rotulo: nome };
      }
    }
    return null;
  }

  buildStreetIndex(streets) {
    const index = new Map();
    const entries = Array.isArray(streets) ? streets : Object.entries(streets || {}).map(([id, st]) => ({ id, ...st }));
    for (const st of entries) {
      const key = this.normalizeText(st && st.nome);
      if (key) index.set(key, st);
    }
    return index;
  }

  findPropositionsNearby(lat, lng, radiusM = 1800, limit = 8) {
    if (!this.proposicoesGeo.length) return [];

    const scored = [];
    for (const p of this.proposicoesGeo) {
      if (p.lat == null || p.lng == null) continue;
      const distM = this.haversineM(lat, lng, p.lat, p.lng);
      if (distM <= radiusM) {
        scored.push({
          ...p,
          distancia_m: Math.round(distM)
        });
      }
    }

    scored.sort((a, b) => a.distancia_m - b.distancia_m);
    return scored.slice(0, limit);
  }

  /**
   * Proposições da região parlamentar — inclui as SEM pino GPS.
   * A vinculação usa contrato territorial (região identificada pelo ponto,
   * zona vigente/proposta e logradouro citado na ementa), não apenas coordenadas.
   */
  getRegionPropositions(regionId, activeZoneCodes = [], limit = 6) {
    const pool = this.proposicoesPorRegiao[regionId] || [];
    if (!pool.length) return [];

    const zonas = activeZoneCodes.map((z) => this.normalizeText(z)).filter(Boolean);
    const scored = pool.map((p) => {
      let score = 0;
      if (p.ano >= 2024) score += 3;
      if (zonas.length) {
        const desc = this.normalizeText(`${p.descricao_resumida || ""} ${p.descricao_completa || ""}`);
        if (zonas.some((z) => desc.includes(z))) score += 4;
      }
      return { ...p, _score: score };
    });

    scored.sort(
      (a, b) => b._score - a._score || String(b.data_formatada || b.ano).localeCompare(String(a.data_formatada || a.ano)),
    );
    return scored.slice(0, limit);
  }

  /**
   * Encontra o logradouro citado no texto (rua/avenida/estrada...) e devolve os
   * protocolos daquela mesma rua em todo o histórico — casando inclusive
   * proposições sem coordenada GPS.
   */
  findPropositionsByStreetAddress(lat, lng, addressText = "", nearbyStreetName = "", limit = 6) {
    // O nome pode vir com o tipo da via ("Rua Enrico Delacqua"); o índice guarda
    // apenas o nome, então tentamos a forma completa e a sem tipo.
    const bruto = String(nearbyStreetName || "").replace(/['"\u2019`\.]/g, " ").trim();
    const semTipo = bruto.replace(/^(rua|r\.?|avenida|av\.?|travessa|tv\.?|alameda|estrada|estr\.?|rodovia|rod\.?|pra[çc]a|largo|viela|beco)\s+/i, "");
    let key = this.normalizeText(semTipo) || this.extractStreetName(addressText);
    if (!key || key.length < 4) return { logradouro: null, proposicoes: [] };

    // Grafia divergente entre o grafo de logradouros e a ementa
    // (ex.: "Enrico Delacqua" no mapa vs "Enricco Delacqua" na Câmara).
    // Rótulo exibido: grafia do grafo de logradouros (nome próprio), quando existir.
    let rotulo = (/[A-ZÀ-Þ]/.test(bruto) ? semTipo : key) || key;
    if (!this.streets?.has(key) && !this.streetsTree?.has(key)) {
      const tolerante = this.findClosestStreetKey(key, bruto);
      if (tolerante) {
        key = tolerante.key;
        rotulo = tolerante.rotulo;
      }
    }

    const st = this.streets?.get(key) || null;
    if (st?.nome) rotulo = st.nome;
    const regioesDoLogradouro = new Set(st?.regioes || []);
    const hits = [];
    for (const p of this.catalogo) {
      if (p.gps) continue; // os com GPS já entram pela busca de raio
      const desc = this.normalizeText(`${p.titulo || ""} ${p.descricao_resumida || ""} ${p.descricao_completa || ""}`);
      if (!desc.includes(key)) continue;
      hits.push({
        ...p,
        match_logradouro: rotulo,
        distancia_m: null,
        regiao_id: p.regiao_id || [...regioesDoLogradouro][0] || null
      });
    }

    hits.sort((a, b) => String(b.data_formatada || b.ano).localeCompare(String(a.data_formatada || a.ano)));
    return { logradouro: st || { nome: rotulo, regioes: [...regioesDoLogradouro] }, proposicoes: hits.slice(0, limit), total: hits.length };
  }

  /**
   * Busca sugestões dos cidadãos nas Audiências Públicas do Plano Diretor para a região ou zona
   */
  getCitizenHearingRequests(regionId, activeZoneCodes = []) {
    if (!this.pedidosAudiencias.length) return [];

    const normalizedZones = activeZoneCodes.map((z) => this.normalizeText(z));
    const requestsRegion = [];
    const requestsZone = [];

    for (const ped of this.pedidosAudiencias) {
      if (ped.regiao_id === regionId) {
        requestsRegion.push(ped);
      } else if (ped.zonas_relacionadas && normalizedZones.length) {
        const pz = ped.zonas_relacionadas.map((z) => this.normalizeText(z));
        if (pz.some((z) => normalizedZones.some((nz) => nz.includes(z) || z.includes(nz)))) {
          requestsZone.push(ped);
        }
      }
    }

    return {
      pedidos_diretos_regiao: requestsRegion,
      pedidos_zonas_semelhantes: requestsZone.slice(0, 3)
    };
  }

  /**
   * Constrói o dossiê consolidado da 'Seção 5 — Voz do Bairro' para o ponto
   */
  /**
   * Quando o ponto traz texto de bairro/logradouro, resume TODOS os protocolos do
   * banco que citam esse logradouro (com e sem GPS), inclusive por termo do bairro.
   */
  describeNeighborhoodByText(addressText = "") {
    const norm = this.normalizeText(addressText);
    if (!norm || !this.catalogo.length) return null;

    const stop = new Set(["rua", "avenida", "av", "travessa", "alameda", "estrada", "rodovia", "praca", "largo", "bairro", "b", "jardim", "jd", "vila", "distrito", "de", "da", "do", "dos", "das", "zcu", "zur", "zue", "zupa", "zdb", "zdm", "zr", "zona"]);
    const termos = norm.split(/[^a-z0-9]+/).filter((t) => t.length >= 4 && !stop.has(t));
    if (!termos.length) return null;

    const porTema = {};
    let total = 0;
    const amostra = [];
    for (const p of this.catalogo) {
      const desc = this.normalizeText(`${p.titulo || ""} ${p.descricao_resumida || ""} ${p.descricao_completa || ""}`);
      if (!termos.some((t) => desc.includes(t))) continue;
      total += 1;
      porTema[p.tema_id] = (porTema[p.tema_id] || 0) + 1;
      if (amostra.length < 4) amostra.push(p);
    }
    if (!total) return null;

    const ranking = Object.entries(porTema)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4)
      .map(([temaId, qtd]) => ({ tema_id: temaId, quantidade: qtd, percentual: Math.round((qtd / total) * 1000) / 10 }));

    return { termos, total_protocolos: total, ranking_temas: ranking, amostra };
  }

  buildCommunityVoiceDossier(lat, lng, activeZoneCodes = [], addressText = "", addressStreetName = "") {
    const regionMatch = this.matchRegionalProfile(lat, lng, addressText);
    const primaryRegion = regionMatch?.primaryRegion;
    const regionId = primaryRegion?.id || "geral";

    const nearbyPropositions = this.findPropositionsNearby(lat, lng, 1800, 8);
    // O nome do logradouro do ponto vem como nome próprio, por isso é passado
    // separado do texto livre (distrito/zona/bairro).
    const addressMatches = this.findPropositionsByStreetAddress(lat, lng, addressText, addressStreetName);
    const resumoBairro = this.describeNeighborhoodByText(addressText);
    const regionPropositions = this.getRegionPropositions(regionId, activeZoneCodes, 6);
    const hearingRequests = this.getCitizenHearingRequests(regionId, activeZoneCodes);

    const stats = primaryRegion?.estatisticas || {
      total_proposicoes: 0,
      indicacoes: 0,
      requerimentos: 0,
      projetos_de_lei: 0,
      temas_ranking: []
    };

    // Resumo de alta densidade semântica para injeção no prompt de IA (Gemini 4 Argon)
    const topTemasStr = (stats.temas_ranking || [])
      .slice(0, 4)
      .map((t) => `${t.tema_nome}: ${t.quantidade} (${t.percentual}%)`)
      .join(" | ");

    const nearbySummaryStr = nearbyPropositions
      .slice(0, 3)
      .map(
        (p) =>
          `[${p.distancia_m}m] ${p.titulo} (${p.data_formatada || p.ano} - ${p.autor}): ${p.descricao_resumida}`
      )
      .join("\n");

    const regionSummaryStr = regionPropositions
      .slice(0, 4)
      .map((p) => `${p.titulo} (${p.data_formatada || p.ano} - ${p.autor}): ${p.descricao_resumida}`)
      .join("\n");

    const addressSummaryStr = addressMatches.proposicoes
      .slice(0, 3)
      .map((p) => `${p.titulo} (${p.data_formatada || p.ano}): ${p.descricao_resumida}`)
      .join("\n");

    const hearingsSummaryStr = (hearingRequests.pedidos_diretos_regiao || [])
      .slice(0, 2)
      .map(
        (h) =>
          `[${h.status_prefeitura}] ${h.local_alvo}: ${h.pedido_dos_moradores.slice(0, 140)}... -> Resposta: ${h.resposta_oficial_minuta_2026.slice(0, 140)}...`
      )
      .join("\n");

    return {
      regiao_identificada: primaryRegion,
      distancia_centroide_m: regionMatch?.distanceToCenterM || 0,
      match_por_endereco: regionMatch?.keywordMatch || false,
      estatisticas_regiao: stats,
      ranking_temas: stats.temas_ranking || [],
      proposicoes_proximas_gps: nearbyPropositions,
      proposicoes_regiao: regionPropositions,
      logradouro_citado: addressMatches.logradouro,
      resumo_por_texto: resumoBairro,
      proposicoes_mesmo_logradouro: addressMatches.proposicoes,
      pedidos_moradores_audiencias: hearingRequests.pedidos_diretos_regiao,
      pedidos_em_zonas_semelhantes: hearingRequests.pedidos_zonas_semelhantes,
      resumo_ia_shorthand: {
        nome_regiao: primaryRegion?.nome_regiao || "São Roque",
        total_protocolos: stats.total_proposicoes,
        indicacoes: stats.indicacoes,
        requerimentos: stats.requerimentos,
        pls: stats.projetos_de_lei,
        top_temas: topTemasStr,
        protocolos_no_raio_gps: nearbySummaryStr,
        protocolos_regiao: regionSummaryStr,
        protocolos_mesmo_logradouro: addressSummaryStr,
        demandas_audiencias_pd: hearingsSummaryStr
      }
    };
  }
}
