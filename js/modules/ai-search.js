/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · ASSISTENTE DE INTELIGÊNCIA TERRITORIAL COM IA (v5.5)
 * ===============================================================================
 * Código IBGE: 3550605 · Estância Turística de São Roque (SP)
 * 
 * Arquitetura Desacoplada e Modular:
 *  - AIContextBuilder (js/modules/ai/ai-context-builder.js): constrói prompts e deep context com todas as 33 camadas
 *  - AIAnswerRenderer (js/modules/ai/ai-answer-renderer.js): renderiza respostas, réplicas, botões e markdown
 *  - AIWebSearchEngine (js/modules/ai/ai-web-search.js): busca em bases abertas e portais oficiais com identificação de fontes
 *  - AILocalFallback (js/modules/ai/ai-local-fallback.js): motor determinístico para contingência e réplicas multi-turno
 *  - SpatialCrossEngine (js/modules/spatial-cross-engine.js): topologia cruzada ("tudo ligado a tudo")
 * 
 * Inovações:
 *  - Modal Persistente: Permanece aberto até o clique no botão explícito (#btn-close-ai-response)
 *  - Diálogo Multi-Turno: Substitui a ai-actions-box por caixa de réplica/aprofundamento contínuo
 *  - Extensão Contínua de Resposta: Cada réplica se soma em .ai-response-text.ai-markdown-body
 *  - Grounding Web Transparente: Citação auditável de fontes oficiais (Câmara, Prefeitura, TJ-SP, IBGE)
 * ===============================================================================
 */

import { SpatialCrossEngine } from "./spatial-cross-engine.js";
import { AIContextBuilder } from "./ai/ai-context-builder.js";
import { AIAnswerRenderer } from "./ai/ai-answer-renderer.js";
import { AIWebSearchEngine } from "./ai/ai-web-search.js";
import { AILocalFallback } from "./ai/ai-local-fallback.js";

export class AISearchEngine {
  constructor(map, layerManager, attributeModal, legislationCatalog) {
    this.map = map;
    this.layerManager = layerManager;
    this.attributeModal = attributeModal;
    this.legislationCatalog = legislationCatalog;

    this.knowledgeBase = null;
    this.isSearching = false;

    // Estado do Modal Persistente
    this.isResponseOpen = false;

    // Histórico de Conversação Multi-Turno
    this.conversationHistory = [];

    // Motor de Topologia e Inteligência Territorial Cruzada (Tudo Ligado a Tudo)
    this.crossEngine = new SpatialCrossEngine();

    // Motor de Busca Web e Repositórios Oficiais
    this.webSearch = new AIWebSearchEngine();

    // Módulos Desacoplados de IA
    this.contextBuilder = new AIContextBuilder();
    this.renderer = new AIAnswerRenderer({
      onToggleLayer: (layerId) => this.toggleLayer(layerId),
      onFlyTo: (lat, lon, zoom) => this.flyTo(lat, lon, zoom),
      onFocusObra: (obraCode) => this.focusObra(obraCode),
      onOpenZoneModal: (zoneKey) => this.openZoneModal(zoneKey),
      onBackToSuggestions: () => this.showSuggestions(),
      onCloseResponse: () => this.closeAIResponse(),
      onFollowUp: (query, useWeb) => this.handleFollowUp(query, useWeb)
    });

    // Configuração do Modelo Gemini 4 Argon
    this.model = "gemini-4-argon";
    const workerBaseUrl = window.SR_GEMINI_WORKER_URL || "";
    this.geminiProxyUrl = workerBaseUrl
      ? `${workerBaseUrl.replace(/\/+$/, "")}/api/argon`
      : (
      ["localhost", "127.0.0.1"].includes(window.location.hostname)
        ? "http://127.0.0.1:8000/api/argon"
        : ""
      );
    this.useGemini = Boolean(this.geminiProxyUrl);

    // Ponto ativo no mapa (selection-pin-marker)
    this.activePin = null;

    // Dados geográficos auxiliares para consulta pontual (Point-in-Polygon)
    this.distritosGeoJson = null;
    this.apaGeoJson = null;
    this.zoneamentoGeoJson = null;

    // Elementos DOM
    this.containerEl = document.getElementById("ai-search-container");
    this.inputEl = document.getElementById("ai-search-input");
    this.submitBtn = document.getElementById("ai-search-submit");
    this.clearBtn = document.getElementById("ai-search-clear");
    this.dropdownEl = document.getElementById("ai-search-dropdown");
    this.suggestionsEl = document.getElementById("ai-search-suggestions");
    this.responseEl = document.getElementById("ai-search-response");
    this.kbdEl = document.querySelector(".ai-search-kbd");

    // Elementos do Ponto Marcado (Pin Indicator)
    this.pinIndicatorEl = document.getElementById("ai-search-pin-indicator");
    this.pinInfoTextEl = document.getElementById("ai-pin-info-text");
    this.pinClearBtn = document.getElementById("ai-pin-clear-btn");
  }

  async init() {
    // 1. Carrega Base de Conhecimento Estruturada
    try {
      const response = await fetch(`data/base_conhecimento_ia.json?v=${Date.now()}`);
      if (!response.ok) throw new Error(`HTTP ${response.status} ao carregar base de conhecimento`);
      this.knowledgeBase = await response.json();
      console.log(`[AISearchEngine] Base IA Territorial Crítica carregada:`, {
        normas: this.knowledgeBase.metadata?.total_normas_cadastradas,
        artigos: this.knowledgeBase.metadata?.total_artigos_indexados,
        cartas: this.knowledgeBase.metadata?.total_cartas_oficiais_2026,
        zonas: this.knowledgeBase.metadata?.total_zonas_parametrizadas,
        modelo: this.model
      });
    } catch (err) {
      console.warn("[AISearchEngine] Falha ao carregar base_conhecimento_ia.json:", err);
    }

    // 2. Carrega GeoJSONs dos limites para Point-in-Polygon em tempo real
    try {
      const [rDist, rApa, rZone] = await Promise.all([
        fetch("data/distritos_sao_roque_web.geojson"),
        fetch("data/apa_itupararanga_limite_sao_roque_web.geojson"),
        fetch("data/pmsr_zoneamento_pmd2006.geojson")
      ]);
      if (rDist.ok) this.distritosGeoJson = await rDist.json();
      if (rApa.ok) this.apaGeoJson = await rApa.json();
      if (rZone.ok) this.zoneamentoGeoJson = await rZone.json();
      console.log("[AISearchEngine] Camadas espaciais de apoio carregadas.");
    } catch (err) {
      console.warn("[AISearchEngine] Erro ao carregar GeoJSONs de apoio espacial:", err);
    }

    // 3. Inicializa o Motor de Topologia e Grafo Territorial Cruzado (Tudo Ligado a Tudo)
    try {
      await this.crossEngine.init();
    } catch (err) {
      console.warn("[AISearchEngine] Erro ao inicializar SpatialCrossEngine:", err);
    }

    this.initEvents();
    this.renderCustomChips();
    this.initSidebarTab();
    this.checkInitialPin();
  }

  initEvents() {
    if (!this.inputEl) return;

    this.inputEl.addEventListener("focus", () => this.openDropdown());
    this.inputEl.addEventListener("input", () => {
      const val = this.inputEl.value.trim();
      if (this.clearBtn) {
        this.clearBtn.style.display = val.length > 0 ? "flex" : "none";
      }
    });

    this.inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        this.handleSearch();
      } else if (e.key === "Escape") {
        this.closeDropdown();
      }
    });

    if (this.submitBtn) {
      this.submitBtn.addEventListener("click", () => this.handleSearch());
    }

    if (this.clearBtn) {
      this.clearBtn.addEventListener("click", () => {
        this.inputEl.value = "";
        this.clearBtn.style.display = "none";
        this.showSuggestions();
        this.inputEl.focus();
      });
    }

    // Botão Remover Ponto do Mapa
    if (this.pinClearBtn) {
      this.pinClearBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (typeof window !== "undefined" && window.GIS && typeof window.GIS.removerPin === "function") {
          window.GIS.removerPin();
        } else {
          this.onPinRemoved();
        }
      });
    }

    // Atalho global '/' ou 'Ctrl+K'
    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
      if (e.key === "/" || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k")) {
        e.preventDefault();
        this.inputEl.focus();
        this.openDropdown();
      }
    });

    if (this.kbdEl) {
      this.kbdEl.addEventListener("click", () => {
        this.inputEl.focus();
        this.openDropdown();
      });
    }

    this.bindChipClicks();

    // Fechar ao clicar fora - MAS SE O MODAL ESTIVER COM RESPOSTA ABERTA, ELE PERMANECE ABERTO!
    document.addEventListener("click", (e) => {
      if (this.isResponseOpen) {
        // Modal persistente: o usuário pode interagir com o mapa ou camadas livremente sem fechar a análise!
        return;
      }
      if (this.containerEl && !this.containerEl.contains(e.target)) {
        this.closeDropdown();
      }
    });
  }

  bindChipClicks() {
    document.querySelectorAll(".ai-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const query = chip.getAttribute("data-query");
        if (query) {
          this.inputEl.value = query;
          if (this.clearBtn) this.clearBtn.style.display = "flex";
          this.handleSearch();
        }
      });
    });
  }

  renderCustomChips() {
    const chipContainer = document.querySelector(".ai-search-chips");
    if (!chipContainer) return;

    const chipsData = [
      { label: "⚠️ O que é ruim? (Diagnóstico e Gargalos)", query: "O que é ruim em São Roque segundo o diagnóstico territorial, leis e o Plano Diretor?" },
      { label: "🗺️ Carta XIII: 22 Obras Prioritárias", query: "Quais são as 22 obras estruturantes e prioritárias de São Roque?" },
      { label: "🏨 Pousada em Canguera / Rota do Vinho", query: "Posso abrir uma pousada em Canguera na Rota do Vinho?" },
      { label: "📐 Lote mínimo e recuos no Jardim Villaça", query: "Qual o lote mínimo, taxa de ocupação e recuos no Jardim Villaça?" },
      { label: "✂️ Como fazer desdobro de lote?", query: "Como funciona o desdobro e fracionamento de lote em São Roque?" },
      { label: "⛰️ Restrições de Declividade ≥ 30%", query: "Posso parcelar ou construir em terreno com declividade acima de 30%?" },
      { label: "🗣️ Pedidos das Audiências Públicas", query: "Quais foram os principais pedidos da população nas audiências do Plano Diretor?" },
      { label: "💧 Regras e Restrições da APA Itupararanga", query: "Quais são as restrições construtivas e de saneamento na APA de Itupararanga?" }
    ];

    chipContainer.innerHTML = chipsData.map(c => 
      `<button type="button" class="ai-chip" data-query="${c.query}">${c.label}</button>`
    ).join("");

    this.bindChipClicks();
  }

  initSidebarTab() {
    const tabBtnAi = document.getElementById("tab-btn-ai");
    const paneAi = document.getElementById("tab-pane-ai");
    const tabMapas = document.getElementById("tab-btn-mapas");
    const tabLeis = document.getElementById("tab-btn-leis");
    const paneMapas = document.getElementById("tab-pane-mapas");
    const paneLeis = document.getElementById("tab-pane-leis");

    if (!tabBtnAi || !paneAi) return;

    tabBtnAi.addEventListener("click", () => {
      [tabMapas, tabLeis].forEach(b => {
        if (b) {
          b.classList.remove("active");
          b.setAttribute("aria-selected", "false");
        }
      });
      [paneMapas, paneLeis].forEach(p => {
        if (p) {
          p.style.display = "none";
          p.classList.remove("active");
          p.setAttribute("aria-hidden", "true");
        }
      });

      tabBtnAi.classList.add("active");
      tabBtnAi.setAttribute("aria-selected", "true");
      paneAi.style.display = "block";
      paneAi.classList.add("active");
      paneAi.setAttribute("aria-hidden", "false");

      this.inputEl.focus();
      this.openDropdown();
    });
  }

  checkInitialPin() {
    if (typeof window !== "undefined" && window.GIS && typeof window.GIS.getPinLocation === "function") {
      const loc = window.GIS.getPinLocation();
      if (loc) {
        this.onPinChanged(loc.lat, loc.lng);
      }
    }
  }

  identifySpatialContext(lat, lng) {
    const pt = [lng, lat];

    // Obtém dossiê topológico do grafo multicamadas (SpatialCrossEngine)
    const dossier = this.crossEngine ? this.crossEngine.buildCrossDossierForPoint(lat, lng, {
      distritosGeoJson: this.distritosGeoJson,
      apaGeoJson: this.apaGeoJson,
      zoneamentoGeoJson: this.zoneamentoGeoJson
    }) : null;

    let distrito = dossier?.distrito?.nome || "São Roque";
    let distritoNomeCompleto = dossier?.distrito?.legenda_oficial || "Distrito de São Roque";
    let insideAPA = !!dossier?.unidade_conservacao_apa;
    let zonaNome = dossier?.zoneamento_2006?.denominacao || "Zona de Consolidação Urbana";
    let zonaKey = dossier?.zoneamento_2006?.sigla || "ZCU";
    let zonaData = dossier?.zoneamento_2006?.parametros || null;
    let zoneamentoMinuta2026 = dossier?.zoneamento_minuta_2026 || null;
    let confrontoZoneamento = dossier?.confronto_zoneamento || null;
    let setorCensitario = dossier?.setor_censitario_ibge || null;
    let logradouro = dossier?.logradouro || null;
    let bairro = dossier?.bairro || null;
    let pedologia = dossier?.pedologia_solos || null;
    let geologia = dossier?.geologia_geotecnia || null;
    let cartasAplicaveis = dossier?.plano_diretor_2026?.cartas_incidentes || ["Carta I: Macrozoneamento"];
    let obrasProximas = dossier?.obras_estruturantes_proximas || [];
    let pedidosLocais = dossier?.demandas_populares || [];

    // Coordenadas Projetadas (UTM Fuso 23S / SIRGAS 2000)
    let utmStr = "UTM Fuso 23S";
    if (typeof window !== "undefined" && window.proj4) {
      try {
        const utm = window.proj4("EPSG:4326", "EPSG:31983", [lng, lat]);
        utmStr = `X: ${Math.round(utm[0])}m, Y: ${Math.round(utm[1])}m (SIRGAS 2000)`;
      } catch (e) {
        utmStr = `Coord: ${lat.toFixed(5)}, ${lng.toFixed(5)}`;
      }
    }

    return {
      lat,
      lng,
      pt,
      distrito,
      distritoNomeCompleto,
      insideAPA,
      zonaNome,
      zonaKey,
      zonaData,
      zoneamentoMinuta2026,
      confrontoZoneamento,
      setorCensitario,
      logradouro,
      bairro,
      pedologia,
      geologia,
      cartasAplicaveis,
      utmStr,
      obrasProximas,
      pedidosLocais,
      dossier
    };
  }

  onPinChanged(lat, lng) {
    this.activePin = this.identifySpatialContext(lat, lng);

    if (this.pinIndicatorEl && this.pinInfoTextEl) {
      const p = this.activePin;
      const viaBadge = p.logradouro ? `🛣️ <strong>${p.logradouro.nome}</strong> (${p.logradouro.distancia_m}m) · ` : "";
      const ibgeBadge = p.setorCensitario ? `<span style="background:rgba(37,99,235,0.15);color:#1d4ed8;font-weight:700;padding:1px 5px;border-radius:4px;font-size:0.75rem;">IBGE ${p.setorCensitario.cd_setor}</span> · ` : "";
      const bairroBadge = p.bairro?.nome ? `${p.bairro.nome} · ` : "";
      const apaBadge = p.insideAPA ? ` · <span style="color:#0284c7;font-weight:700;">💧 APA Itupararanga</span>` : "";
      const soloBadge = p.pedologia?.macroclasse ? ` · 🌱 ${p.pedologia.macroclasse}` : "";
      this.pinInfoTextEl.innerHTML = `${viaBadge}${ibgeBadge}${bairroBadge}<strong>${p.distrito}</strong> · ${p.zonaNome}${apaBadge}${soloBadge} <span style="opacity:0.8;font-size:0.75rem;">(${p.lat.toFixed(4)}, ${p.lng.toFixed(4)})</span>`;
      this.pinIndicatorEl.style.display = "flex";
    }

    if (this.inputEl && !this.inputEl.value) {
      const viaNome = this.activePin.logradouro?.nome ? `próximo à ${this.activePin.logradouro.nome}` : `no ${this.activePin.distrito}`;
      this.inputEl.placeholder = `Pergunte sobre este lote ${viaNome} (${this.activePin.zonaNome})...`;
    }
  }

  onPinRemoved() {
    this.activePin = null;
    if (this.pinIndicatorEl) {
      this.pinIndicatorEl.style.display = "none";
    }
    if (this.inputEl) {
      this.inputEl.placeholder = "Pergunte qualquer coisa à IA: obras da Carta 13, pousada em Canguera, desdobro de lote, recuos, bairros...";
    }
  }

  openDropdown() {
    if (!this.dropdownEl) return;
    this.dropdownEl.style.display = "block";
    if (this.containerEl) this.containerEl.classList.add("is-open");
  }

  closeDropdown() {
    if (!this.dropdownEl) return;
    this.dropdownEl.style.display = "none";
    if (this.containerEl) this.containerEl.classList.remove("is-open");
    this.isResponseOpen = false;
  }

  closeAIResponse() {
    this.isResponseOpen = false;
    this.closeDropdown();
    this.showSuggestions();
  }

  showSuggestions() {
    this.isResponseOpen = false;
    if (this.suggestionsEl) this.suggestionsEl.style.display = "block";
    if (this.responseEl) this.responseEl.style.display = "none";
  }

  showResponse() {
    this.isResponseOpen = true;
    if (this.suggestionsEl) this.suggestionsEl.style.display = "none";
    if (this.responseEl) this.responseEl.style.display = "block";
  }

  async handleSearch() {
    const query = this.inputEl.value.trim();
    if (!query) {
      this.showSuggestions();
      return;
    }

    this.showResponse();
    const pinMsg = this.activePin 
      ? `📍 Analisando lote no ${this.activePin.distrito} (${this.activePin.zonaNome}) com o modelo ${this.model}...`
      : `✨ Executando síntese profunda com o modelo ${this.model} (13 Cartas, 22 Obras, 1.709 artigos e audiências)...`;

    this.renderLoading(pinMsg);

    try {
      const answer = await this.synthesizeAnswer(query);
      
      // Reinicia o histórico de diálogo com esta consulta inicial
      this.conversationHistory = [
        { role: "user", text: query },
        { role: "model", text: answer.markdownText || answer.resumo || "" }
      ];

      this.renderAnswer(answer);
    } catch (err) {
      console.error("[AISearchEngine] Erro ao sintetizar resposta:", err);
      this.renderError("Ocorreu um erro ao processar sua consulta territorial. Reformule a pergunta ou reposicione o pino.");
    }
  }

  /**
   * Trata a réplica / aprofundamento contextual (multi-turno) enviado pela nova ai-followup-box
   */
  async handleFollowUp(followUpQuery, useWebSearch = true) {
    if (!followUpQuery || !followUpQuery.trim()) return;

    const q = followUpQuery.trim();
    console.log(`[AISearchEngine] Réplica de aprofundamento recebida: "${q}" (Web Search: ${useWebSearch})`);

    // Exibe indicador sutil de carregamento no final do corpo existente
    this.renderer.showFollowUpLoading(this.responseEl, `Processando réplica com ${this.model}...`);

    let pinCtx = this.activePin;
    if (!pinCtx && typeof window !== "undefined" && window.GIS && typeof window.GIS.getPinLocation === "function") {
      const loc = window.GIS.getPinLocation();
      if (loc) {
        pinCtx = this.identifySpatialContext(loc.lat, loc.lng);
        this.activePin = pinCtx;
      }
    }

    let webData = null;
    if (useWebSearch) {
      try {
        webData = await this.webSearch.search(q, pinCtx);
      } catch (err) {
        console.warn("[AISearchEngine] Falha na busca multidimensional externa:", err);
      }
    }

    const kb = this.knowledgeBase || {};
    const deepContext = this.buildDeepContext(q, pinCtx, kb);

    let followUpAnswer = null;
    let isArgon = false;

    // 1. Chamada multi-turno ao Gemini 4 Argon
    if (this.useGemini) {
      try {
        const argonResponse = await this.callGeminiArgonMultiTurn(q, this.conversationHistory, deepContext, webData);
        if (argonResponse && argonResponse.length > 50) {
          followUpAnswer = argonResponse;
          isArgon = true;
        }
      } catch (err) {
        console.warn("[AISearchEngine] Gemini Argon falhou na réplica, acionando fallback contextual:", err);
      }
    }

    // 2. Fallback determinístico contextual se Argon não responder
    if (!followUpAnswer) {
      const prevContextText = this.conversationHistory.map(h => h.text).join("\n\n");
      followUpAnswer = AILocalFallback.synthesizeFollowUp(q, prevContextText, pinCtx, kb, this.crossEngine, webData);
      isArgon = false;
    }

    // Atualiza histórico
    this.conversationHistory.push({ role: "user", text: q });
    this.conversationHistory.push({ role: "model", text: followUpAnswer });

    // Oculta loading e anexa o novo turno ao corpo existente (.ai-response-text.ai-markdown-body)
    this.renderer.hideFollowUpLoading(this.responseEl);
    this.renderer.appendFollowUpTurn(this.responseEl, {
      query: q,
      rawMarkdown: followUpAnswer,
      webSources: webData?.sources || [],
      isArgon: isArgon
    });
  }

  renderLoading(msg) {
    this.renderer.renderLoading(this.responseEl, msg);
  }

  renderError(msg) {
    this.renderer.renderError(this.responseEl, msg);
  }

  renderAnswer(data) {
    this.renderer.renderAnswer(this.responseEl, data);
  }

  isDiagnosticQuery(qNorm) {
    return this.contextBuilder.isDiagnosticQuery(qNorm);
  }

  buildDeepContext(query, pinCtx, kb) {
    return this.contextBuilder.buildDeepContext(query, pinCtx, kb, this.crossEngine);
  }

  synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic) {
    return AILocalFallback.synthesize(qRaw, qNorm, pinCtx, kb, isDiagnostic, this.crossEngine);
  }

  // --- CHAMADA DIRETA AO GOOGLE GEMINI 4 ARGON (TURNO ÚNICO) ---
  async callGeminiArgon(userQuery, deepContext) {
    if (!this.geminiProxyUrl) return null;
    const url = this.geminiProxyUrl;
    const systemPrompt = this.contextBuilder.buildSystemPrompt(deepContext);

    const payload = {
      contents: [
        {
          role: "user",
          parts: [{ text: `${systemPrompt}\n\nPERGUNTA DO USUÁRIO:\n${userQuery}` }]
        }
      ],
      generationConfig: {
        temperature: 0.15,
        maxOutputTokens: 3500
      }
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 75000);

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!resp.ok) {
        console.warn(`[AISearchEngine] Gemini API HTTP ${resp.status}`);
        return null;
      }

      const data = await resp.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      return text || null;
    } catch (err) {
      clearTimeout(timeoutId);
      console.warn("[AISearchEngine] Falha na requisição Gemini 4 Argon:", err);
      return null;
    }
  }

  // --- CHAMADA MULTI-TURNO AO GOOGLE GEMINI 4 ARGON (RÉPLICA COM HISTÓRICO & WEB) ---
  async callGeminiArgonMultiTurn(followUpQuery, conversationHistory, deepContext, webData) {
    if (!this.geminiProxyUrl) return null;
    const url = this.geminiProxyUrl;
    const systemPrompt = this.contextBuilder.buildSystemPrompt(deepContext);

    const contents = [];

    // Turno Inicial: Injeta System Prompt e Primeira Pergunta
    if (conversationHistory && conversationHistory.length >= 2) {
      contents.push({
        role: "user",
        parts: [{ text: `${systemPrompt}\n\nPERGUNTA INICIAL DO AUDITOR:\n${conversationHistory[0].text}` }]
      });
      contents.push({
        role: "model",
        parts: [{ text: conversationHistory[1].text }]
      });

      // Turnos intermediários
      for (let i = 2; i < conversationHistory.length; i++) {
        contents.push({
          role: conversationHistory[i].role,
          parts: [{ text: conversationHistory[i].text }]
        });
      }
    } else {
      contents.push({
        role: "user",
        parts: [{ text: systemPrompt }]
      });
    }

    // Turno Atual: Pergunta de Aprofundamento + Grounding de Fontes Web (se houver) + Diretriz Crítica Dialética
    let currentPartText = "";
    if (webData && webData.groundingPrompt) {
      currentPartText += `${webData.groundingPrompt}\n\n`;
    }
    currentPartText += `[DIRETRIZ DE AVALIAÇÃO CRÍTICA & DIALÉTICA EM PROFUNDIDADE]:
Analise a réplica do usuário com postura de Perito Judicial Urbanístico e Ambiental, avaliando obrigatoriamente tanto os aspectos negativos (riscos, malefícios, fragilidades, gargalos) quanto os aspectos positivos (avanços, potencialidades, mitigações).
Fundamente sua crítica no TRIPÉ:
1. Jurídico (Estatuto da Cidade Arts. 2º e 42-B, CF/88 Arts. 182/225, Lei 6.766/79 Art. 3º, APA Itupararanga 11.579/03, LC 39/06 e LC 40/06 vigentes vs Minutas);
2. Científico (Argissolos PVA com erodibilidade, declividades >= 30%, inundações do Aracaí/Guaçu, capacidade hídrica);
3. Notícias & Fatos da Cidade (Câmara EPROCLEG 22.468 protocolos, audiências públicas com moradores).
Conclua com recomendações periciais de condicionantes e emendas para a Câmara Municipal.

PERGUNTA DE APROFUNDAMENTO DO USUÁRIO (MANTENDO O CONTEXTO ANTERIOR):
${followUpQuery}`;

    contents.push({
      role: "user",
      parts: [{ text: currentPartText }]
    });

    const payload = {
      contents: contents,
      generationConfig: {
        temperature: 0.15,
        maxOutputTokens: 3500
      }
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 75000);

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      if (!resp.ok) {
        console.warn(`[AISearchEngine] Gemini Multi-Turn HTTP ${resp.status}`);
        return null;
      }

      const data = await resp.json();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      return text || null;
    } catch (err) {
      clearTimeout(timeoutId);
      console.warn("[AISearchEngine] Falha Gemini Multi-Turn:", err);
      return null;
    }
  }

  /**
   * MOTOR PRINCIPAL DE SÍNTESE TERRITORIAL HÍBRIDA (TURNO INICIAL)
   */
  async synthesizeAnswer(query) {
    const qRaw = query.trim();
    const qNorm = qRaw.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const kb = this.knowledgeBase || {};

    let pinCtx = this.activePin;
    if (!pinCtx && typeof window !== "undefined" && window.GIS && typeof window.GIS.getPinLocation === "function") {
      const loc = window.GIS.getPinLocation();
      if (loc) {
        pinCtx = this.identifySpatialContext(loc.lat, loc.lng);
        this.activePin = pinCtx;
      }
    }

    const isDiagnostic = this.isDiagnosticQuery(qNorm);

    let camadaSugerida = "carta_01_macrozoneamento_2026";
    let defaultCentro = pinCtx ? [pinCtx.lat, pinCtx.lng, 16] : [-23.5350, -47.1350, 13];

    if (qNorm.includes("canguera") || qNorm.includes("vinho")) {
      camadaSugerida = "carta_07_canguera_2026";
      defaultCentro = [-23.5850, -47.1200, 14];
    } else if (qNorm.includes("maylasky") || qNorm.includes("mailasqui")) {
      camadaSugerida = "carta_05_maylasky_2026";
      defaultCentro = [-23.5450, -47.0700, 14];
    } else if (qNorm.includes("sao joao novo") || qNorm.includes("são joão novo")) {
      camadaSugerida = "carta_06_sao_joao_novo_2026";
      defaultCentro = [-23.5800, -47.0100, 14];
    } else if (qNorm.includes("sede") || qNorm.includes("centro")) {
      camadaSugerida = "carta_04_sede_2026";
      defaultCentro = [-23.5350, -47.1350, 15];
    } else if (qNorm.includes("obra") || qNorm.includes("piscinao") || qNorm.includes("aracai") || isDiagnostic) {
      camadaSugerida = "carta_13_obras_prioritarias_2026";
      defaultCentro = [-23.5350, -47.1350, 14];
    } else if (pinCtx?.insideAPA || qNorm.includes("apa") || qNorm.includes("manancial") || qNorm.includes("itupararanga")) {
      camadaSugerida = "carta_02_zue_2026";
      defaultCentro = [-23.5850, -47.1200, 13];
    } else if (qNorm.includes("corredor") || qNorm.includes("raposo") || qNorm.includes("castello")) {
      camadaSugerida = "carta_08_corredores_2026";
      defaultCentro = [-23.5350, -47.1141, 13];
    } else if (qNorm.includes("aeis") || qNorm.includes("interesse social") || qNorm.includes("zeis")) {
      camadaSugerida = "carta_09_aeis_2026";
      defaultCentro = [-23.5350, -47.1141, 13];
    }

    // Pesquisa Multidimensional em 4 Etapas (Jurídico, Científico/Desastres, Notícias e São Roque)
    let webData = null;
    try {
      webData = await this.webSearch.search(qRaw, pinCtx);
    } catch (e) {
      console.warn("[AISearchEngine] Erro ao carregar fontes multidimensionais no turno inicial:", e);
    }

    // 1. Tentativa com o Modelo Gemini 4 Argon
    if (this.useGemini) {
      try {
        const deepContext = this.buildDeepContext(qRaw, pinCtx, kb);
        const augmentedContext = webData?.groundingPrompt ? `${deepContext}\n\n${webData.groundingPrompt}` : deepContext;
        const argonResponse = await this.callGeminiArgon(qRaw, augmentedContext);
        if (argonResponse && argonResponse.length > 100) {
          console.log("[AISearchEngine] ✅ SUCESSO: Resposta do Gemini 4 Argon (sem fallback)");
          return {
            query: qRaw,
            titulo: isDiagnostic 
              ? "Diagnóstico Territorial, Físico e Normativo de São Roque" 
              : (pinCtx ? `Análise do Ponto Marcado (${pinCtx.distrito} · ${pinCtx.zonaNome})` : `Parecer Territorial: "${qRaw}"`),
            categoria: "Inteligência Geoespacial & Jurídica (Gemini 4 Argon)",
            isArgon: true,
            isFallback: false,
            markdownText: argonResponse,
            pinContext: pinCtx,
            camadaSugerida: camadaSugerida,
            centroMapa: defaultCentro,
            origem: "Modelo Google Gemini 4 Argon · RAG Territorial Exaustivo",
            webSources: webData?.sources || []
          };
        }
      } catch (err) {
        console.error("[AISearchEngine] ❌ ERRO: Gemini 4 Argon FALHOU - Ativando FALLBACK", err);
      }
    }

    // 2. Fallback local exaustivo multi-eixo
    console.log("[AISearchEngine] 🔄 Executando FALLBACK local...");
    const fallbackAnswer = this.synthesizeExhaustiveLocalFallback(qRaw, qNorm, pinCtx, kb, isDiagnostic);
    if (fallbackAnswer && typeof fallbackAnswer === "object") {
      fallbackAnswer.webSources = webData?.sources || [];
      fallbackAnswer.isFallback = true;
      fallbackAnswer.isArgon = false;
    }
    console.log("[AISearchEngine] ℹ️ RESPOSTA: FALLBACK (não é Gemini 4 Argon)");
    return fallbackAnswer;
  }

  // --- AÇÕES ESPACIAIS NO MAPA LEAFLET ---
  focusObra(obraCode) {
    const kb = this.knowledgeBase || {};
    const obras = kb.obras_prioritarias_srq || [];
    const obra = obras.find(o => o.codigo === obraCode);

    this.toggleLayer("carta_13_obras_prioritarias_2026");

    if (obra) {
      const loc = (obra.local || "").toLowerCase();
      let coords = [-23.5350, -47.1350, 15];
      if (loc.includes("vinho") || loc.includes("canguera")) coords = [-23.5850, -47.1200, 14];
      else if (loc.includes("são joão") || loc.includes("sao joao")) coords = [-23.5800, -47.0100, 15];
      else if (loc.includes("maylasky") || loc.includes("mailasqui")) coords = [-23.5450, -47.0700, 15];
      else if (loc.includes("saboó") || loc.includes("saboo")) coords = [-23.4950, -47.1500, 14];
      else if (loc.includes("mombaça") || loc.includes("mombaca")) coords = [-23.5150, -47.1250, 15];

      this.flyTo(coords[0], coords[1], coords[2]);
    }
  }

  toggleLayer(layerId) {
    if (!this.layerManager) return;
    try {
      this.layerManager.toggleLayer(layerId);
      console.log(`[AISearchEngine] Camada alternada: ${layerId}`);
    } catch (e) {
      console.warn(`[AISearchEngine] Erro ao alternar camada ${layerId}:`, e);
    }
  }

  flyTo(lat, lon, zoom) {
    if (!this.map) return;
    this.map.flyTo([lat, lon], zoom, {
      duration: 1.2,
      easeLinearity: 0.25
    });
  }

  openZoneModal(zoneKey) {
    if (!this.attributeModal) return;
    const legalCtx = this.legislationCatalog ? this.legislationCatalog.getZoneLegalMetadata(zoneKey) : null;
    this.attributeModal.showZoneLegalDetails(`Zona ${zoneKey}`, { sigla: zoneKey }, legalCtx);
  }
}
