/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · RENDERIZADOR DE ZONEAMENTO E ARTIGOS DE LEI
 * ===============================================================================
 * Renderiza modal especializado para:
 *  - Zoneamento Homologado Vigente (LC 40/2006 & LC 39/2006)
 *  - Índices Urbanísticos (Taxa de Ocupação, Coef. Aproveitamento, Gabarito, Lote Mínimo)
 *  - Confronto com Minuta de Revisão 2026
 *  - Rol Hierárquico de Leis Aplicáveis pela Pirâmide de Kelsen
 * ===============================================================================
 */

export class ModalZoneRenderer {
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

  render(titulo, propriedades = {}, legalContext = null) {
    let displayTitle = titulo;
    if (!displayTitle || /^fid\b/i.test(displayTitle.trim()) || /^\d+$/.test(displayTitle.trim())) {
      displayTitle = propriedades.denominacao || propriedades.nome || legalContext?.parametros?.nome || "Zoneamento Municipal";
    }

    const container = document.createElement("div");
    container.className = "modal-legal-container";

    const params = legalContext?.parametros;
    const applicableLaws = legalContext?.leis_aplicaveis || [];

    // 1. Cabeçalho da Zona e Categoria
    if (params) {
      const headerBox = document.createElement("div");
      headerBox.className = "modal-zone-highlight";
      headerBox.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;">
          <div>
            <strong style="font-size: 0.95rem; color: #1e3a8a;">${this.escapeHTML(params.nome)}</strong>
            <div style="font-size: 0.74rem; color: #475569;">Categoria: ${this.escapeHTML(params.categoria)}</div>
          </div>
          <span class="dossier-badge dossier-badge-blue">Código: ${this.escapeHTML(params.codigo)}</span>
        </div>
      `;
      container.appendChild(headerBox);

      // 2. Grid de Índices Urbanísticos Oficiais Vigentes (LC 40/2006)
      const paramsTitle = document.createElement("div");
      paramsTitle.className = "modal-section-title";
      paramsTitle.textContent = "🏛️ Regime Vigente: Parâmetros Urbanísticos (LC 40/2006 & LC 39/2006)";
      container.appendChild(paramsTitle);

      const grid = document.createElement("div");
      grid.className = "urban-params-grid";
      grid.innerHTML = `
        <div class="urban-param-card">
          <span class="urban-param-label">Taxa de Ocupação Vigente</span>
          <span class="urban-param-val">${this.escapeHTML(params.taxa_ocupacao || "—")}</span>
        </div>
        <div class="urban-param-card">
          <span class="urban-param-label">Coef. Aproveitamento</span>
          <span class="urban-param-val">${this.escapeHTML(params.coeficiente_aproveitamento || "—")}</span>
        </div>
        <div class="urban-param-card">
          <span class="urban-param-label">Gabarito Máximo</span>
          <span class="urban-param-val">${this.escapeHTML(params.gabarito_altura || "—")}</span>
        </div>
        <div class="urban-param-card">
          <span class="urban-param-label">Lote Mínimo Vigente</span>
          <span class="urban-param-val">${this.escapeHTML(params.lote_minimo || "—")}</span>
        </div>
      `;
      container.appendChild(grid);

      if (params.recuos) {
        const recuoRow = document.createElement("div");
        recuoRow.className = "modal-subcard";
        recuoRow.innerHTML = `<strong>Recuos Mínimos Vigentes:</strong> <span>${this.escapeHTML(params.recuos)}</span>`;
        container.appendChild(recuoRow);
      }

      if (params.usos_admitidos && params.usos_admitidos !== "—") {
        const usosRow = document.createElement("div");
        usosRow.className = "modal-subcard";
        usosRow.innerHTML = `<strong>Usos Admitidos:</strong> <span>${this.escapeHTML(params.usos_admitidos)}</span>`;
        container.appendChild(usosRow);
      }

      if (params.restricoes && params.restricoes !== "—") {
        const restRow = document.createElement("div");
        restRow.className = "modal-subcard subcard-warning";
        restRow.innerHTML = `<strong>Restrições & Vetos Legais:</strong> <span>${this.escapeHTML(params.restricoes)}</span>`;
        container.appendChild(restRow);
      }

      // 2.1 Card de Confronto com a Proposta de Revisão (Plano Diretor 2026)
      const revisaoCard = document.createElement("div");
      revisaoCard.className = "dossier-card";
      revisaoCard.style.borderLeft = "4px solid #d97706";
      revisaoCard.style.marginTop = "10px";
      revisaoCard.innerHTML = `
        <div class="dossier-card-header" style="justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span>📋</span>
            <span>Regime Proposto: Minutas de Revisão (LC 39 e 40) & Cartas 2026</span>
          </div>
          <span class="dossier-badge dossier-badge-amber">Em Tramitação</span>
        </div>
        <div style="font-size: 0.74rem; color: #334155; line-height: 1.4;">
          <strong>Referência na Minuta 2026:</strong> ${this.escapeHTML(params.lei_referencia || "Quadros I a IX da Minuta da nova LC 40")}
          <div style="margin-top: 4px; color: #475569;">
            A Proposta do Plano Diretor 2026 prevê novos parâmetros de adensamento controlado, exigência de taxa de permeabilidade mínima (50% a 55% em mananciais) e integração com as <strong>13 Cartas Oficiais</strong> e <strong>22 Obras Estruturantes da Carta XIII</strong>.
          </div>
        </div>
      `;
      container.appendChild(revisaoCard);
    }

    // 3. Rol de Leis Aplicáveis organizado pela Pirâmide de Kelsen
    const lawsTitle = document.createElement("div");
    lawsTitle.className = "modal-section-title";
    lawsTitle.style.marginTop = "14px";
    lawsTitle.textContent = `⚖️ Precedência das Leis Aplicáveis a este Local (${applicableLaws.length})`;
    container.appendChild(lawsTitle);

    const pyramidBanner = document.createElement("div");
    pyramidBanner.className = "pyramid-banner";
    pyramidBanner.innerHTML = `
      <strong>🔺 Pirâmide Normativa (Prevalência Automática):</strong><br>
      <span style="font-size: 0.72rem; color: #475569;">
        <strong>Federal</strong> (Normas Gerais) &gt; <strong>Estadual</strong> (Regional/Mananciais) &gt; <strong>Municipal</strong> (Uso Local).<br>
        A norma municipal suplementa o interesse local, prevalecendo sempre a regra de maior proteção ambiental e urbanística.
      </span>
    `;
    container.appendChild(pyramidBanner);

    if (applicableLaws.length > 0) {
      const federais = applicableLaws.filter((l) => l.esfera_cat === "federal" || l.tipo?.includes("Federal") || String(l.esfera_label || "").includes("Federal"));
      const estaduais = applicableLaws.filter((l) => l.esfera_cat === "estadual" || l.tipo?.includes("Estadual") || String(l.esfera_label || "").includes("Estadual"));
      const municipais = applicableLaws.filter((l) => l.esfera_cat === "municipal" || l.tipo?.includes("Municipal") || l.tipo?.includes("Complementar") || String(l.esfera_label || "").includes("Municipal"));

      const groups = [
        { title: "🔺 1. Esfera Federal (Teto Normativo e Parcelamento do Solo)", list: federais, color: "#1d4ed8" },
        { title: "🔺 2. Esfera Estadual (Condicionantes Regionais e Mananciais)", list: estaduais, color: "#059669" },
        { title: "🔺 3. Esfera Municipal (Zoneamento Local e Uso do Solo)", list: municipais, color: "#7c3aed" }
      ];

      const lawsList = document.createElement("div");
      lawsList.className = "modal-laws-list";

      groups.forEach((grp) => {
        if (grp.list.length === 0) return;

        const grpHeader = document.createElement("div");
        grpHeader.style.fontSize = "0.74rem";
        grpHeader.style.fontWeight = "700";
        grpHeader.style.color = grp.color;
        grpHeader.style.marginTop = "8px";
        grpHeader.style.marginBottom = "3px";
        grpHeader.textContent = grp.title;
        lawsList.appendChild(grpHeader);

        grp.list.slice(0, 5).forEach((law) => {
          const lawItem = document.createElement("div");
          lawItem.className = "modal-law-item";
          lawItem.style.borderLeftColor = grp.color;
          lawItem.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
              <div>
                <strong style="color: #1e293b; font-size: 0.82rem;">${this.escapeHTML(law.tipo)} nº ${this.escapeHTML(law.numero)}/${this.escapeHTML(String(law.ano))}</strong>
                <div style="font-size: 0.72rem; color: #64748b; margin-top: 2px;">
                  ${this.escapeHTML(law.tag_ambito || law.ambito_territorial || "Âmbito Territorial")}
                </div>
              </div>
              <a href="${this.escapeHTML(law.link_oficial)}" target="_blank" rel="noopener noreferrer" class="btn-law-modal-link" title="Abrir link oficial da norma">
                Oficial ↗
              </a>
            </div>
            <p style="font-size: 0.73rem; color: #334155; margin-top: 5px; line-height: 1.35;">
              ${this.escapeHTML(law.ementa || "")}
            </p>
          `;
          lawsList.appendChild(lawItem);
        });
      });

      container.appendChild(lawsList);
    }

    return {
      title: displayTitle,
      container
    };
  }
}
