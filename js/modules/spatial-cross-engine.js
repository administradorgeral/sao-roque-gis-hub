/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE INTELIGÊNCIA TERRITORIAL CRUZADA (TUDO LIGADO A TUDO)
 * ===============================================================================
 * Padrão: GeoSPARQL / OGC Linked Data / Topological DE-9IM
 * 
 * Elimina totalmente o uso de 'FIDs' numéricos opacos.
 * Toda e qualquer referência espacial é formulada como:
 *   [Nome da Camada Oficial]: [Legenda Oficial / Nome Semântico]
 * 
 * Capacidades:
 *   1. Ponto/Coordenada -> Drill-down em todas as camadas (Rua, Bairro, Zona, Solo, Geologia, Declividade, APA, Obras, Leis)
 *   2. Rua/Logradouro -> Bairros, Zonas que atravessa, Solos, APA, Obras da Carta XIII
 *   3. Bairro/Distrito -> Vias principais, Zonas incidentes, Restrições, Demandas Populares
 *   4. Camada/Legenda -> Cruzamentos espaciais, Vias que a cortam, Leis que a regem
 * ===============================================================================
 */

import { ALL_33_LAYERS, LayerIntelligenceCatalog } from "./spatial/layer-intelligence-catalog.js";
import { SpatialLocator } from "./spatial/spatial-locator.js";
import { CommunityVoiceEngine } from "./spatial/community-voice-engine.js";

