/**
 * Módulo: Gerenciador Centralizado de Opacidade
 * Centraliza toda a programação de opacidade para camadas
 * Permite controle unificado e consistente de opacidade em todo o sistema
 */

export class OpacityManager {
  constructor(layerManager) {
    this.layerManager = layerManager;
    this.opacityControls = new Map(); // layerId -> { slider: HTMLElement, currentValue: number }
    this.defaultOpacity = 0.75;
    this.opacityMultiplier = 0.65; // Multiplicador para fillOpacity em camadas GeoJSON
  }

  /**
   * Registra um controle de opacidade para uma camada
   * @param {string} layerId - ID da camada
   * @param {HTMLElement} sliderElement - Elemento input range do slider
   * @param {number} initialValue - Valor inicial de opacidade (0-1)
   */
  registerControl(layerId, sliderElement, initialValue = this.defaultOpacity) {
    if (!sliderElement || !(sliderElement instanceof HTMLElement)) {
      console.warn(`[OpacityManager] Slider element inválido para camada ${layerId}`);
      return;
    }

    // Armazena o controle
    this.opacityControls.set(layerId, {
      slider: sliderElement,
      currentValue: initialValue
    });

    // Sincroniza o valor inicial
    sliderElement.value = initialValue;

    // Adiciona listener para atualizar opacidade quando o slider mudar
    sliderElement.addEventListener('input', (e) => {
      const value = parseFloat(e.target.value);
      this.setOpacity(layerId, value);
    });

    // Aplica o valor inicial
    this.setOpacity(layerId, initialValue);

    console.log(`[OpacityManager] Controle de opacidade registrado para ${layerId}`);
  }

  /**
   * Define a opacidade para uma camada específica
   * @param {string} layerId - ID da camada
   * @param {number} opacity - Valor de opacidade (0-1)
   */
  setOpacity(layerId, opacity) {
    // Validação
    opacity = Math.max(0, Math.min(1, opacity));

    // Atualiza o valor corrente no controle
    const control = this.opacityControls.get(layerId);
    if (control) {
      control.currentValue = opacity;
    }

    // Delega para o LayerManager
    if (this.layerManager && typeof this.layerManager.setOpacity === 'function') {
      this.layerManager.setOpacity(layerId, opacity);
    }
  }

  /**
   * Obtém a opacidade atual de uma camada
   * @param {string} layerId - ID da camada
   * @returns {number} Valor de opacidade (0-1)
   */
  getOpacity(layerId) {
    const control = this.opacityControls.get(layerId);
    return control ? control.currentValue : this.defaultOpacity;
  }

  /**
   * Define a opacidade para todas as camadas visíveis
   * @param {number} opacity - Valor de opacidade (0-1)
   */
  setGlobalOpacity(opacity) {
    opacity = Math.max(0, Math.min(1, opacity));
    for (const [layerId] of this.opacityControls) {
      this.setOpacity(layerId, opacity);
    }
  }

  /**
   * Reseta a opacidade de todas as camadas para o valor padrão
   */
  resetAll() {
    for (const [layerId] of this.opacityControls) {
      this.setOpacity(layerId, this.defaultOpacity);
    }
  }

  /**
   * Remove um controle de opacidade
   * @param {string} layerId - ID da camada
   */
  unregisterControl(layerId) {
    const control = this.opacityControls.get(layerId);
    if (control && control.slider) {
      // Remove listeners - não possível remover addEventListener anônimo
      // então apenas removemos da lista
      this.opacityControls.delete(layerId);
    }
  }

  /**
   * Destrói todos os controles de opacidade
   */
  destroy() {
    this.opacityControls.clear();
  }

  /**
   * Criar um grupo de controles de opacidade a partir de configurações
   * @param {Array} layerConfigs - Array de configurações de camadas
   */
  createControlsFromConfig(layerConfigs) {
    layerConfigs.forEach(config => {
      const sliderId = `opacity-${config.id}`;
      const slider = document.getElementById(sliderId);
      if (slider) {
        this.registerControl(config.id, slider, config.defaultOpacity || this.defaultOpacity);
      }
    });
  }
}
