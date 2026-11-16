/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · ORQUESTRADOR MODULAR DE MODAIS E ATRIBUTOS
 * ===============================================================================
 * Módulo Desacoplado de Interface (UI Modal Orchestrator)
 * 
 * Gerencia a abertura, acessibilidade (ARIA), foco e fechamento do modal principal,
 * delegando a renderização para submódulos especializados:
 *  - ModalFeatureRenderer: Atributos gerais, obras, vias e solos.
 *  - ModalLawRenderer: Ficha de leis e precedência na Pirâmide de Kelsen.
 *  - ModalZoneRenderer: Zoneamento LC 40/06, parâmetros e minuta 2026.
 *  - ModalDossierRenderer: Dossiê topológico multicamadas do ponto territorial.
 * ===============================================================================
 */

import { ModalFeatureRenderer } from "./modal/modal-feature-renderer.js";
import { ModalLawRenderer } from "./modal/modal-law-renderer.js";
import { ModalZoneRenderer } from "./modal/modal-zone-renderer.js";
import { ModalDossierRenderer } from "./modal/modal-dossier-renderer.js";

export class AttributeModal {
  constructor(modalId = "feature-modal", titleId = "modal-title", bodyId = "modal-body", closeId = "modal-close") {
    this.modalEl = document.getElementById(modalId);
    this.titleEl = document.getElementById(titleId);
    this.bodyEl = document.getElementById(bodyId);
    this.closeEl = document.getElementById(closeId);

    // Instanciação dos Renderizadores Desacoplados
    this.featureRenderer = new ModalFeatureRenderer((s) => this.escapeHTML(s));
    this.lawRenderer = new ModalLawRenderer((s) => this.escapeHTML(s));
    this.zoneRenderer = new ModalZoneRenderer((s) => this.escapeHTML(s));
    this.dossierRenderer = new ModalDossierRenderer((s) => this.escapeHTML(s));

    this.initEvents();
  }

  escapeHTML(str) {
    if (str == null) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  initEvents() {
    if (this.closeEl) {
      this.closeEl.addEventListener("click", () => this.close());
    }

    if (this.modalEl) {
      this.modalEl.addEventListener("click", (e) => {
        if (e.target === this.modalEl) {
          this.close();
        }
      });
    }

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.isOpen()) {
        this.close();
      }
    });
  }

  isOpen() {
    return this.modalEl?.getAttribute("aria-hidden") === "false";
  }

  open() {
    if (this.modalEl) {
      this.modalEl.setAttribute("aria-hidden", "false");
      if (this.closeEl) this.closeEl.focus();
    }
  }

  close() {
    if (this.modalEl) {
      this.modalEl.setAttribute("aria-hidden", "true");
    }
  }

  hide() {
    this.close();
  }

  /**
   * Renderiza atributos de um elemento ou camada cartográfica
   */
  show(titulo, propriedades = {}) {
    if (!this.modalEl || !this.titleEl || !this.bodyEl) return;

    // Suporte a chamada com objeto de conteúdo { title, content } ou { title, html }
    if (typeof titulo === "object" && titulo !== null) {
      if (titulo.content || titulo.html) {
        this.titleEl.textContent = titulo.title || "Detalhes do Elemento";
        this.bodyEl.innerHTML = titulo.content || titulo.html;
        this.open();
        return;
      }
      propriedades = titulo;
      titulo = propriedades.denominacao || propriedades.nome || propriedades.title || "Detalhes do Elemento";
    }

    const { title, container } = this.featureRenderer.render(titulo, propriedades);
    this.titleEl.textContent = title;
    this.bodyEl.innerHTML = "";
    this.bodyEl.appendChild(container);
    this.open();
  }

  /**
   * Exibe o Dossiê Especializado de uma Norma Jurídica do Catálogo
   */
  showLawDetails(law) {
    if (!this.modalEl || !this.titleEl || !this.bodyEl || !law) return;

    const res = this.lawRenderer.render(law);
    if (!res) return;

    this.titleEl.textContent = res.title;
    this.bodyEl.innerHTML = "";
    this.bodyEl.appendChild(res.container);
    this.open();
  }

  /**
   * Exibe a ficha completa com metadados urbanísticos e rol de leis aplicáveis ao ponto clicado
   */
  showZoneLegalDetails(titulo, propriedades = {}, legalContext = null) {
    if (!this.modalEl || !this.titleEl || !this.bodyEl) return;

    const { title, container } = this.zoneRenderer.render(titulo, propriedades, legalContext);
    this.titleEl.textContent = title;
    this.bodyEl.innerHTML = "";
    this.bodyEl.appendChild(container);
    this.open();
  }

  /**
   * Exibe o Dossiê Topológico Multicamadas Integral do Ponto Selecionado
   */
  showMultiLayerDossier(dossier, legalContext = null) {
    if (!this.modalEl || !this.titleEl || !this.bodyEl || !dossier) return;

    const res = this.dossierRenderer.render(dossier, legalContext);
    if (!res) return;

    this.titleEl.textContent = res.title;
    this.bodyEl.innerHTML = "";
    this.bodyEl.appendChild(res.container);
    this.open();
  }

  /**
   * Permite renderização controlada de fragmentos HTML confiáveis
   */
  setContentHTML(htmlString) {
    if (!this.bodyEl) return;
    this.bodyEl.innerHTML = htmlString;
  }
}
