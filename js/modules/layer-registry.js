/**
 * Módulo: Registro Dinâmico de Camadas
 * Permite carregar camadas de forma dinâmica a partir de configurações
 * e pastas, possibilitando adicionar/remover camadas sem modificar o código principal
 */

export class LayerRegistry {
  constructor(layerManager, attributeModal, opacityManager) {
    this.layerManager = layerManager;
    this.attributeModal = attributeModal;
    this.opacityManager = opacityManager;
    this.loadedLayers = new Set(); // Armazena IDs das camadas carregadas
  }

  /**
   * Carrega camadas a partir de um array de configurações
   * @param {Array} layerConfigs - Array de configurações de camadas
   * @param {Object} options - Opções de carregamento
   * @returns {Promise<Array>} Array de promessas de carregamento
   */
  async loadLayersFromConfig(layerConfigs, options = {}) {
    const { autoRegisterOpacity = true } = options;
    
    const loadPromises = [];

    for (const config of layerConfigs) {
      if (this.loadedLayers.has(config.id)) {
        console.log(`[LayerRegistry] Camada ${config.id} já carregada, pulando...`);
        continue;
      }

      const promise = this.loadLayer(config, { autoRegisterOpacity })
        .then(() => {
          this.loadedLayers.add(config.id);
          console.log(`[LayerRegistry] Camada ${config.id} carregada com sucesso`);
        })
        .catch(err => {
          console.error(`[LayerRegistry] Erro ao carregar camada ${config.id}:`, err);
        });

      loadPromises.push(promise);
    }

    return Promise.all(loadPromises);
  }

  /**
   * Carrega uma camada individual
   * @param {Object} config - Configuração da camada
   * @param {Object} options - Opções de carregamento
   * @returns {Promise}
   */
  async loadLayer(config, options = {}) {
    const { autoRegisterOpacity = true } = options;

    // 1. Registra a camada no LayerManager
    await this.layerManager.registerLayer(config);

    // 2. Carrega os dados GeoJSON
    const styleFn = this.createStyleFunction(config);
    await this.layerManager.loadGeoJSONLayer(config.id, config.url, styleFn);

    // 3. Configura o toggle de visibilidade
    this.setupVisibilityToggle(config);

    // 4. Configura o botão de enquadramento
    this.setupFitBoundsButton(config);

    // 5. Registra o controle de opacidade
    if (autoRegisterOpacity && this.opacityManager) {
      this.registerOpacityControl(config);
    }

    // 6. Aplica visibilidade inicial
    if (config.defaultVisible) {
      this.layerManager.setVisible(config.id, true);
    }
  }

  /**
   * Cria função de estilo para a camada
   * @param {Object} config - Configuração da camada
   * @returns {Function}
   */
  createStyleFunction(config) {
    if (typeof config.style === 'function') {
      return config.style;
    }
    return (feature) => {
      // Cor padrão da configuração ou cor da feature
      const color = feature.properties?.cor_hex || feature.properties?.cor || config.cor || config.defaultColor || "#2563eb";
      const weight = config.weight || 2;
      const opacity = config.defaultOpacity || 1.0;
      
      return {
        color: color,
        weight: weight,
        fillColor: color,
        fillOpacity: opacity * 0.75, // 75% do valor padrão
        opacity: 0.95
      };
    };
  }

  /**
   * Configura o toggle de visibilidade para a camada
   * @param {Object} config - Configuração da camada
   */
  setupVisibilityToggle(config) {
    // Tenta diferentes padrões de IDs
    const possibleIds = [
      `toggle-${config.id}`,
      `toggle-${config.id.replace(/_/g, '-')}`,
      `toggle-${config.id.replace(/pmd2006/g, '')}`
    ];
    
    let toggle = null;
    for (const id of possibleIds) {
      toggle = document.getElementById(id);
      if (toggle) break;
    }
    
    if (toggle && toggle instanceof HTMLInputElement) {
      toggle.checked = config.defaultVisible || false;
      toggle.addEventListener('change', (e) => {
        this.layerManager.setVisible(config.id, e.target.checked);
      });
    } else {
      console.warn(`[LayerRegistry] Toggle não encontrado para ${config.id}. IDs tentados: ${possibleIds.join(', ')}`);
    }
  }

  /**
   * Configura o botão de enquadramento para a camada
   * (Deprecated - botões de zoom foram removidos por solicitação do usuário)
   */
  setupFitBoundsButton(config) {
    // Botões de zoom foram removidos do design
    // Este método não faz nada
  }

  /**
   * Registra o controle de opacidade para a camada
   * @param {Object} config - Configuração da camada
   */
  registerOpacityControl(config) {
    if (!this.opacityManager) return;
    
    // Tenta diferentes padrões de IDs
    const possibleIds = [
      `opacity-${config.id}`,
      `opacity-${config.id.replace(/_/g, '-')}`,
      `opacity-${config.id.replace(/pmd2006/g, '')}`
    ];
    
    let slider = null;
    for (const id of possibleIds) {
      slider = document.getElementById(id);
      if (slider) break;
    }
    
    if (slider) {
      const initialValue = config.defaultOpacity || 0.55;
      this.opacityManager.registerControl(config.id, slider, initialValue);
    } else {
      console.warn(`[LayerRegistry] Slider de opacidade não encontrado para ${config.id}`);
    }
  }

  /**
   * Remove uma camada do registro
   * @param {string} layerId - ID da camada
   */
  async unloadLayer(layerId) {
    if (!this.loadedLayers.has(layerId)) {
      console.warn(`[LayerRegistry] Camada ${layerId} não está carregada`);
      return;
    }

    // Remove do LayerManager
    // (Nota: LayerManager atualmente não tem método unregister)
    
    // Remove do OpacityManager
    if (this.opacityManager) {
      this.opacityManager.unregisterControl(layerId);
    }

    this.loadedLayers.delete(layerId);
    console.log(`[LayerRegistry] Camada ${layerId} removida`);
  }

  /**
   * Recarrega uma camada específica
   * @param {string} layerId - ID da camada
   * @param {Object} newConfig - Nova configuração (opcional)
   */
  async reloadLayer(layerId, newConfig = null) {
    const config = newConfig || this.getLayerConfig(layerId);
    if (!config) {
      console.warn(`[LayerRegistry] Configuração não encontrada para ${layerId}`);
      return;
    }

    // Remove a camada atual
    await this.unloadLayer(layerId);
    
    // Recarrega
    await this.loadLayer(config);
  }

  /**
   * Obtém a configuração de uma camada pelo ID
   * @param {string} layerId - ID da camada
   * @returns {Object|null}
   */
  getLayerConfig(layerId) {
    // Precisaria de acesso ao config original
    // Por enquanto, retorna null
    return null;
  }

  /**
   * Verifica se uma camada está carregada
   * @param {string} layerId - ID da camada
   * @returns {boolean}
   */
  isLoaded(layerId) {
    return this.loadedLayers.has(layerId);
  }

  /**
   * Obtém todas as camadas carregadas
   * @returns {Set}
   */
  getLoadedLayers() {
    return new Set(this.loadedLayers);
  }

  /**
   * Limpa todas as camadas carregadas
   */
  async clearAll() {
    const layersToRemove = Array.from(this.loadedLayers);
    for (const layerId of layersToRemove) {
      await this.unloadLayer(layerId);
    }
  }
}
