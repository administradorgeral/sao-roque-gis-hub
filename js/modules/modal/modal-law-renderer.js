/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · RENDERIZADOR DE LEGISLAÇÃO E PIRÂMIDE DE KELSEN
 * ===============================================================================
 * Renderiza modal especializado para:
 *  - Ementa, Objeto e Vigência de Normas Jurídicas
 *  - Enquadramento na Pirâmide de Kelsen (Federal > Estadual > Municipal)
 *  - Links para Repositório Oficial do Poder Público
 * ===============================================================================
 */

export class ModalLawRenderer {
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

  render(law) {
    if (!law) return null;

    const modalTitle = `${law.tipo} nº ${law.numero}/${law.ano}`;
    const container = document.createElement("div");
    container.className = "modal-legal-container";

    // 1. Cabeçalho com Esfera e Vigência
    const isVigente = law.ano <= 2026 && !String(law.tipo || "").toLowerCase().includes("minuta");
    const esferaBadgeClass = law.esfera_cat === "federal" 
      ? "dossier-badge-blue" 
      : (law.esfera_cat === "estadual" ? "dossier-badge-green" : "dossier-badge-purple");

    const headerCard = document.createElement("div");
    headerCard.className = "dossier-point-header";
    headerCard.innerHTML = `
      <div class="dossier-point-title" style="justify-content: space-between; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span>⚖️</span>
          <span>${this.escapeHTML(modalTitle)}</span>
        </div>
        <span class="dossier-badge ${esferaBadgeClass}" style="font-size: 0.72rem; padding: 3px 9px;">
          ${this.escapeHTML(law.esfera_label || "Legislação")}
        </span>
      </div>
      <div class="dossier-point-subtitle">
        Status Normativo: ${isVigente ? "🟢 Em Vigor / Direito Positivo Eficaz" : "🟡 Minuta / Proposta em Tramitação"}
      </div>
    `;
    container.appendChild(headerCard);

    // 2. Card: Ementa e Objeto
    const ementaCard = document.createElement("div");
    ementaCard.className = "dossier-card";
    ementaCard.innerHTML = `
      <div class="dossier-card-header">
        <span>📜</span>
        <span>Ementa & Objeto da Norma</span>
      </div>
      <div style="font-size: 0.8rem; line-height: 1.45; color: #1e293b; margin-bottom: 8px;">
        ${this.escapeHTML(law.ementa || "Sem ementa detalhada registrada.")}
      </div>
      <div class="dossier-grid-2">
        <div class="dossier-item"><strong>Âmbito Territorial:</strong><br>${this.escapeHTML(law.ambito_territorial || "Todo o Município")}</div>
        <div class="dossier-item"><strong>Zonas Afetadas:</strong><br>${this.escapeHTML((law.zonas_afetadas || []).join(", ") || "Todas as Zonas")}</div>
      </div>
    `;
    container.appendChild(ementaCard);

    // 3. Card: Posição na Pirâmide de Kelsen
    const kelsenCard = document.createElement("div");
    kelsenCard.className = "dossier-card";
    kelsenCard.innerHTML = `
      <div class="dossier-card-header">
        <span>🔺</span>
        <span>Precedência Normativa (Pirâmide de Kelsen)</span>
      </div>
      <div class="pyramid-banner" style="margin-bottom: 8px;">
        <strong>🔺 Hierarquia Federativa:</strong> Normas Federais fixam as diretrizes nacionais gerais (Art. 24 e 182 da CF/88); Leis Estaduais regulam matérias regionais e mananciais; e Leis Municipais suplementam no estrito interesse local (Art. 30 da CF/88).
      </div>
      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
        <span style="font-size: 0.74rem; color: #475569;">Repositório Oficial:</span>
        <a href="${this.escapeHTML(law.link_oficial || '#')}" target="_blank" rel="noopener noreferrer" class="btn-law-modal-link" style="font-size: 0.75rem; padding: 4px 10px;">
          Acessar Texto Integral Oficial ↗
        </a>
      </div>
    `;
    container.appendChild(kelsenCard);

    return {
      title: modalTitle,
      container
    };
  }
}
