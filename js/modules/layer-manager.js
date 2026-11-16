/**
 * Módulo: Gerenciador Desacoplado de Camadas (Layer Manager)
 * Controla a ingestão, renderização, opacidade e visibilidade de camadas oficiais
 */

export class LayerManager {
  constructor(map, attributeModal) {
    this.map = map;
    this.attributeModal = attributeModal;
    this.legislationCatalog = null;
    this.layers = new Map(); // id -> { config, leafletLayer, data }
    this.listeners = new Set();
  }

  setLegislationCatalog(legislationCatalog) {
    this.legislationCatalog = legislationCatalog;
  }

  /**
   * Registra e instancia uma nova camada oficial no sistema
   * @param {Object} layerConfig Configuração da camada com metadados
   */
  async registerLayer(layerConfig) {
    if (this.layers.has(layerConfig.id)) {
      console.warn(`[LayerManager] Camada ${layerConfig.id} já registrada.`);
      return this.layers.get(layerConfig.id);
    }

    const entry = {
      config: layerConfig,
      leafletLayer: null,
      data: null,
      visible: layerConfig.defaultVisible || false,
      opacity: layerConfig.defaultOpacity || 1.0
    };

    this.layers.set(layerConfig.id, entry);
    this.notifyListeners("registered", entry);
    return entry;
  }

  /**
   * Carrega os dados vetoriais de uma camada via GeoJSON
   */
  async loadGeoJSONLayer(layerId, geojsonUrl, styleFn, pointToLayerFn) {
    const entry = this.layers.get(layerId);
    if (!entry) throw new Error(`Camada ${layerId} não encontrada no registro.`);

    try {
      let geoLayer = null;
      if (geojsonUrl) {
        const response = await fetch(`${geojsonUrl}?v=${Date.now()}`);
        if (!response.ok) throw new Error(`HTTP ${response.status} ao carregar ${geojsonUrl}`);

        const data = await response.json();
        entry.data = data;

        geoLayer = L.geoJSON(data, {
          style: styleFn || { color: entry.config.cor || "#2563eb", weight: 2 },
          pointToLayer: pointToLayerFn || null,
          onEachFeature: (feature, layer) => {
            layer.on("click", (e) => {
              L.DomEvent.stopPropagation(e);
              const props = feature.properties || {};
              let rawName = props.nome || props.denominacao || props.nome_classe || props.classe || props.local;
              if (rawName && (/^fid\b/i.test(String(rawName).trim()) || /^\d+$/.test(String(rawName).trim()))) {
                rawName = props.denominacao || props.nome_classe || props.classe || entry.config.name;
              }
              const title = rawName || entry.config.name;
              const zonaKey = props.zona || props.sigla || props.denominacao;

              const catalog = this.legislationCatalog || window.GIS?.legislationCatalog;
              const legalContext = catalog ? catalog.getZoneLegalMetadata(zonaKey) : null;

              if (this.attributeModal) {
                if (legalContext && typeof this.attributeModal.showZoneLegalDetails === "function") {
                  this.attributeModal.showZoneLegalDetails(title, props, legalContext);
                } else {
                  this.attributeModal.show(title, props);
                }
              }
            });
          }
        });
      }

      if (entry.config.rasterUrl && entry.config.rasterBounds) {
        const rasterLayer = L.imageOverlay(entry.config.rasterUrl, entry.config.rasterBounds, {
          opacity: entry.opacity || 0.70,
          interactive: false
        });
        entry.leafletLayer = geoLayer ? L.layerGroup([rasterLayer, geoLayer]) : rasterLayer;
      } else if (geoLayer) {
        entry.leafletLayer = geoLayer;
      }

      if (entry.visible && entry.leafletLayer) {
        entry.leafletLayer.addTo(this.map);
      }

      this.notifyListeners("loaded", entry);
      return entry;
    } catch (err) {
      console.error(`[LayerManager] Erro ao carregar GeoJSON da camada ${layerId}:`, err);
      throw err;
    }
  }

  /**
   * Alterna a visibilidade da camada
   */
  setVisible(layerId, visible) {
    const entry = this.layers.get(layerId);
    if (!entry || !entry.leafletLayer) return;

    entry.visible = visible;
    if (visible) {
      if (!this.map.hasLayer(entry.leafletLayer)) {
        entry.leafletLayer.addTo(this.map);
      }
    } else {
      if (this.map.hasLayer(entry.leafletLayer)) {
        this.map.removeLayer(entry.leafletLayer);
      }
    }
    this.notifyListeners("visibilityChanged", entry);
  }

  /**
   * Ajusta a opacidade da camada
   * Para camadas GeoJSON, aplica a opacidade a todas as features
   */
  setOpacity(layerId, opacity) {
    const entry = this.layers.get(layerId);
    if (!entry || !entry.leafletLayer) return;

    entry.opacity = opacity;
    
    const isRasterComposite = !!(entry.config.rasterUrl && entry.config.rasterBounds);
    const targetFillOpacity = isRasterComposite ? 0.0 : (opacity * 0.75);

    // Para camadas GeoJSON (L.GeoJSON) ou grupos mistos com Raster
    if (typeof entry.leafletLayer.setStyle === "function") {
      entry.leafletLayer.setStyle({
        fillOpacity: targetFillOpacity,
        opacity: opacity
      });
    } else if (typeof entry.leafletLayer.setOpacity === "function") {
      // Para camadas de tiles ou imagens
      entry.leafletLayer.setOpacity(opacity);
    } else if (typeof entry.leafletLayer.eachLayer === "function") {
      entry.leafletLayer.eachLayer((subLayer) => {
        if (typeof subLayer.setStyle === "function") {
          subLayer.setStyle({ fillOpacity: targetFillOpacity, opacity: opacity });
        } else if (typeof subLayer.setOpacity === "function") {
          subLayer.setOpacity(opacity);
        }
      });
    }
    
    this.notifyListeners("opacityChanged", entry);
  }

  /**
   * Retorna os limites geodésicos para zoom
   */
  getBounds(layerId) {
    const entry = this.layers.get(layerId);
    if (!entry || !entry.leafletLayer) return null;
    if (entry.config.rasterBounds) {
      return L.latLngBounds(entry.config.rasterBounds);
    }
    if (typeof entry.leafletLayer.getBounds === "function") {
      return entry.leafletLayer.getBounds();
    }
    if (typeof entry.leafletLayer.eachLayer === "function") {
      let bounds = null;
      entry.leafletLayer.eachLayer((sub) => {
        if (typeof sub.getBounds === "function") {
          const b = sub.getBounds();
          bounds = bounds ? bounds.extend(b) : b;
        }
      });
      return bounds;
    }
    return null;
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notifyListeners(event, data) {
    this.listeners.forEach((fn) => {
      try {
        fn(event, data);
      } catch (e) {
        console.error("[LayerManager] Erro em listener:", e);
      }
    });
  }
}