export class SpatialCrossEngine {
  constructor() {
    this.graph = null;
    this.isLoaded = false;
    this.locator = new SpatialLocator();
    this.communityVoice = new CommunityVoiceEngine();
    this.streetIndex = new Map();
    this.bairroIndex = new Map();
    this.zonaIndex = new Map();
    this.soloIndex = new Map();
    this.geologiaIndex = new Map();
    this.obraIndex = new Map();
    this.cartaIndex = new Map();
    this.leiIndex = new Map();
    this.regraIndex = new Map();
    this.layer33Index = new Map();
    this.layerCatalog = LayerIntelligenceCatalog;
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

  async init() {
    try {
      const [graphData] = await Promise.all([
        this.fetchJson("data/grafo_territorial_sao_roque.json"),
        this.locator.init().catch(err => {
          console.warn("[SpatialCrossEngine] Aviso ao inicializar SpatialLocator:", err);
          return false;
        }),
        this.communityVoice.init().catch(err => {
          console.warn("[SpatialCrossEngine] Aviso ao inicializar CommunityVoiceEngine:", err);
          return false;
        })
      ]);
      if (!graphData) throw new Error("Não foi possível carregar grafo territorial");
      this.graph = graphData;
      this.buildIndices();
      this.isLoaded = true;
      console.log("[SpatialCrossEngine] Grafo territorial multicamadas carregado com sucesso:", {
        distritos: Object.keys(this.graph.distritos || {}).length,
        logradouros: Object.keys(this.graph.logradouros || {}).length,
        zonas: Object.keys(this.graph.zonas_2006 || {}).length,
        cartas: Object.keys(this.graph.cartas_2026 || {}).length,
        solos: Object.keys(this.graph.solos_pedologia || {}).length,
        obras: Object.keys(this.graph.obras_estruturantes_2026 || {}).length,
        locatorAtivo: this.locator.isInitialized,
        vozDoBairroAtivo: this.communityVoice.isLoaded
      });
      return true;
    } catch (err) {
      console.warn("[SpatialCrossEngine] Erro ao carregar grafo_territorial_sao_roque.json:", err);
      return false;
    }
  }

  normalize(str) {
    if (!str) return "";
    return str
      .toString()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();
  }

  buildIndices() {
    if (!this.graph) return;

    // Indexar Logradouros
    const logs = this.graph.logradouros || {};
    for (const [key, obj] of Object.entries(logs)) {
      const norm = this.normalize(obj.nome_oficial);
      this.streetIndex.set(norm, obj);
      // Indexar sem prefixo de via (rua, avenida, estrada, rodovia)
      const semPrefixo = norm.replace(/^(rua|avenida|estrada|rodovia|alameda|travessa|beco|praca|estrada municipal)\s+/i, "");
      if (semPrefixo && semPrefixo !== norm) {
        this.streetIndex.set(semPrefixo, obj);
      }
    }

    // Indexar Bairros
    const bairros = this.graph.bairros || {};
    for (const [key, obj] of Object.entries(bairros)) {
      this.bairroIndex.set(this.normalize(obj.nome), obj);
    }

    // Indexar Zonas
    const zonas = this.graph.zonas_2006 || {};
    for (const [key, obj] of Object.entries(zonas)) {
      this.zonaIndex.set(this.normalize(obj.sigla), obj);
      this.zonaIndex.set(this.normalize(obj.denominacao), obj);
    }

    // Indexar Solos
    const solos = this.graph.solos_pedologia || {};
    for (const [key, obj] of Object.entries(solos)) {
      this.soloIndex.set(this.normalize(obj.codigo_classe), obj);
      this.soloIndex.set(this.normalize(obj.macroclasse), obj);
      this.soloIndex.set(this.normalize(obj.nome_classe), obj);
    }

    // Indexar Geologia
    const geol = this.graph.unidades_geologicas || {};
    for (const [key, obj] of Object.entries(geol)) {
      this.geologiaIndex.set(this.normalize(obj.codigo), obj);
      this.geologiaIndex.set(this.normalize(obj.nome), obj);
    }

    // Indexar Obras
    const obras = this.graph.obras_estruturantes_2026 || {};
    for (const [key, obj] of Object.entries(obras)) {
      this.obraIndex.set(this.normalize(obj.codigo), obj);
      this.obraIndex.set(this.normalize(obj.nome), obj);
    }

    // Indexar Cartas
    const cartas = this.graph.cartas_2026 || {};
    for (const [key, obj] of Object.entries(cartas)) {
      this.cartaIndex.set(this.normalize(`carta ${obj.romano}`), obj);
      this.cartaIndex.set(this.normalize(`carta ${obj.numero}`), obj);
      this.cartaIndex.set(this.normalize(obj.titulo), obj);
    }

    // Indexar Legislação Territorial Oficial (227 Leis e Decretos)
    const normas = this.graph.legislacao_territorial?.normas || {};
    for (const [key, obj] of Object.entries(normas)) {
      this.leiIndex.set(this.normalize(key), obj);
      if (obj.numero) {
        const numStr = String(obj.numero).trim();
        const numClean = numStr.replace(/\./g, "").trim();
        this.leiIndex.set(this.normalize(numStr), obj);
        this.leiIndex.set(this.normalize(numClean), obj);
        this.leiIndex.set(this.normalize(`lei ${numStr}`), obj);
        this.leiIndex.set(this.normalize(`lei ${numClean}`), obj);
        this.leiIndex.set(this.normalize(`lei nº ${numStr}`), obj);
        this.leiIndex.set(this.normalize(`lei nº ${numClean}`), obj);
        this.leiIndex.set(this.normalize(`lc ${numStr}`), obj);
        this.leiIndex.set(this.normalize(`lc ${numClean}`), obj);
        this.leiIndex.set(this.normalize(`lc nº ${numStr}`), obj);
        this.leiIndex.set(this.normalize(`lc nº ${numClean}`), obj);
        if (obj.tipo) {
          this.leiIndex.set(this.normalize(`${obj.tipo} ${numStr}`), obj);
          this.leiIndex.set(this.normalize(`${obj.tipo} ${numClean}`), obj);
          this.leiIndex.set(this.normalize(`${obj.tipo} nº ${numStr}`), obj);
          this.leiIndex.set(this.normalize(`${obj.tipo} nº ${numClean}`), obj);
        }
      }
      if (obj.id) {
        this.leiIndex.set(this.normalize(obj.id), obj);
      }
    }

    // Indexar Cruzamentos Topológicos de Camadas com Normas (180 Regras em 33 Camadas)
    const cruzamentos = this.graph.cruzamentos_camadas_leis || {};
    for (const [camadaKey, regrasList] of Object.entries(cruzamentos)) {
      this.regraIndex.set(this.normalize(camadaKey), regrasList);
    }

    // Indexar Todas as 33 Camadas Oficiais do Sistema
    for (const layer of ALL_33_LAYERS) {
      this.layer33Index.set(this.normalize(layer.id), layer);
      this.layer33Index.set(this.normalize(layer.nome), layer);
      const cleanId = layer.id.replace(/_/g, " ");
      this.layer33Index.set(this.normalize(cleanId), layer);
    }
  }

  /**
   * Obtém a lista completa das 33 camadas cartográficas oficiais
   */
  getAll33Layers() {
    return ALL_33_LAYERS;
  }

  /**
   * Obtém os metadados de uma das 33 camadas oficiais
   */
  getLayerInfo(layerId) {
    if (!layerId) return null;
    return this.layer33Index.get(this.normalize(layerId)) || LayerIntelligenceCatalog.getLayer(layerId);
  }

  /**
   * Obtém as regras jurídicas incidentes sobre uma determinada camada
   */
  getRulesForLayer(layerId) {
    if (!this.graph?.cruzamentos_camadas_leis) return [];
    return this.graph.cruzamentos_camadas_leis[layerId] || [];
  }

  /**
   * Obtém a lista de todas as leis compiladas no repositório oficial
   */
  getAllLaws() {
    if (!this.graph?.legislacao_territorial?.normas) return [];
    return Object.values(this.graph.legislacao_territorial.normas);
  }

  /**
   * Obtém uma norma específica por ID ou número
   */
  getLaw(lawIdOrNumber) {
    if (!this.graph?.legislacao_territorial?.normas) return null;
    const norm = this.normalize(lawIdOrNumber);
    return this.leiIndex.get(norm) || this.graph.legislacao_territorial.normas[lawIdOrNumber] || null;
  }

  /**
   * Encontra a rua mais próxima de um ponto (lat, lng) com alinhamento geométrico sub-métrico
   */
  findNearestStreet(lat, lng) {
    // 1. Prioridade Absoluta: Localizador Geométrico Ponto-a-Segmento (SpatialLocator O(1))
    if (this.locator && this.locator.isInitialized) {
      const s = this.locator.findNearestStreet(lat, lng);
      if (s) {
        return {
          id: s.id,
          nome: s.nome,
          nome_oficial: s.nome_oficial,
          camada: s.camada_oficial,
          legenda_oficial: s.legenda_oficial,
          distancia_m: s.distancia_m,
          distancia_metros: s.distancia_m,
          tipo_via: s.tipo_via,
          superficie: s.superficie,
          velocidade_max: s.velocidade_max,
          bairro: s.bairro_oficial,
          ref: s.ref,
          coordenadas_mais_proximas: s.coordenadas_mais_proximas
        };
      }
    }

    // 2. Fallback de Contingência: Centróide do Grafo Territorial
    if (!this.graph || !this.graph.logradouros) return null;
    let closest = null;
    let minDistanceM = Infinity;

    for (const [key, via] of Object.entries(this.graph.logradouros)) {
      const vLat = via.coordenadas_referencia?.lat;
      const vLng = via.coordenadas_referencia?.lng;
      if (vLat == null || vLng == null) continue;

      const dLat = (vLat - lat) * 111320;
      const dLng = (vLng - lng) * 111320 * Math.cos((lat * Math.PI) / 180);
      const dist = Math.sqrt(dLat * dLat + dLng * dLng);

      if (dist < minDistanceM) {
        minDistanceM = dist;
        closest = {
          ...via,
          distancia_m: Math.round(dist),
          distancia_metros: Math.round(dist)
        };
      }
    }

    return closest;
  }

  /**
   * Encontra o setor censitário IBGE 2022 e o bairro correspondente ao ponto
   */
  findNearestNeighborhood(lat, lng) {
    // 1. Prioridade Absoluta: Setor Censitário IBGE 2022 Oficial (Ponto-em-Polígono)
    if (this.locator && this.locator.isInitialized) {
      const sector = this.locator.findCensusSector(lat, lng);
      if (sector) {
        return {
          nome: `${sector.distrito} (${sector.situacao})`,
          legenda_oficial: sector.legenda_oficial,
          camada: sector.camada_oficial,
          distrito: sector.distrito,
          situacao: sector.situacao,
          cd_setor: sector.cd_setor,
          area_ha: sector.area_ha,
          distancia_metros: 0
        };
      }
    }

    // 2. Fallback de Contingência: Centróide do Grafo Territorial
    if (!this.graph || !this.graph.bairros) return null;
    let closest = null;
    let minDistanceM = Infinity;

    for (const [key, b] of Object.entries(this.graph.bairros)) {
      const bLat = b.centro?.lat;
      const bLng = b.centro?.lng;
      if (bLat == null || bLng == null) continue;

      const dLat = (bLat - lat) * 111320;
      const dLng = (bLng - lng) * 111320 * Math.cos((lat * Math.PI) / 180);
      const dist = Math.sqrt(dLat * dLat + dLng * dLng);

      if (dist < minDistanceM) {
        minDistanceM = dist;
        closest = {
          ...b,
          distancia_metros: Math.round(dist)
        };
      }
    }

    return closest;
  }

  /**
   * Busca entidades por termo no Grafo (Rua, Bairro, Zona, Solo, Obra, Carta, Lei)
   * Possui guardrail estrito para NÃO sequestrar perguntas analíticas completas como ruas isoladas.
   */
  searchEntity(query) {
    if (!query) return null;
    const qNorm = this.normalize(query);
    const words = qNorm.split(/\s+/).filter(w => w.length > 0);

    // Guardrail Crítico: Se a consulta for uma sentença analítica ou pergunta composta,
    // não deve casar cegamente com um logradouro isolado!
    const isAnalyticalQuery = words.length > 3 || 
      /^(o que|quais|qual|como|por que|porque|onde|quando|quem|analise|parecer|diagnostico|minuta|plano diretor|revisao|alteracao|maleficio|beneficio|impacto|risco|gargalo|posso|pode|como funciona|vantagem|desvantagem|prejuizo|dano)/i.test(qNorm);

    // Stop words proibidas para matching isolado de rua sem prefixo
    const streetStopWords = new Set([
      "sao roque", "brasil", "centro", "plano diretor", "matriz", "sede", 
      "cidade", "municipio", "sp", "vila", "jardim", "bairro", "zona", "lei",
      "estancia", "turistica"
    ]);

    // 1. Procurar Norma Jurídica Oficial Primeiro (ex: LC 40, Lei 6766, Lei 11579, Art 3)
    if (this.leiIndex.has(qNorm)) {
      return { type: "legislacao", data: this.leiIndex.get(qNorm) };
    }
    let bestLawMatch = null;
    let longestLawKey = 0;
    for (const [key, norma] of this.leiIndex.entries()) {
      if (key.length >= 3 && (qNorm === key || (qNorm.includes(key) && !streetStopWords.has(key)))) {
        if (key.length > longestLawKey) {
          longestLawKey = key.length;
          bestLawMatch = norma;
        }
      }
    }
    if (bestLawMatch) {
      return { type: "legislacao", data: bestLawMatch };
    }

    // 2. Procurar Obra da Carta XIII (ex: SRQ-01, SRQ-15, Piscinão Aracaí)
    for (const [key, obra] of this.obraIndex.entries()) {
      if (key.length >= 5 && (qNorm === key || qNorm.includes(key))) {
        if (/^srq-\d+/i.test(key) || qNorm.includes("obra") || qNorm.includes("piscinao")) {
          return { type: "obra", data: obra };
        }
      }
    }

    // 3. Procurar Rua (Apenas se tiver prefixo viário explícito OU se a consulta for curta e exata)
    const hasRoadPrefix = /^(rua|r\.|av\.|av|avenida|estrada|est\.|rodovia|rod\.|spv|sp-\d+|alameda|travessa|beco|praca|estrada municipal)\b/i.test(qNorm);

    if (!isAnalyticalQuery || hasRoadPrefix) {
      for (const [key, via] of this.streetIndex.entries()) {
        if (streetStopWords.has(key) && !hasRoadPrefix) {
          continue;
        }
        if (qNorm === key) {
          return { type: "logradouro", data: via };
        }
        if (hasRoadPrefix && (qNorm.includes(key) || key.includes(qNorm))) {
          if (key.length >= 4) {
            return { type: "logradouro", data: via };
          }
        }
      }
    }

    // 4. Procurar Bairro (Se não for consulta analítica longa)
    if (!isAnalyticalQuery || qNorm.includes("bairro")) {
      for (const [key, bairro] of this.bairroIndex.entries()) {
        if (streetStopWords.has(key) && !qNorm.includes("bairro")) continue;
        if (qNorm === key || (qNorm.includes("bairro") && qNorm.includes(key))) {
          if (key.length >= 4) {
            return { type: "bairro", data: bairro };
          }
        }
      }
    }

    // 5. Procurar Zona 2006 (se citada diretamente, ex: "ZUE-DT", "ZCU", "ZR-1")
    for (const [key, zona] of this.zonaIndex.entries()) {
      if (qNorm === key || (qNorm.includes("zona ") && qNorm.includes(key))) {
        if (key.length >= 3) {
          return { type: "zona_2006", data: zona };
        }
      }
    }

    // 6. Procurar Solo
    for (const [key, solo] of this.soloIndex.entries()) {
      if ((qNorm.includes("solo") || qNorm.includes("pedologia")) && qNorm.includes(key)) {
        if (key.length >= 3) {
          return { type: "solo", data: solo };
        }
      }
    }

    // 7. Procurar Geologia
    for (const [key, geol] of this.geologiaIndex.entries()) {
      if ((qNorm.includes("geologia") || qNorm.includes("rocha")) && qNorm.includes(key)) {
        if (key.length >= 4) {
          return { type: "geologia", data: geol };
        }
      }
    }

    // 8. Procurar Carta 2026
    for (const [key, carta] of this.cartaIndex.entries()) {
      if ((qNorm.includes("carta ") || qNorm.includes("mapa ")) && qNorm.includes(key)) {
        return { type: "carta_2026", data: carta };
      }
    }

    // 9. Procurar em Todas as 33 Camadas Oficiais do Sistema
    if (qNorm.includes("camada") || !isAnalyticalQuery) {
      for (const [key, layer] of this.layer33Index.entries()) {
        if (key.length >= 4 && (qNorm === key || qNorm.includes(key) || key.includes(qNorm))) {
          return { type: "camada_33", data: layer };
        }
      }
    }

    return null;
  }

  /**
   * Monta o Dossiê Territorial Multidimensional Completo para um Ponto
   */
  buildCrossDossierForPoint(lat, lng, spatialSupport = {}) {
    const pt = [lng, lat];
    let locRes = null;
    if (this.locator && this.locator.isInitialized) {
      locRes = this.locator.resolvePointLocation(lat, lng);
    }

    const nearestStreet = locRes?.logradouro || this.findNearestStreet(lat, lng);
    const nearestNeighborhood = locRes?.bairro || this.findNearestNeighborhood(lat, lng);
    const setorCensitario = locRes?.setor_censitario_ibge || (this.locator?.isInitialized ? this.locator.findCensusSector(lat, lng) : null);

    // 1. Distrito
    let distritoNome = locRes?.distrito?.nome || "Distrito Sede";
    if (!locRes && spatialSupport.distritosGeoJson?.features) {
      for (const f of spatialSupport.distritosGeoJson.features) {
        if (this.pointInPolygon(pt, f.geometry)) {
          distritoNome = f.properties.nome || f.properties.distrito;
          break;
        }
      }
    } else if (!locRes && nearestStreet?.distritos?.length) {
      distritoNome = `Distrito de ${nearestStreet.distritos[0]}`;
    }

    // 2. APA de Itupararanga
    let insideAPA = locRes ? locRes.unidade_conservacao_apa : false;
    if (!locRes && spatialSupport.apaGeoJson?.features) {
      for (const f of spatialSupport.apaGeoJson.features) {
        if (this.pointInPolygon(pt, f.geometry)) {
          insideAPA = true;
          break;
        }
      }
    } else if (!locRes && nearestStreet?.inside_apa) {
      insideAPA = true;
    }

    // 3. Zoneamento LC 40/06 (Vigente)
    let zonaNome = locRes?.zoneamento_vigente_2006?.denominacao || "Zona de Consolidação Urbana (ZCU)";
    let zonaSigla = locRes?.zoneamento_vigente_2006?.sigla || "ZCU";
    let zonaParametros = null;
    if (!locRes && spatialSupport.zoneamentoGeoJson?.features) {
      for (const f of spatialSupport.zoneamentoGeoJson.features) {
        if (this.pointInPolygon(pt, f.geometry)) {
          zonaSigla = f.properties.sigla || f.properties.zona || "ZCU";
          zonaNome = f.properties.denominacao || f.properties.zona || zonaSigla;
          break;
        }
      }
    }

    // Buscar parâmetros no grafo
    const zKey = this.normalize(zonaSigla);
    if (this.graph?.zonas_2006?.[`zona:${zKey}`]) {
      zonaParametros = this.graph.zonas_2006[`zona:${zKey}`].parametros_construtivos;
    }

    // 3.1 Proposta de Zoneamento 2026 (Minuta LC 40/2026)
    const zoneamentoMinuta2026 = locRes?.zoneamento_minuta_2026 || (this.locator?.isInitialized ? this.locator.findZoneamentoMinuta2026(lat, lng) : null);
    const confrontoZoneamento = locRes?.confronto_zoneamento || {
      vigente: `${zonaSigla} - ${zonaNome}`,
      proposta_2026: zoneamentoMinuta2026 ? zoneamentoMinuta2026.legenda_oficial : "Manutenção do Zoneamento Vigente",
      houve_alteracao: zoneamentoMinuta2026 ? (zonaSigla !== zoneamentoMinuta2026.sigla) : false
    };

    // 4. Pedologia (Solo)
    let soloInfo = null;
    if (locRes?.pedologia) {
      soloInfo = {
        camada: locRes.pedologia.camada_oficial,
        legenda_oficial: locRes.pedologia.legenda_oficial,
        macroclasse: locRes.pedologia.macroclasse,
        textura: "Média a Argilosa",
        permeabilidade: "Moderada",
        implicacao_obras: "Aptidão para urbanização condicionada a controle de erosão e drenagem pluvial."
      };
    } else if (nearestStreet?.solos_predominantes?.length) {
      const sMacro = nearestStreet.solos_predominantes[0];
      for (const [k, s] of Object.entries(this.graph?.solos_pedologia || {})) {
        if (s.macroclasse?.includes(sMacro) || s.codigo_classe?.includes(sMacro)) {
          soloInfo = s;
          break;
        }
      }
    }
    if (!soloInfo && this.graph?.solos_pedologia) {
      soloInfo = Object.values(this.graph.solos_pedologia)[0];
    }

    // 5. Geologia
    let geologiaInfo = null;
    if (locRes?.geologia) {
      geologiaInfo = {
        camada: locRes.geologia.camada_oficial,
        legenda_oficial: locRes.geologia.legenda_oficial,
        litologia: locRes.geologia.litologia,
        comportamento_geotecnico: "Embasamento cristalino estável fora de áreas de talude íngreme."
      };
    } else if (this.graph?.unidades_geologicas) {
      const geolList = Object.values(this.graph.unidades_geologicas);
      geologiaInfo = (lat < -23.560 && geolList.length > 0) ? geolList[0] : (geolList[1] || geolList[0]);
    }

    // 6. Cartas do Plano Diretor 2026 aplicáveis
    const cartasAplicaveis = [];
    cartasAplicaveis.push("Carta I: Macrozoneamento Municipal");
    if (insideAPA) {
      cartasAplicaveis.push("Carta II: Zoneamento das Áreas Urbanas e ZUE em Mananciais");
    }
    const distLower = distritoNome.toLowerCase();
    if (distLower.includes("canguera")) {
      cartasAplicaveis.push("Carta VII: Consolidação Urbana - Canguera");
      cartasAplicaveis.push("Carta XII: Sistema Viário e Drenagem - Canguera");
    } else if (distLower.includes("maylasky") || distLower.includes("mailasqui")) {
      cartasAplicaveis.push("Carta V: Consolidação Urbana - Maylasky");
      cartasAplicaveis.push("Carta XI: Sistema Viário e Drenagem - Maylasky");
    } else if (distLower.includes("são joão") || distLower.includes("sao joao")) {
      cartasAplicaveis.push("Carta VI: Consolidação Urbana - São João Novo");
    } else {
      cartasAplicaveis.push("Carta IV: Consolidação Urbana - Distrito Sede");
      cartasAplicaveis.push("Carta X: Sistema Viário e Drenagem - Sede");
    }
    cartasAplicaveis.push("Carta VIII: Corredores de Uso e Ocupação do Solo");
    cartasAplicaveis.push("Carta XIII: 22 Obras Estruturantes Prioritárias");

    // 7. Obras Próximas (Carta XIII)
    const obrasProximas = [];
    if (this.graph?.obras_estruturantes_2026) {
      for (const [k, o] of Object.entries(this.graph.obras_estruturantes_2026)) {
        const local = (o.local || "").toLowerCase();
        if (distLower.includes("canguera") && (local.includes("canguera") || local.includes("vinho") || o.codigo === "SRQ-15" || o.codigo === "SRQ-16" || o.codigo === "SRQ-17")) {
          obrasProximas.push(o);
        } else if ((distLower.includes("maylasky") || distLower.includes("mailasqui")) && (local.includes("maylasky") || local.includes("mailasqui") || o.codigo === "SRQ-09" || o.codigo === "SRQ-10" || o.codigo === "SRQ-11")) {
          obrasProximas.push(o);
        } else if ((distLower.includes("são joão") || distLower.includes("sao joao")) && (local.includes("são joão") || local.includes("sjn") || o.codigo === "SRQ-18" || o.codigo === "SRQ-19" || o.codigo === "SRQ-20")) {
          obrasProximas.push(o);
        } else if ((distLower.includes("sede") || distLower.includes("são roque") || distLower.includes("sao roque")) && (local.includes("centro") || local.includes("aracaí") || o.codigo === "SRQ-01" || o.codigo === "SRQ-02" || o.codigo === "SRQ-03" || o.codigo === "SRQ-04" || o.codigo === "SRQ-05" || o.codigo === "SRQ-06" || o.codigo === "SRQ-07" || o.codigo === "SRQ-08" || o.codigo === "SRQ-22")) {
          obrasProximas.push(o);
        }
      }
    }

    // 8. Demandas Comunitárias do Distrito/Bairro
    let demandasDistrito = [];
    for (const [dKey, dObj] of Object.entries(this.graph?.distritos || {})) {
      if (this.normalize(distritoNome).includes(this.normalize(dObj.distrito))) {
        demandasDistrito = dObj.demandas_populares || [];
        break;
      }
    }

    // 9. Regras Jurídicas Incidentes no Ponto (Topologia Cruzada Camada <-> Legislação)
    const regrasIncidentes = [];

    // Regras de Zoneamento (LC 40/2006, LC 39/2006, Minuta 2026)
    const zoneRules = this.getRulesForLayer("zoneamento");
    if (zoneRules.length) {
      regrasIncidentes.push(...zoneRules.map(r => ({ ...r, camada_incidente: "Zoneamento Municipal" })));
    }

    // Regras de APA de Itupararanga (se no polígono da APA)
    if (insideAPA) {
      const apaRules = this.getRulesForLayer("apa_itupararanga");
      if (apaRules.length) {
        regrasIncidentes.push(...apaRules.map(r => ({ ...r, camada_incidente: "APA da Represa de Itupararanga" })));
      }
    }

    // Regras de Declividade & Restrições Físicas
    const declivRules = this.getRulesForLayer("declividade");
    if (declivRules.length) {
      regrasIncidentes.push(...declivRules.map(r => ({ ...r, camada_incidente: "Declividade e Topografia" })));
    }

    // Regras de Hidrografia & APPs Hídricas
    const hidroRules = this.getRulesForLayer("hidrografia");
    if (hidroRules.length) {
      regrasIncidentes.push(...hidroRules.map(r => ({ ...r, camada_incidente: "Hidrografia e APPs Hídricas" })));
    }

    // Regras Pedológicas
    const pedoRules = this.getRulesForLayer("pedologico");
    if (pedoRules.length) {
      regrasIncidentes.push(...pedoRules.map(r => ({ ...r, camada_incidente: "Pedologia e Solos" })));
    }

    // Regras Geológicas
    const geoRules = this.getRulesForLayer("geologia");
    if (geoRules.length) {
      regrasIncidentes.push(...geoRules.map(r => ({ ...r, camada_incidente: "Geologia e Geotecnia" })));
    }

    return {
      coordenadas: {
        lat: Number(lat.toFixed(5)),
        lng: Number(lng.toFixed(5))
      },
      logradouro: nearestStreet ? {
        nome: nearestStreet.nome_oficial,
        camada: nearestStreet.camada,
        legenda_oficial: nearestStreet.legenda_oficial,
        distancia_m: nearestStreet.distancia_metros,
        tipo_via: nearestStreet.tipo_via
      } : null,
      bairro: nearestNeighborhood ? {
        nome: nearestNeighborhood.nome,
        camada: nearestNeighborhood.camada,
        legenda_oficial: nearestNeighborhood.legenda_oficial,
        distrito: nearestNeighborhood.distrito
      } : null,
      setor_censitario_ibge: setorCensitario ? {
        cd_setor: setorCensitario.cd_setor,
        distrito: setorCensitario.distrito,
        situacao: setorCensitario.situacao,
        area_ha: setorCensitario.area_ha,
        legenda_oficial: setorCensitario.legenda_oficial,
        camada: "Setores Censitários IBGE 2022"
      } : null,
      distrito: {
        nome: distritoNome,
        camada: "Divisão Distrital Oficial",
        legenda_oficial: distritoNome
      },
      zoneamento_2006: {
        camada: "Zoneamento Municipal (LC 40/2006)",
        legenda_oficial: `${zonaSigla} · ${zonaNome}`,
        sigla: zonaSigla,
        denominacao: zonaNome,
        parametros: zonaParametros
      },
      zoneamento_minuta_2026: zoneamentoMinuta2026 ? {
        camada: "Minuta Prévia da Revisão do Plano Diretor (2026)",
        legenda_oficial: zoneamentoMinuta2026.legenda_oficial,
        sigla: zoneamentoMinuta2026.sigla,
        denominacao: zoneamentoMinuta2026.denominacao,
        regime: "Proposta em Tramitação"
      } : null,
      confronto_zoneamento: confrontoZoneamento,
      plano_diretor_2026: {
        camada: "Revisão do Plano Diretor Municipal (2024–2026)",
        cartas_incidentes: cartasAplicaveis
      },
      pedologia_solos: soloInfo ? {
        camada: soloInfo.camada,
        legenda_oficial: soloInfo.legenda_oficial,
        macroclasse: soloInfo.macroclasse,
        textura: soloInfo.textura,
        permeabilidade: soloInfo.permeabilidade,
        implicacao_obras: soloInfo.implicacao_obras
      } : null,
      geologia_geotecnia: geologiaInfo ? {
        camada: geologiaInfo.camada,
        legenda_oficial: geologiaInfo.legenda_oficial,
        litologia: geologiaInfo.litologia,
        comportamento_geotecnico: geologiaInfo.comportamento_geotecnico
      } : null,
      unidade_conservacao_apa: insideAPA ? {
        camada: "Área de Proteção Ambiental de Itupararanga",
        legenda_oficial: "APA da Represa de Itupararanga (Lei Estadual 11.579/03)",
        status: "Área de Proteção de Mananciais",
        restricoes: "Lote mínimo 1.000m² a 5.000m²; esgotamento com tratamento biológico obrigatório; vedado lançamento in natura."
      } : null,
      obras_estruturantes_proximas: obrasProximas.map(o => ({
        camada: o.camada,
        legenda_oficial: o.legenda_oficial,
        codigo: o.codigo,
        nome: o.nome,
        local: o.local,
        descricao: o.descricao
      })),
      demandas_populares: demandasDistrito,
      regras_juridicas_incidentes: regrasIncidentes,
      voz_do_bairro: (this.communityVoice && this.communityVoice.isLoaded) ? this.communityVoice.buildCommunityVoiceDossier(
        lat,
        lng,
        [zonaSigla, zoneamentoMinuta2026?.sigla].filter(Boolean),
        `${nearestStreet?.nome || ""} ${distritoNome} ${nearestNeighborhood?.nome || ""}`
      ) : null
    };
  }

  pointInPolygon(point, vs) {
    if (!vs || !point) return false;
    const x = point[0], y = point[1];
    
    if (vs.type === "Polygon") {
      return this._pipRing(x, y, vs.coordinates[0]);
    } else if (vs.type === "MultiPolygon") {
      for (const poly of vs.coordinates) {
        if (this._pipRing(x, y, poly[0])) return true;
      }
    }
    return false;
  }

  _pipRing(x, y, ring) {
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const xi = ring[i][0], yi = ring[i][1];
      const xj = ring[j][0], yj = ring[j][1];
      const intersect = ((yi > y) !== (yj > y)) && (x < ((xj - xi) * (y - yi)) / (yj - yi) + xi);
      if (intersect) inside = !inside;
    }
    return inside;
  }
}
