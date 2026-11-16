/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · RENDERIZADOR DE ATRIBUTOS E ELEMENTOS TERRITORIAIS
 * ===============================================================================
 * Renderiza cards especializados para:
 *  - Obras Estruturantes da Carta XIII (SRQ-01 a SRQ-22)
 *  - Vias e Logradouros Municipais
 *  - Classes de Solo (Pedologia) e Subsolo (Geologia)
 *  - Tabela Limpa de Atributos Cadastrais (sem FIDs numéricos)
 * ===============================================================================
 */

export class ModalFeatureRenderer {
  constructor(escapeHTMLFn) {
    this.escapeHTML = escapeHTMLFn || ((str) => {
      if (str == null) return "";
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    });
  }

  render(titulo, propriedades = {}) {
    let displayTitle = typeof titulo === "string" ? titulo : "";
    if (!displayTitle || /^fid\b/i.test(displayTitle.trim()) || /^\d+$/.test(displayTitle.trim())) {
      displayTitle = propriedades.denominacao || propriedades.nome_classe || propriedades.nome || propriedades.classe || "Elemento Territorial Oficial";
    }

    const container = document.createElement("div");
    container.className = "modal-legal-container";

    const pKeys = Object.keys(propriedades).map((k) => k.toLowerCase());
    const isObra = (propriedades.codigo && String(propriedades.codigo).startsWith("SRQ-")) || displayTitle.includes("SRQ-");
    const isVia = propriedades.tipo_via || propriedades.cod_logradouro || (propriedades.denominacao && pKeys.includes("tipo_via"));
    const isSolo = propriedades.macroclasse || (propriedades.classe && pKeys.includes("textura"));
    const isGeol = propriedades.litologia || propriedades["Litologia Principal"];

    if (isObra) {
      const cod = propriedades.codigo || "SRQ-XX";
      const nomeObra = propriedades.nome || displayTitle;
      const localObra = propriedades.local || propriedades.bairro || "São Roque";
      const descObra = propriedades.descricao || propriedades.justificativa || "Intervenção prioritária do Plano Diretor.";

      const obraCard = document.createElement("div");
      obraCard.className = "dossier-card";
      obraCard.style.borderLeft = "4px solid #d97706";
      obraCard.innerHTML = `
        <div class="dossier-card-header" style="justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span>🏗️</span>
            <span>Intervenção Prioritária (Carta XIII - PD 2026)</span>
          </div>
          <span class="dossier-badge dossier-badge-amber">${this.escapeHTML(cod)}</span>
        </div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #1e293b; margin-bottom: 6px;">
          ${this.escapeHTML(nomeObra)}
        </div>
        <div style="font-size: 0.75rem; color: #64748b; margin-bottom: 8px;">
          <strong>Local / Influência:</strong> ${this.escapeHTML(localObra)}
        </div>
        <div style="font-size: 0.78rem; line-height: 1.45; color: #334155; margin-bottom: 10px;">
          ${this.escapeHTML(descObra)}
        </div>
        <div class="modal-subcard" style="font-size: 0.72rem; color: #475569;">
          <strong>Vínculo Normativo:</strong> Mapeada na Carta XIII da Minuta de Revisão 2026 como intervenção pública estruturante de drenagem, mobilidade ou equipamento social.
        </div>
      `;
      container.appendChild(obraCard);
    } else if (isVia) {
      const nomeVia = propriedades.denominacao || propriedades.nome || displayTitle;
      const tipoVia = propriedades.tipo_via || "Via Pública";
      const bairro = propriedades.bairro || "Distrito Sede";

      const viaCard = document.createElement("div");
      viaCard.className = "dossier-card";
      viaCard.innerHTML = `
        <div class="dossier-card-header">
          <span>🛣️</span>
          <span>Eixo do Sistema Viário Oficial de São Roque</span>
        </div>
        <div style="font-size: 0.92rem; font-weight: 700; color: #1e3a8a; margin-bottom: 6px;">
          ${this.escapeHTML(nomeVia)}
        </div>
        <div class="dossier-grid-2">
          <div class="dossier-item"><strong>Tipologia Viária:</strong><br><span class="dossier-badge dossier-badge-blue">${this.escapeHTML(tipoVia)}</span></div>
          <div class="dossier-item"><strong>Bairro / Setor:</strong><br>${this.escapeHTML(bairro)}</div>
        </div>
        <div class="modal-subcard" style="margin-top: 8px; font-size: 0.72rem;">
          <strong>Conexão Multicamadas:</strong> Eixo viário integrado à malha cadastral municipal, cruzando parâmetros da LC 40/2006 e diretrizes viárias das Cartas X, XI e XII (2026).
        </div>
      `;
      container.appendChild(viaCard);
    } else if (isSolo || isGeol) {
      const titleGeo = isSolo ? "🌱 Ficha Pedológica (Solos)" : "⛰️ Ficha Geotécnica do Subsolo";
      const classeNome = propriedades.nome_classe || propriedades.classe || displayTitle;
      const textGeol = propriedades.textura || propriedades.permeabilidade || propriedades.litologia || "Formação territorial regional.";

      const geoCard = document.createElement("div");
      geoCard.className = "dossier-card";
      geoCard.innerHTML = `
        <div class="dossier-card-header">
          <span>${isSolo ? "🌱" : "⛰️"}</span>
          <span>${titleGeo}</span>
        </div>
        <div style="font-size: 0.9rem; font-weight: 700; color: #1e293b; margin-bottom: 6px;">
          ${this.escapeHTML(classeNome)}
        </div>
        <div style="font-size: 0.76rem; color: #475569; line-height: 1.4; margin-bottom: 8px;">
          ${this.escapeHTML(textGeol)}
        </div>
        ${propriedades.implicacao_obras ? `
          <div class="modal-subcard" style="font-size: 0.72rem;">
            <strong>Aptidão Construtiva & Drenagem:</strong> ${this.escapeHTML(propriedades.implicacao_obras)}
          </div>
        ` : ""}
      `;
      container.appendChild(geoCard);
    }

    // Tabela Limpa de Atributos Cadastrais
    const filteredEntries = Object.entries(propriedades).filter(([key]) => {
      const kLower = key.toLowerCase();
      return !["cor", "id", "style", "fid", "descricao", "justificativa"].includes(kLower) && !kLower.startsWith("fid_");
    });

    if (filteredEntries.length > 0) {
      const attrCard = document.createElement("div");
      attrCard.className = "dossier-card";
      attrCard.innerHTML = `
        <div class="dossier-card-header">
          <span>📋</span>
          <span>Metadados Cadastrais & Cartográficos Oficiais</span>
        </div>
      `;
      const attrList = document.createElement("div");
      attrList.style.display = "flex";
      attrList.style.flexDirection = "column";
      attrList.style.gap = "4px";

      filteredEntries.forEach(([key, val]) => {
        const row = document.createElement("div");
        row.className = "modal-row";
        row.innerHTML = `
          <span class="modal-row-label">${this.escapeHTML(key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()))}</span>
          <span class="modal-row-val">${this.escapeHTML(typeof val === "object" ? JSON.stringify(val) : String(val ?? "—"))}</span>
        `;
        attrList.appendChild(row);
      });
      attrCard.appendChild(attrList);
      container.appendChild(attrCard);
    }

    return {
      title: displayTitle,
      container
    };
  }
}
