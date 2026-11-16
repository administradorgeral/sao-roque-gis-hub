/**
 * Módulo: Catálogo de Legislação e Inteligência Territorial
 * São Roque GIS Hub (Código IBGE: 3550605)
 * Gerencia o Rol de Leis, Âmbito Territorial e Metadados para Clique no Mapa
 */

export class LegislationCatalog {
  constructor(attributeModal) {
    this.attributeModal = attributeModal;
    this.data = null;
    this.currentSphere = "todas";
    this.searchQuery = "";

    // Mapeamento normalizado entre as nomenclaturas das camadas, siglas e os códigos do banco
    this.zoneCodeMap = {
      // 2006 Vigente & Equivalências
      "Central": "ZUR_CENTRAL",
      "ZUC": "ZUR_CENTRAL",
      "ZUR_CENTRAL": "ZUR_CENTRAL",
      "Zona Urbana Central": "ZUR_CENTRAL",
      "Consolidação urbana": "MACROZONA_CONSOLIDACAO",
      "ZCU": "MACROZONA_CONSOLIDACAO",
      "MACROZONA_CONSOLIDACAO": "MACROZONA_CONSOLIDACAO",
      "Zona de Consolidação Urbana": "MACROZONA_CONSOLIDACAO",
      "Densidade Alta": "ZUR_ALTA",
      "ZUR-ad": "ZUR_ALTA",
      "ZUR_ALTA": "ZUR_ALTA",
      "Densidade Media": "ZUR_MEDIA",
      "Densidade Média": "ZUR_MEDIA",
      "ZUR-md": "ZUR_MEDIA",
      "ZUR_MEDIA": "ZUR_MEDIA",
      "Densidade Baixa": "ZUR_BAIXA",
      "ZUR-bd": "ZUR_BAIXA",
      "ZUR_BAIXA": "ZUR_BAIXA",
      "Industrial": "ZUR_INDUSTRIAL",
      "ZUI": "ZUR_INDUSTRIAL",
      "ZUR_INDUSTRIAL": "ZUR_INDUSTRIAL",
      "Preservação": "ZUR_ZUPA",
      "ZUPA": "ZUR_ZUPA",
      "ZUR_ZUPA": "ZUR_ZUPA",
      "Rural": "MACROZONA_RURAL",
      "ZR": "MACROZONA_RURAL",
      "MACROZONA_RURAL": "MACROZONA_RURAL",
      "ZUCAer": "ZUCAer",

      // Proposta Revisão 2026 (ZUEs e Corredores das Cartas Oficiais)
      "ZUE": "MACROZONA_ZUE",
      "MACROZONA_ZUE": "MACROZONA_ZUE",
      "ZUE-Chacaras em Manancial": "ZUE_MANANCIAL",
      "ZUE - Chácaras em Manancial": "ZUE_MANANCIAL",
      "ZUE-CM": "ZUE_MANANCIAL",
      "ZUE_MANANCIAL": "ZUE_MANANCIAL",
      "ZUE-Desenvolvimento Turistico": "ZUE_TURISTICO",
      "ZUE - Desenvolvimento Turístico": "ZUE_TURISTICO",
      "ZUE - Interesse Turístico": "ZUE_TURISTICO",
      "ZUE-DT": "ZUE_TURISTICO",
      "ZUE_TURISTICO": "ZUE_TURISTICO",
      "ZUE-Desenvolvimento Econômico": "ZUE_DESENV_ECON",
      "ZUE - Desenvolvimento Econômico": "ZUE_DESENV_ECON",
      "ZUE-DE": "ZUE_DESENV_ECON",
      "ZUE_DESENV_ECON": "ZUE_DESENV_ECON",
      "ZUE-Ocupação Estratégica": "ZUE_OCUP_ESTRATEGICA",
      "ZUE - Ocupação Estratégica": "ZUE_OCUP_ESTRATEGICA",
      "ZUE-OE": "ZUE_OCUP_ESTRATEGICA",
      "ZUE_OCUP_ESTRATEGICA": "ZUE_OCUP_ESTRATEGICA",
      "ZUE_MOMBACA": "ZUE_MOMBACA",
      "Mombaça": "ZUE_MOMBACA",
      "ZUE_RAPOSO": "ZUE_RAPOSO",
      "ZUCL": "ZUCL_CORREDOR",
      "ZUCL_CORREDOR": "ZUCL_CORREDOR",
      "Corredor Logístico": "ZUCL_CORREDOR",

      // Elementos Físicos, APA, Obras e Distritos
      "PVA": "PVA19",
      "PVA19": "PVA19",
      "LVA": "LVA17",
      "LVA17": "LVA17",
      "APA": "PERIMETRO_APA_ITUPARARANGA",
      "APA_ITUPARARANGA": "PERIMETRO_APA_ITUPARARANGA",
      "PERIMETRO_APA_ITUPARARANGA": "PERIMETRO_APA_ITUPARARANGA",
      "SRQ_OBRAS": "SRQ_OBRAS",
      "GRANITO_IBIUNA": "GEOL_GRANITO_IBIUNA",
      "GEOL_GRANITO_IBIUNA": "GEOL_GRANITO_IBIUNA",
      "CANGUERA": "DISTRITO_CANGUERA",
      "MAILASQUI": "DISTRITO_MAILASQUI",
      "MAYLASKY": "DISTRITO_MAILASQUI",
      "SAO_JOAO_NOVO": "DISTRITO_SAO_JOAO_NOVO",
      "SEDE": "DISTRITO_SAO_ROQUE"
    };
  }

