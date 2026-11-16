/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · RENDERIZADOR DE RESPOSTAS E AÇÕES DE MAPA DA IA
 * ===============================================================================
 * Módulo desacoplado responsável por:
 *  - Converter saídas da IA em elementos DOM acessíveis
 *  - Botões interativos Leaflet ([[ACTION:...]]), dossiês visuais e badges
 *  - Botão explícito de fechar no cabeçalho (#btn-close-ai-response)
 *  - Caixa de Réplica / Aprofundamento Contextual (Diálogo Multi-Turno)
 *  - Extensão contínua das respostas em .ai-response-text.ai-markdown-body
 *  - Exibição de fontes web auditáveis e auditabilidade territorial estrita
 * ===============================================================================
 */

export class AIAnswerRenderer {
  constructor(handlers = {}) {
    this.handlers = handlers; // { onToggleLayer, onFlyTo, onFocusObra, onOpenZoneModal, onBackToSuggestions, onCloseResponse, onFollowUp }
  }

  setHandlers(handlers) {
    this.handlers = { ...this.handlers, ...handlers };
  }

  renderLoading(containerEl, msg) {
    if (!containerEl) return;
    containerEl.innerHTML = `
      <div class="ai-loading-state">
        <div class="ai-spinner"></div>
        <div class="ai-loading-text">${msg}</div>
      </div>
    `;
  }

  renderError(containerEl, msg) {
    if (!containerEl) return;
    containerEl.innerHTML = `
      <div class="ai-response-card">
        <div class="ai-response-header">
          <span class="ai-badge" style="background:#fef2f2;color:#991b1b;border:1px solid #fecaca;">⚠️ Consulta</span>
          <button type="button" class="btn-close-ai-response" id="btn-close-ai-response" title="Fechar análise da IA">
            <span class="btn-close-icon">✕</span>
            <span class="btn-close-label">Fechar</span>
          </button>
        </div>
        <div class="ai-response-text" style="border-left-color:#ef4444;color:#991b1b;">
          ${msg}
        </div>
      </div>
    `;
    this.bindActionEvents(containerEl);
  }

  renderAnswer(containerEl, data) {
    if (!containerEl) return;

    // 1. Card de Contexto do Ponto Marcado (Dossiê Territorial Multidimensional)
    let pinCardHtml = "";
    if (data.pinContext) {
      const p = data.pinContext;
      const viaNome = p.logradouro ? `${p.logradouro.nome} (${p.logradouro.distancia_m}m)` : "Via local";
      const bairroNome = p.bairro?.nome ? `${p.bairro.nome} · ` : "";
      const soloNome = p.pedologia?.macroclasse || p.pedologia?.nome_classe || "Argissolo Vermelho-Amarelo (PVA)";
      const geolNome = p.geologia?.nome || "Granito Ibiúna";

      pinCardHtml = `
        <div class="ai-pin-context-card">
          <div class="ai-pin-context-title">
            <span>📍 Dossiê Territorial Cruzado do Ponto Selecionado</span>
            <span style="font-size:0.7rem;opacity:0.8;font-weight:normal;">Interconexão Multicamadas</span>
          </div>
          <div class="ai-pin-context-details">
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Logradouro / Via:</span>
              <span class="ai-pin-context-val">🛣️ ${viaNome}</span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Localização:</span>
              <span class="ai-pin-context-val">🏘️ ${bairroNome}${p.distritoNomeCompleto}</span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Zoneamento (LC 40/06):</span>
              <span class="ai-pin-context-val">📐 ${p.zonaNome}</span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Pedologia (Solos):</span>
              <span class="ai-pin-context-val">🌱 ${soloNome}</span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Geologia:</span>
              <span class="ai-pin-context-val">🪨 ${geolNome}</span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">APA Itupararanga:</span>
              <span class="ai-pin-context-val" style="color: ${p.insideAPA ? '#0284c7' : '#475569'};font-weight:600;">
                ${p.insideAPA ? "💧 SIM (Área de Mananciais - Lei 11.579/03)" : "Não (Fora da APA)"}
              </span>
            </div>
            <div class="ai-pin-context-item">
              <span class="ai-pin-context-label">Coordenadas:</span>
              <span class="ai-pin-context-val">${p.lat.toFixed(5)}, ${p.lng.toFixed(5)} (${p.utmStr})</span>
            </div>
          </div>
        </div>
      `;
    }

    // 2. Processamento do Conteúdo (Markdown Rico com Gemini 4 Argon ou HTML estruturado)
    let bodyHtml = "";
    if (data.isArgon && data.markdownText) {
      let parsed = (typeof window !== "undefined" && window.marked)
        ? window.marked.parse(data.markdownText)
        : this.simpleMarkdownToHtml(data.markdownText);

      parsed = this.parseActionTags(parsed);

      parsed = parsed.replace(/\[FIM DO PARECER(?: TÉCNICO)?\]/gi, () => {
        return `<div class="ai-complete-badge"><span>✅ Parecer Concluído na Íntegra (Modelo Gemini 4 Argon)</span></div>`;
      });

      bodyHtml = `<div class="ai-response-text ai-markdown-body">${parsed}</div>`;
    } else {
      let text = data.resumo || "";
      let parsed = this.parseActionTags(text);
      bodyHtml = `<div class="ai-response-text ai-markdown-body">${parsed}</div>`;
    }

    // 3. Cartas Relacionadas Pills
    let cartasHtml = "";
    if (data.cartasRelacionadas && data.cartasRelacionadas.length > 0) {
      cartasHtml = `
        <div style="margin: 8px 0; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;">
          <span style="font-size: 0.73rem; font-weight: 700; color: #475569; text-transform: uppercase;">🗺️ Cartas Aplicáveis:</span>
          ${data.cartasRelacionadas.map(c => `<span style="font-size: 0.72rem; background: #f1f5f9; color: #0f172a; padding: 2px 7px; border-radius: 4px; border: 1px solid #cbd5e1; font-weight: 600;">${c}</span>`).join("")}
        </div>
      `;
    }

    // 4. Parâmetros Técnicos da Zona (quando não for Argon)
    let paramsHtml = "";
    if (!data.isArgon && data.zona) {
      const z = data.zona;
      paramsHtml = `
        <div class="ai-params-box">
          <div class="ai-params-title">📊 Parâmetros Técnicos Oficiais da Zona (${data.zonaKey || ""})</div>
          <div class="ai-params-grid">
            <div class="ai-param-item">
              <span class="ai-param-label">Taxa de Ocupação Máx.</span>
              <span class="ai-param-val">${z.taxa_ocupacao || (data.pinContext?.insideAPA ? "50%" : "60%")}</span>
            </div>
            <div class="ai-param-item">
              <span class="ai-param-label">Coef. Aproveitamento</span>
              <span class="ai-param-val">${z.coeficiente_aproveitamento || "1.0"}</span>
            </div>
            <div class="ai-param-item">
              <span class="ai-param-label">Gabarito Máximo</span>
              <span class="ai-param-val">${z.gabarito_altura || "12 metros"}</span>
            </div>
            <div class="ai-param-item">
              <span class="ai-param-label">Lote Mínimo</span>
              <span class="ai-param-val">${z.lote_minimo || (data.pinContext?.insideAPA ? "5.000 m²" : "250 m²")}</span>
            </div>
          </div>
          ${z.recuos ? `<div style="font-size: 0.76rem; color: #475569; margin-top: 6px;"><strong>Recuos Obrigatórios:</strong> ${z.recuos}</div>` : ""}
          ${z.usos_admitidos ? `<div style="font-size: 0.76rem; color: #166534; margin-top: 4px;"><strong>Usos Permitidos:</strong> ${z.usos_admitidos}</div>` : ""}
          ${z.restricoes ? `<div style="font-size: 0.76rem; color: #991b1b; margin-top: 4px;"><strong>Restrições Críticas:</strong> ${z.restricoes}</div>` : ""}
        </div>
      `;
    }

    // 4.1 Card de Fontes Multidimensionais Auditáveis (quando houver)
    let sourcesHtml = "";
    if (data.webSources && data.webSources.length > 0) {
      sourcesHtml = this.renderSourcesHtml(data.webSources);
    }

    // 5. Botões de Ação Rápida de Mapa
    const actionButtons = [];
    if (data.camadaSugerida) {
      actionButtons.push(`
        <button type="button" class="btn-ai-action" data-action="toggle-layer" data-layer="${data.camadaSugerida}">
          🗺️ Ativar Carta Principal
        </button>
      `);
    }

    if (data.pinContext) {
      actionButtons.push(`
        <button type="button" class="btn-ai-action" data-action="fly-to" data-lat="${data.pinContext.lat}" data-lon="${data.pinContext.lng}" data-zoom="16">
          🎯 Focar no Ponto Marcado
        </button>
      `);
    } else if (data.centroMapa && data.centroMapa.length >= 2) {
      actionButtons.push(`
        <button type="button" class="btn-ai-action" data-action="fly-to" data-lat="${data.centroMapa[0]}" data-lon="${data.centroMapa[1]}" data-zoom="${data.centroMapa[2] || 15}">
          🎯 Focar Localidade
        </button>
      `);
    }

    // 6. CAIXA DE RÉPLICA & APROFUNDAMENTO CONTEXTUAL (Substitui com inteligência a antiga ai-actions-box)
    const mapShortcutsHtml = actionButtons.length > 0 ? `
      <div class="ai-map-shortcuts-bar">
        <span class="ai-map-shortcuts-label">🗺️ Ações no Mapa:</span>
        <div class="ai-map-shortcuts-buttons">
          ${actionButtons.join("")}
        </div>
      </div>
    ` : "";

    const followupBoxHtml = `
      <div class="ai-followup-box" id="ai-followup-box">
        <div class="ai-followup-header">
          <div class="ai-followup-title">
            <span class="ai-followup-icon">💬</span>
            <span><strong>Aprofundar Análise ou Fazer Nova Pergunta</strong></span>
          </div>
          <label class="ai-web-search-toggle" title="Consultar base ampliada da internet, repositórios públicos municipais e jurisprudência com identificação de fontes">
            <input type="checkbox" id="ai-web-search-toggle" checked />
            <span class="ai-web-search-label">🌐 Busca Web & Fontes</span>
          </label>
        </div>

        <div class="ai-followup-input-wrapper">
          <span class="ai-followup-sparkle">⚡</span>
          <input
            type="text"
            id="ai-followup-input"
            class="ai-followup-input"
            placeholder="Pergunte sobre esta análise (ex: 'Quais os recuos?', 'E se for pousada?', 'Quais as minutas?')..."
            aria-label="Aprofundar análise ou perguntar à IA"
          />
          <button type="button" id="ai-followup-submit" class="ai-followup-submit-btn" title="Enviar pergunta à IA">
            <span>Perguntar</span>
            <span class="ai-followup-arrow">➔</span>
          </button>
        </div>

        <div class="ai-followup-chips">
          <button type="button" class="ai-followup-chip" data-query="Qual o confronto detalhado da LC 40/06 vigente com as minutas e Cartas de 2026 neste caso?">⚖️ Vigente vs. Minuta 2026</button>
          <button type="button" class="ai-followup-chip" data-query="Quais as restrições de declividade, pedologia (solos) e APA de Itupararanga aqui?">🌱 Solos, Declividade & APA</button>
          <button type="button" class="ai-followup-chip" data-query="Quais as demandas da comunidade (Voz do Bairro) e audiências públicas nesta região?">🗣️ Voz do Bairro & Audiências</button>
          <button type="button" class="ai-followup-chip" data-query="Pesquisar notícias, jurisprudência e normas estaduais na internet sobre este ponto">🌐 Fontes Web & Notícias</button>
        </div>

        ${mapShortcutsHtml}
      </div>
    `;

    const modelBadge = data.isArgon 
      ? `<span class="ai-argon-badge">✨ Gemini 4 Argon · RAG Territorial</span>`
      : `<span class="ai-badge ai-badge-ia">✨ Inteligência Territorial Crítica</span>`;

    containerEl.innerHTML = `
      <div class="ai-response-card">
        <div class="ai-response-header">
          <div class="ai-response-tag-row">
            ${modelBadge}
            <span class="ai-badge ai-badge-model">${data.origem}</span>
          </div>
          <div class="ai-response-header-actions">
            <button type="button" class="btn-close-ai-response" id="btn-close-ai-response" title="Fechar análise da IA">
              <span class="btn-close-icon">✕</span>
              <span class="btn-close-label">Fechar</span>
            </button>
          </div>
        </div>

        <h3 class="ai-response-title">${data.titulo}</h3>

        ${pinCardHtml}
        ${cartasHtml}
        ${bodyHtml}
        ${paramsHtml}
        ${sourcesHtml}
        ${followupBoxHtml}
      </div>
    `;

    this.bindActionEvents(containerEl);
  }

  /**
   * Extende a resposta em .ai-response-text.ai-markdown-body com uma nova réplica / pergunta
   */
  appendFollowUpTurn(containerEl, { query, rawMarkdown, webSources, isArgon }) {
    if (!containerEl) return null;

    const bodyEl = containerEl.querySelector(".ai-response-text.ai-markdown-body") || containerEl.querySelector(".ai-response-text");
    if (!bodyEl) return null;

    let parsed = (typeof window !== "undefined" && window.marked)
      ? window.marked.parse(rawMarkdown)
      : this.simpleMarkdownToHtml(rawMarkdown);

    parsed = this.parseActionTags(parsed);

    // Formatação de Fontes Web Expandidas com 4 Pilares
    let sourcesHtml = "";
    if (webSources && webSources.length > 0) {
      sourcesHtml = this.renderSourcesHtml(webSources);
    }

    const turnId = `thread-turn-${Date.now()}`;
    const turnDiv = document.createElement("div");
    turnDiv.className = "ai-thread-turn";
    turnDiv.id = turnId;

    const modelName = isArgon ? "Gemini 4 Argon" : "Síntese RAG Territorial";
    const webBadge = (webSources && webSources.length > 0)
      ? `<span class="ai-thread-web-badge">🌐 ${webSources.length} Fontes Identificadas</span>`
      : "";

    turnDiv.innerHTML = `
      <div class="ai-thread-divider">
        <span class="ai-thread-divider-line"></span>
        <span class="ai-thread-divider-badge">⚡ Réplica & Aprofundamento · ${modelName}</span>
        <span class="ai-thread-divider-line"></span>
      </div>
      <div class="ai-thread-question">
        <div class="ai-thread-q-header">
          <span class="ai-thread-q-avatar">👤 Pergunta de Aprofundamento:</span>
          ${webBadge}
        </div>
        <div class="ai-thread-q-text">${query}</div>
      </div>
      <div class="ai-thread-answer">
        ${parsed}
      </div>
      ${sourcesHtml}
    `;

    bodyEl.appendChild(turnDiv);

    // Re-vincula os botões de ação Leaflet recém-adicionados
    this.bindActionEvents(containerEl);

    // Rolagem suave até a nova resposta
    try {
      turnDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (e) {
      // Ignora erro em ambientes sem scrollIntoView
    }

    return turnDiv;
  }

  showFollowUpLoading(containerEl, msg = "Processando réplica com o modelo Gemini 4 Argon...") {
    if (!containerEl) return;
    this.hideFollowUpLoading(containerEl);

    const bodyEl = containerEl.querySelector(".ai-response-text.ai-markdown-body") || containerEl.querySelector(".ai-response-text");
    if (!bodyEl) return;

    const loadingDiv = document.createElement("div");
    loadingDiv.className = "ai-thread-loading";
    loadingDiv.id = "ai-thread-loading-indicator";
    loadingDiv.innerHTML = `
      <div class="ai-spinner-small"></div>
      <span class="ai-thread-loading-text">${msg}</span>
    `;
    bodyEl.appendChild(loadingDiv);

    try {
      loadingDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } catch (e) {}
  }

  hideFollowUpLoading(containerEl) {
    if (!containerEl) return;
    const old = containerEl.querySelector("#ai-thread-loading-indicator");
    if (old && old.parentNode) {
      old.parentNode.removeChild(old);
    }
  }

  parseActionTags(html) {
    if (!html) return "";

    return html
      .replace(/\[\[ACTION:LAYER:(.*?)\|(.*?)\]\]/g, (match, layerId, label) => {
        return `<button type="button" class="ai-action-btn ai-action-layer" data-action="toggle-layer" data-layer="${layerId.trim()}">🗺️ ${label.trim()}</button>`;
      })
      .replace(/\[\[ACTION:FLYTO:(.*?)\|(.*?)\]\]/g, (match, coords, label) => {
        return `<button type="button" class="ai-action-btn ai-action-flyto" data-action="flyto-coords" data-coords="${coords.trim()}">📍 ${label.trim()}</button>`;
      })
      .replace(/\[\[ACTION:OBRA:(.*?)\|(.*?)\]\]/g, (match, obraCode, label) => {
        return `<button type="button" class="ai-action-btn ai-action-obra" data-action="focus-obra" data-obra="${obraCode.trim()}">🏗️ ${label.trim()}</button>`;
      })
      .replace(/\[\[ACTION:ZONA:(.*?)\|(.*?)\]\]/g, (match, zoneKey, label) => {
        return `<button type="button" class="ai-action-btn" data-action="view-zone-modal" data-zone="${zoneKey.trim()}">📋 ${label.trim()}</button>`;
      });
  }

  bindActionEvents(containerEl) {
    if (!containerEl) return;

    // 1. Botão Fechar Análise (Permanece aberto até o clique)
    const btnClose = containerEl.querySelector("#btn-close-ai-response");
    if (btnClose) {
      btnClose.addEventListener("click", () => {
        if (this.handlers.onCloseResponse) {
          this.handlers.onCloseResponse();
        } else if (this.handlers.onBackToSuggestions) {
          this.handlers.onBackToSuggestions();
        }
      });
    }

    // 2. Caixa de Réplica / Aprofundamento Contextual
    const followupInput = containerEl.querySelector("#ai-followup-input");
    const followupSubmit = containerEl.querySelector("#ai-followup-submit");
    const followupWebToggle = containerEl.querySelector("#ai-web-search-toggle");

    const submitFollowup = (customQuery = null) => {
      const q = (customQuery !== null ? customQuery : (followupInput ? followupInput.value : "")).trim();
      if (!q) return;
      const useWeb = followupWebToggle ? followupWebToggle.checked : true;
      if (this.handlers.onFollowUp) {
        this.handlers.onFollowUp(q, useWeb);
      }
      if (followupInput) followupInput.value = "";
    };

    if (followupSubmit) {
      followupSubmit.onclick = () => submitFollowup();
    }

    if (followupInput) {
      followupInput.onkeydown = (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          submitFollowup();
        }
      };
    }

    containerEl.querySelectorAll(".ai-followup-chip").forEach((chip) => {
      chip.onclick = () => {
        const query = chip.getAttribute("data-query");
        if (query) submitFollowup(query);
      };
    });

    // 3. Botões de Ações de Mapa (Ativar Camada, FlyTo, Focar Obra, Ver Zona)
    containerEl.querySelectorAll(".btn-ai-action, .ai-action-btn").forEach((btn) => {
      btn.onclick = () => {
        const action = btn.getAttribute("data-action");

        if (action === "toggle-layer" && this.handlers.onToggleLayer) {
          const layerId = btn.getAttribute("data-layer");
          this.handlers.onToggleLayer(layerId);
        } else if (action === "fly-to" && this.handlers.onFlyTo) {
          const lat = parseFloat(btn.getAttribute("data-lat"));
          const lon = parseFloat(btn.getAttribute("data-lon"));
          const zoom = parseInt(btn.getAttribute("data-zoom"), 10) || 16;
          this.handlers.onFlyTo(lat, lon, zoom);
        } else if (action === "flyto-coords" && this.handlers.onFlyTo) {
          const coordsStr = btn.getAttribute("data-coords");
          const parts = coordsStr.split(",").map((s) => parseFloat(s.trim()));
          if (parts.length >= 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
            const zoom = parts[2] || 15;
            this.handlers.onFlyTo(parts[0], parts[1], zoom);
          }
        } else if (action === "focus-obra" && this.handlers.onFocusObra) {
          const obraCode = btn.getAttribute("data-obra");
          this.handlers.onFocusObra(obraCode);
        } else if (action === "view-zone-modal" && this.handlers.onOpenZoneModal) {
          const zoneKey = btn.getAttribute("data-zone");
          this.handlers.onOpenZoneModal(zoneKey);
        }
      };
    });

    // 4. Abas de Filtro de Fontes (.ai-sources-tab-btn)
    containerEl.querySelectorAll(".ai-sources-tab-btn").forEach((tabBtn) => {
      tabBtn.onclick = () => {
        const targetId = tabBtn.getAttribute("data-target");
        const filter = tabBtn.getAttribute("data-filter");
        const cardEl = targetId ? containerEl.querySelector(`#${targetId}`) : tabBtn.closest(".ai-sources-card");
        if (!cardEl) return;

        // Atualiza botões
        cardEl.querySelectorAll(".ai-sources-tab-btn").forEach((b) => b.classList.remove("active"));
        tabBtn.classList.add("active");

        // Filtra cards de fontes
        cardEl.querySelectorAll(".ai-source-item").forEach((item) => {
          const pillar = item.getAttribute("data-pillar");
          if (filter === "all" || pillar === filter) {
            item.style.display = "flex";
          } else {
            item.style.display = "none";
          }
        });
      };
    });
  }

  /**
   * Renderiza o Card de Fontes Expandido com Cabeçalho e Abas (.ai-sources-card & .ai-sources-header)
   */
  renderSourcesHtml(sources) {
    if (!sources || sources.length === 0) return "";

    const juridicoCount = sources.filter((s) => s.pillar === "juridico").length;
    const cientificoCount = sources.filter((s) => s.pillar === "cientifico").length;
    const noticiasCount = sources.filter((s) => s.pillar === "noticias").length;
    const localCount = sources.filter((s) => s.pillar === "local").length;

    const cardId = `sources-card-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;

    return `
      <div class="ai-sources-card" id="${cardId}">
        <div class="ai-sources-header">
          <div class="ai-sources-header-main">
            <span class="ai-sources-icon">📚</span>
            <div class="ai-sources-title-box">
              <span class="ai-sources-title">Base de Conhecimento Multidimensional & Evidências Auditáveis (${sources.length})</span>
              <span class="ai-sources-subtitle">⚖️ Jurídico & Regras · 🔬 Ciência & Catástrofes Similares · 📰 Notícias & Fatos · 🏛️ São Roque Local</span>
            </div>
          </div>
          <div class="ai-sources-tabs">
            <button type="button" class="ai-sources-tab-btn active" data-filter="all" data-target="${cardId}">Todos (${sources.length})</button>
            ${juridicoCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="juridico" data-target="${cardId}">⚖️ Jurídico (${juridicoCount})</button>` : ""}
            ${cientificoCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="cientifico" data-target="${cardId}">🔬 Ciência & Desastres (${cientificoCount})</button>` : ""}
            ${noticiasCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="noticias" data-target="${cardId}">📰 Notícias & Fatos (${noticiasCount})</button>` : ""}
            ${localCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="local" data-target="${cardId}">🏛️ São Roque (${localCount})</button>` : ""}
          </div>
        </div>

        <div class="ai-sources-list">
          ${sources.map((s, idx) => {
            let orientationClass = "ai-source-role-regra";
            if (s.orientation === "ALERTA") orientationClass = "ai-source-role-alerta";
            else if (s.orientation === "APOIO") orientationClass = "ai-source-role-apoio";
            else if (s.orientation === "ESTUDO_COMPARATIVO") orientationClass = "ai-source-role-comparativo";

            const pillar = s.pillar || "local";
            const pillarClass = `ai-source-pillar-${pillar}`;
            const pillarIcon = s.pillarIcon || "🌐";
            const pillarName = s.pillarName || s.category || "Fonte Oficial";
            const orientLabel = s.orientationLabel || s.orientation || "Referência";

            return `
              <a href="${s.url}" target="_blank" rel="noopener noreferrer" class="ai-source-item ${pillarClass}" data-pillar="${pillar}" title="Auditar no repositório oficial: ${s.url}">
                <div class="ai-source-badge-row">
                  <span class="ai-source-index">#${idx + 1}</span>
                  <span class="ai-source-pillar-tag">${pillarIcon} ${pillarName}</span>
                  <span class="ai-source-role-badge ${orientationClass}">${orientLabel}</span>
                  <span class="ai-source-domain">${s.domain}</span>
                </div>
                <div class="ai-source-item-title">${s.title} <span class="ai-source-external-arrow">↗</span></div>
                <div class="ai-source-item-snippet">${s.snippet}</div>
              </a>
            `;
          }).join("")}
        </div>
      </div>
    `;
  }

  simpleMarkdownToHtml(md) {
    if (!md) return "";
    return md
      .replace(/### (.*?)\n/g, "<h4 style='color:#1e3a8a;margin:10px 0 4px;'>$1</h4>")
      .replace(/## (.*?)\n/g, "<h3 style='color:#1e3a8a;margin:12px 0 6px;'>$1</h3>")
      .replace(/# (.*?)\n/g, "<h2 style='color:#1e3a8a;margin:14px 0 8px;'>$1</h2>")
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/- (.*?)\n/g, "<li>$1</li>")
      .replace(/\n\n/g, "<br><br>");
  }
}
