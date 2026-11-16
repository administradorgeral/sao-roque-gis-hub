/**
 * Módulo: Painel Flutuante de Camadas (Floating Layer Card)
 * Padrão Imersivo Moderno (Mapbox / Google Earth / Felt)
 * Totalmente Desacoplado, Reutilizável e Acessível (WCAG 2.1 AA)
 */

export class FloatingPanel {
  constructor(map, options = {}) {
    this.map = map;
    this.panel = document.querySelector(options.panelSelector || "#floating-layers-panel");
    this.closeBtn = document.querySelector(options.closeBtnSelector || "#btn-panel-close");
    this.backdrop = document.querySelector(options.backdropSelector || "#panel-backdrop");
    this.onStateChange = options.onStateChange || null;

    this.initEvents();

    this.close();
  }

  isMobile() {
    return window.innerWidth <= 768;
  }

  isOpen() {
    return this.panel ? !this.panel.classList.contains("panel-closed") : false;
  }

  initEvents() {
    if (this.closeBtn) {
      this.closeBtn.addEventListener("click", () => this.close());
    }

    if (this.backdrop) {
      this.backdrop.addEventListener("click", () => this.close());
    }

    // Tecla Escape fecha o painel
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && this.isOpen()) {
        this.close();
      }
    });

    // Ajusta comportamento no redimensionamento da janela
    window.addEventListener("resize", () => {
      if (this.backdrop) {
        if (!this.isMobile()) {
          this.backdrop.classList.remove("active");
        } else if (this.isOpen()) {
          this.backdrop.classList.add("active");
        }
      }
    });
  }

  open() {
    if (!this.panel) return;
    this.panel.classList.remove("panel-closed");
    this.panel.setAttribute("aria-hidden", "false");

    if (this.backdrop && this.isMobile()) {
      this.backdrop.classList.add("active");
    }

    if (this.onStateChange) this.onStateChange(true);
  }

  close() {
    if (!this.panel) return;
    this.panel.classList.add("panel-closed");
    this.panel.setAttribute("aria-hidden", "true");

    if (this.backdrop) {
      this.backdrop.classList.remove("active");
    }

    if (this.onStateChange) this.onStateChange(false);
  }

  toggle() {
    if (this.isOpen()) {
      this.close();
    } else {
      this.open();
    }
  }
}