  async init() {
    try {
      const response = await fetch(`data/rol_legislacao_territorial.json?v=${Date.now()}`);
      if (!response.ok) throw new Error(`HTTP ${response.status} ao carregar rol de legislação`);
      this.data = await response.json();
      console.log(`[LegislationCatalog] ${this.data.total_leis_catalogo} leis carregadas com sucesso.`);
    } catch (err) {
      console.warn("[LegislationCatalog] Falha ao carregar catálogo de leis, usando fallback:", err);
      this.data = { leis: { municipal: [], estadual: [], federal: [] }, zonas_parametros: {} };
    }

    this.initTabs();
    this.initSearchAndFilters();
    this.renderLaws();
  }

  initTabs() {
    const tabMapas = document.getElementById("tab-btn-mapas");
    const tabLeis = document.getElementById("tab-btn-leis");
    const tabAi = document.getElementById("tab-btn-ai");
    const paneMapas = document.getElementById("tab-pane-mapas");
    const paneLeis = document.getElementById("tab-pane-leis");
    const paneAi = document.getElementById("tab-pane-ai");

    if (!tabMapas || !tabLeis || !paneMapas || !paneLeis) return;

    const deactivateAll = () => {
      [tabMapas, tabLeis, tabAi].forEach(t => {
        if (t) {
          t.classList.remove("active");
          t.setAttribute("aria-selected", "false");
        }
      });
      [paneMapas, paneLeis, paneAi].forEach(p => {
        if (p) {
          p.style.display = "none";
          p.classList.remove("active");
          p.setAttribute("aria-hidden", "true");
        }
      });
    };

    tabMapas.addEventListener("click", () => {
      deactivateAll();
      tabMapas.classList.add("active");
      tabMapas.setAttribute("aria-selected", "true");
      paneMapas.style.display = "block";
      paneMapas.classList.add("active");
      paneMapas.setAttribute("aria-hidden", "false");
    });

    tabLeis.addEventListener("click", () => {
      deactivateAll();
      tabLeis.classList.add("active");
      tabLeis.setAttribute("aria-selected", "true");
      paneLeis.style.display = "block";
      paneLeis.classList.add("active");
      paneLeis.setAttribute("aria-hidden", "false");

      // Foca no campo de busca se estiver vazio
      const searchInput = document.getElementById("law-search-input");
      if (searchInput && !searchInput.value) {
        searchInput.focus();
      }
    });
  }

