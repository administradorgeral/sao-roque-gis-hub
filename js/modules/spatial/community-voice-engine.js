/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE INTELIGÊNCIA COMUNITÁRIA (VOZ DO BAIRRO)
 * ===============================================================================
 * Integra em tempo real:
 *  1. Banco da Câmara Municipal (EPROCLEG): 22.468 proposições reais de vereadores
 *     com data/hora exata do protocolo, autor, macrotema e link auditável.
 *  2. Vinculação Espacial: Identificação da Região Parlamentar (11 Perfis Regionais)
 *     e busca em raio de 1.800m de proposições georreferenciadas.
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
    this.pedidosAudiencias = [];
  }

  async init(dataSource = null) {
    try {
      if (dataSource) {
        this.data = dataSource;
      } else {
        this.data = await this.fetchJson("data/voz_do_bairro_resumo.json");
      }

      if (this.data) {
        this.perfisRegionais = this.data.perfis_regionais || [];
        this.proposicoesGeo = this.data.proposicoes_geolocalizadas || [];
        this.pedidosAudiencias = this.data.pedidos_audiencias_publicas || [];
        this.isLoaded = true;
        console.log("[CommunityVoiceEngine] Base Voz do Bairro carregada:", {
          perfis: this.perfisRegionais.length,
          geolocalizadas: this.proposicoesGeo.length,
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
  buildCommunityVoiceDossier(lat, lng, activeZoneCodes = [], addressText = "") {
    const regionMatch = this.matchRegionalProfile(lat, lng, addressText);
    const primaryRegion = regionMatch?.primaryRegion;
    const regionId = primaryRegion?.id || "geral";

    const nearbyPropositions = this.findPropositionsNearby(lat, lng, 1800, 8);
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
        demandas_audiencias_pd: hearingsSummaryStr
      }
    };
  }
}