  initSearchAndFilters() {
    const searchInput = document.getElementById("law-search-input");
    const clearBtn = document.getElementById("btn-clear-law-search");

    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.searchQuery = e.target.value.trim().toLowerCase();
        if (clearBtn) {
          clearBtn.style.display = this.searchQuery ? "block" : "none";
        }
        this.renderLaws();
      });
    }

    if (clearBtn && searchInput) {
      clearBtn.addEventListener("click", () => {
        searchInput.value = "";
        this.searchQuery = "";
        clearBtn.style.display = "none";
        this.renderLaws();
        searchInput.focus();
      });
    }

    const filterChips = document.querySelectorAll(".law-filter-chip");
    filterChips.forEach((chip) => {
      chip.addEventListener("click", () => {
        filterChips.forEach((c) => {
          c.classList.remove("active");
          c.setAttribute("aria-checked", "false");
        });
        chip.classList.add("active");
        chip.setAttribute("aria-checked", "true");

        this.currentSphere = chip.getAttribute("data-sphere") || "todas";
        this.renderLaws();
      });
    });
  }

  getAllLaws() {
    if (!this.data || !this.data.leis) return [];
    const { municipal = [], estadual = [], federal = [] } = this.data.leis;
    // Ordenação estrita pela Pirâmide de Kelsen: Federal > Estadual > Municipal
    return [
      ...federal.map((l) => ({ ...l, esfera_cat: "federal", esfera_label: "🔺 1. Federal (Teto Normativo)", hierarquia_ordem: 1 })),
      ...estadual.map((l) => ({ ...l, esfera_cat: "estadual", esfera_label: "🔺 2. Estadual / SP (Regional)", hierarquia_ordem: 2 })),
      ...municipal.map((l) => ({ ...l, esfera_cat: "municipal", esfera_label: "🔺 3. Municipal / São Roque (Local)", hierarquia_ordem: 3 }))
    ];
  }

  renderLaws() {
    const container = document.getElementById("laws-list-container");
    const countBadge = document.getElementById("laws-count-badge");
    if (!container) return;

    const all = this.getAllLaws();
    const filtered = all.filter((law) => {
      // Filtro por esfera
      if (this.currentSphere !== "todas" && law.esfera_cat !== this.currentSphere) {
        return false;
      }
      // Filtro por busca textual
      if (this.searchQuery) {
        const textToMatch = [
          law.tipo,
          law.numero,
          law.ano,
          law.ementa,
          law.ambito_territorial,
          law.tag_ambito,
          ...(law.zonas_afetadas || [])
        ].join(" ").toLowerCase();

        return textToMatch.includes(this.searchQuery);
      }
      return true;
    });

    if (countBadge) {
      countBadge.textContent = `${filtered.length} norma(s)`;
    }

    if (filtered.length === 0) {
      container.innerHTML = `
        <div class="empty-state-card" style="text-align: center; padding: 24px 12px;">
          🔍 <strong>Nenhuma lei encontrada</strong><br>
          <span style="font-size: 0.74rem; color: #64748b;">
            Tente outros termos como "recuo", "declividade", "gabarito", "manancial", "lotes" ou limpe a busca.
          </span>
        </div>
      `;
      return;
    }

    container.innerHTML = "";
    const fragment = document.createDocumentFragment();

    filtered.forEach((law) => {
      const card = document.createElement("div");
      card.className = "law-card";

      const badgeSphereClass =
        law.esfera_cat === "municipal"
          ? "badge-purple"
          : law.esfera_cat === "estadual"
          ? "badge-green"
          : "badge-blue";

      card.innerHTML = `
        <div class="law-card-top">
          <div class="law-card-header">
            <span class="badge-audit ${badgeSphereClass}">${law.esfera_label}</span>
            <span class="law-card-year">${law.ano}</span>
          </div>
          <h3 class="law-card-title">${law.tipo} nº ${law.numero}/${law.ano}</h3>
          
          <div class="law-card-ambito">
            <span class="law-badge-ambito" title="Recorte espacial em que a lei incide">
              ${law.tag_ambito || "🏛️ " + law.ambito_territorial}
            </span>
          </div>

          <p class="law-card-desc">${law.ementa || "Sem ementa cadastrada."}</p>
        </div>

        <div class="law-card-footer">
          <a href="${law.link_oficial}" target="_blank" rel="noopener noreferrer" class="btn-law-link" title="Acessar íntegra no portal oficial">
            🌐 Portal Oficial ↗
          </a>
          <button type="button" class="btn-law-details" data-law-id="${law.id}" title="Ver detalhes completos e artigos da norma">
            📄 Detalhes
          </button>
        </div>
      `;

      // Evento de detalhes
      const btnDetails = card.querySelector(".btn-law-details");
      if (btnDetails) {
        btnDetails.addEventListener("click", () => this.showLawDetails(law));
      }

      fragment.appendChild(card);
    });

    container.appendChild(fragment);
  }

  showLawDetails(law) {
    if (!this.attributeModal) return;

    if (typeof this.attributeModal.showLawDetails === "function") {
      this.attributeModal.showLawDetails(law);
      return;
    }

    const props = {
      "Diploma Legal": `${law.tipo} nº ${law.numero}/${law.ano}`,
      "Esfera Federativa": law.esfera_label,
      "Âmbito Territorial de Aplicação": law.ambito_territorial,
      "Zonas Territoriais Afetadas": (law.zonas_afetadas || []).join(", ") || "Todo o Município",
      "Ementa Oficial": law.ementa,
      "Link Oficial Pericial": law.link_oficial,
      "Repositório Local": `dados_oficiais/legislacao/${law.id}.md`
    };

    this.attributeModal.show(`${law.tipo} nº ${law.numero}/${law.ano}`, props);
  }

  /**
   * Retorna os metadados jurídicos e parâmetros urbanísticos completos
   * para qualquer ponto ou zona clicada no mapa de São Roque
   */
  getZoneLegalMetadata(zonaNameOrSigla) {
    if (!zonaNameOrSigla) return null;

    const zClean = String(zonaNameOrSigla).trim();
    // 1. Verificar mapeamento direto no dicionário
    let code = this.zoneCodeMap[zClean];

    // 2. Se não achou, buscar case-insensitive
    if (!code) {
      const zLower = zClean.toLowerCase();
      for (const [k, v] of Object.entries(this.zoneCodeMap)) {
        if (k.toLowerCase() === zLower) {
          code = v;
          break;
        }
      }
    }

    // 3. Se ainda não achou, verificar se o código direto existe em zonas_parametros
    if (!code && this.data?.zonas_parametros?.[zClean]) {
      code = zClean;
    }

    // 4. Se ainda não achou, buscar substring nos códigos
    if (!code && this.data?.zonas_parametros) {
      const zNorm = zClean.toUpperCase().replace(/[^A-Z0-9]/g, "_");
      for (const k of Object.keys(this.data.zonas_parametros)) {
        if (k === zNorm || k.includes(zNorm) || zNorm.includes(k)) {
          code = k;
          break;
        }
      }
    }

    const params = (code && this.data?.zonas_parametros?.[code]) ? this.data.zonas_parametros[code] : null;

    // Localiza leis que afetam esta zona ou o município inteiro
    const allLaws = this.getAllLaws();
    const applicableLaws = allLaws.filter((law) => {
      if (!law.zonas_afetadas) return false;
      const zStr = law.zonas_afetadas.join(" ").toLowerCase();
      return (
        zStr.includes("todo o município") ||
        zStr.includes("todas as zonas") ||
        zStr.includes("geral") ||
        (code && zStr.includes(code.toLowerCase())) ||
        (params && zStr.includes(params.nome.toLowerCase())) ||
        zStr.includes(zClean.toLowerCase())
      );
    });

    return {
      zona: zClean,
      codigo: code || zClean,
      parametros: params,
      leis_aplicaveis: applicableLaws
    };
  }
}
