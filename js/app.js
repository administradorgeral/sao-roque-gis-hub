/**
 * Central de Inteligência de Mapas - São Roque (SP)
 * Orquestrador Principal do WebGIS: Interface Imersiva Full-Screen
 * Painel Flutuante de Camadas (Floating Layer Card) · Sem Barra Superior
 * Botão Discreto de Fontes Oficiais no Rodapé do Painel de Camadas
 * 
 * Arquitetura Modular: Camadas podem ser adicionadas/removidas da pasta js/layers/
 */

import { CONFIG, initializeConfig } from "./config.js";
import { AttributeModal } from "./modules/attribute-modal.js?v=3";
import { LayerManager } from "./modules/layer-manager.js";
import { FloatingPanel } from "./modules/floating-panel.js?v=2";
import { OpacityManager } from "./modules/opacity-manager.js";
import { LayerRegistry } from "./modules/layer-registry.js";
import { LegislationCatalog } from "./modules/legislation-catalog.js";
import { AISearchEngine } from "./modules/ai-search.js";

document.addEventListener("DOMContentLoaded", async () => {
  // 1. Inicializa configuração com camadas dinâmicas
  const config = await initializeConfig();

  // 2. Registro da Projeção Cartográfica Oficial (SIRGAS 2000 / UTM Fuso 23S - EPSG: 31983)
  if (typeof proj4 !== "undefined") {
    proj4.defs("EPSG:31983", config.proj4Def);
  } else {
    console.error("[CRÍTICO] Proj4js não carregado. Operações métricas indisponíveis.");
  }

  // 3. Inicialização do Motor Leaflet
  const map = L.map("map", {
    center: config.center,
    zoom: config.defaultZoom,
    minZoom: config.minZoom,
    maxZoom: config.maxZoom,
    zoomControl: false,
    attributionControl: false
  });

  // 4. Basemaps 100% Gratuitos e sem Chave de API
  const basemaps = {};
  for (const [key, cfg] of Object.entries(config.basemaps)) {
    basemaps[key] = L.tileLayer(cfg.url, cfg.options);
  }
  // OpenStreetMap ativado por padrão
  basemaps.osm.addTo(map);

  // 5. Instanciação dos Módulos Desacoplados
  const attributeModal = new AttributeModal();
  const legislationCatalog = new LegislationCatalog(attributeModal);
  await legislationCatalog.init();

  const layerManager = new LayerManager(map, attributeModal);
  layerManager.setLegislationCatalog(legislationCatalog);

  const opacityManager = new OpacityManager(layerManager);
  const layerRegistry = new LayerRegistry(layerManager, attributeModal, opacityManager);

  // 6. Painel Flutuante de Camadas (Floating Layer Card)
  const btnLayersFab = document.getElementById("btn-layers-fab");

  const floatingPanel = new FloatingPanel(map, {
    panelSelector: "#floating-layers-panel",
    closeBtnSelector: "#btn-panel-close",
    backdropSelector: "#panel-backdrop",
    onStateChange: (isOpen) => {
      if (btnLayersFab) {
        btnLayersFab.classList.toggle("active-fab", isOpen);
        btnLayersFab.setAttribute("aria-expanded", String(isOpen));
      }
    }
  });

  if (btnLayersFab) {
    btnLayersFab.addEventListener("click", () => floatingPanel.toggle());
  }

  // 7. Assistente e Caixa de Pesquisa com IA Territorial
  const aiSearchEngine = new AISearchEngine(map, layerManager, attributeModal, legislationCatalog);
  await aiSearchEngine.init();

  // Registro global protegido para inspeção e testes
  window.GIS = {
    map,
    layerManager,
    attributeModal,
    legislationCatalog,
    floatingPanel,
    opacityManager,
    layerRegistry,
    aiSearchEngine,
    CONFIG: config,
    getPinLocation: () => (pinMarker && map.hasLayer(pinMarker)) ? pinMarker.getLatLng() : null,
    posicionarPin: (lat, lng) => posicionarPin(lat, lng),
    removerPin: () => {
      if (pinMarker) {
        map.removeLayer(pinMarker);
        pinMarker = null;
        if (aiSearchEngine && typeof aiSearchEngine.onPinRemoved === "function") {
          aiSearchEngine.onPinRemoved();
        }
        atualizarCoordenadas(config.center[0], config.center[1]);
        mostrarToast("Seleção removida");
      }
    },
    findZoneAtLatLng: (lat, lng) => findZoneAtLatLng(lat, lng)
  };

  // 7. HUD Superior de Coordenadas com Recurso de Cópia
  const coordText = document.getElementById("coord-text");
  const btnCopyCoord = document.getElementById("btn-copy-coord");
  const toastMsg = document.getElementById("toast-msg");
  let ultimaCoordTexto = "";

  function mostrarToast(texto) {
    if (!toastMsg) return;
    toastMsg.textContent = texto;
    toastMsg.classList.add("show");
    setTimeout(() => toastMsg.classList.remove("show"), 2200);
  }

  function formatarCoordenadas(lat, lng) {
    try {
      const utm = proj4("EPSG:4326", "EPSG:31983", [lng, lat]);
      const utmE = Math.round(utm[0]);
      const utmN = Math.round(utm[1]);
      return `UTM 23S: E ${utmE.toLocaleString('pt-BR')} N ${utmN.toLocaleString('pt-BR')} | ${lat.toFixed(5)}, ${lng.toFixed(5)}`;
    } catch {
      return `Lat: ${lat.toFixed(5)}, Long: ${lng.toFixed(5)}`;
    }
  }

  function atualizarCoordenadas(lat, lng) {
    if (!coordText) return;
    ultimaCoordTexto = formatarCoordenadas(lat, lng);
    coordText.textContent = ultimaCoordTexto;
  }

  if (btnCopyCoord) {
    btnCopyCoord.addEventListener("click", () => {
      if (!ultimaCoordTexto) return;
      navigator.clipboard.writeText(ultimaCoordTexto)
        .then(() => mostrarToast("Coordenadas copiadas!"))
        .catch(() => mostrarToast("Não foi possível copiar."));
    });
  }

  atualizarCoordenadas(config.center[0], config.center[1]);

  // 8. Ferramenta de Seleção de Local no Mapa (Pin Interativo)
  const btnSelectLocation = document.getElementById("btn-gps");
  let modoSelecaoAtivo = false;
  let pinMarker = null;

  function isPointInRing(pt, ring) {
    const [x, y] = pt;
    let inside = false;
    for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      const xi = ring[i][0], yi = ring[i][1];
      const xj = ring[j][0], yj = ring[j][1];
      const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
      if (intersect) inside = !inside;
    }
    return inside;
  }

  function findZoneAtLatLng(lat, lng) {
    for (const entry of layerManager.layers.values()) {
      if (!entry.data || !entry.data.features) continue;
      for (const feat of entry.data.features) {
        const geom = feat.geometry;
        if (!geom) continue;
        if (geom.type === "Polygon") {
          if (isPointInRing([lng, lat], geom.coordinates[0])) {
            return feat.properties;
          }
        } else if (geom.type === "MultiPolygon") {
          for (const poly of geom.coordinates) {
            if (isPointInRing([lng, lat], poly[0])) {
              return feat.properties;
            }
          }
        }
      }
    }
    return null;
  }

  const pinIcon = L.divIcon({
    className: "selection-pin-marker",
    html: `
      <div class="pin-marker-wrapper" style="display: flex; flex-direction: column; align-items: center; user-select: none;">
        <div class="pin-marker-head" style="background: #dc2626; color: #fff; width: 36px; height: 36px; border-radius: 50% 50% 50% 0; transform: rotate(-45deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 14px rgba(220,38,38,0.5), 0 2px 6px rgba(0,0,0,0.3); border: 2.5px solid #ffffff;">
          <span style="transform: rotate(45deg); font-size: 16px;">📍</span>
        </div>
        <div class="pin-marker-pulse" style="width: 14px; height: 14px; background: rgba(220,38,38,0.35); border-radius: 50%; margin-top: -6px;"></div>
      </div>
    `,
    iconSize: [36, 46],
    iconAnchor: [18, 44],
    tooltipAnchor: [0, -44]
  });

  function posicionarPin(lat, lng) {
    if (!pinMarker) {
      pinMarker = L.marker([lat, lng], {
        icon: pinIcon,
        draggable: true,
        autoPan: true,
        autoPanPadding: [50, 50],
        autoPanSpeed: 10,
        title: "Segure e arraste o pino para qualquer ponto do município"
      }).addTo(map);

      pinMarker.bindTooltip("📍 <strong>Segure e arraste</strong> para analisar qualquer ponto", {
        direction: "top",
        offset: [0, -42],
        className: "pin-tooltip",
        opacity: 0.95
      });

      pinMarker.on("dragstart", () => {
        pinMarker.setTooltipContent("📍 Arrastando pelo mapa...");
        pinMarker.openTooltip();
      });

      pinMarker.on("drag", (e) => {
        const pos = e.target.getLatLng();
        atualizarCoordenadas(pos.lat, pos.lng);
      });

      pinMarker.on("dragend", (e) => {
        const pos = e.target.getLatLng();
        atualizarCoordenadas(pos.lat, pos.lng);
        pinMarker.setTooltipContent("📍 <strong>Segure e arraste</strong> para analisar qualquer ponto");
        if (aiSearchEngine && typeof aiSearchEngine.onPinChanged === "function") {
          aiSearchEngine.onPinChanged(pos.lat, pos.lng);
        }
        mostrarToast("📍 Ponto ajustado e analisado em todas as camadas!");
      });

      pinMarker.on("click", (e) => {
        L.DomEvent.stopPropagation(e);
        const pos = pinMarker.getLatLng();
        atualizarCoordenadas(pos.lat, pos.lng);

        if (aiSearchEngine?.crossEngine && typeof aiSearchEngine.crossEngine.buildCrossDossierForPoint === "function") {
          const dossier = aiSearchEngine.crossEngine.buildCrossDossierForPoint(pos.lat, pos.lng, {
            zoneamentoGeoJson: layerManager.layers.get("zoneamento_lc4006")?.data,
            distritosGeoJson: layerManager.layers.get("distritos")?.data,
            apaGeoJson: layerManager.layers.get("apa_itupararanga")?.data
          });
          const zonaKey = dossier?.zoneamento_2006?.sigla || dossier?.zoneamento_2006?.denominacao;
          const legalContext = zonaKey
            ? legislationCatalog.getZoneLegalMetadata(zonaKey)
            : legislationCatalog.getZoneLegalMetadata("Geral");

          if (typeof attributeModal.showMultiLayerDossier === "function") {
            attributeModal.showMultiLayerDossier(dossier, legalContext);
            return;
          }
        }

        const zoneProps = findZoneAtLatLng(pos.lat, pos.lng);
        const zonaKey = zoneProps ? (zoneProps.zona || zoneProps.sigla || zoneProps.denominacao) : null;
        const legalContext = zonaKey
          ? legislationCatalog.getZoneLegalMetadata(zonaKey)
          : legislationCatalog.getZoneLegalMetadata("Geral");

        const modalTitle = zoneProps
          ? `Local: ${zoneProps.denominacao || zoneProps.zona}`
          : "Local Selecionado no Mapa";

        const baseProps = {
          "Latitude": pos.lat.toFixed(6),
          "Longitude": pos.lng.toFixed(6),
          "Coordenadas Projetadas": formatarCoordenadas(pos.lat, pos.lng),
          "Sistema de Referência": "SIRGAS 2000 (EPSG: 31983)",
          ...(zoneProps ? { "Zona Identificada": zoneProps.zona, "Denominação": zoneProps.denominacao || zoneProps.zona } : {})
        };

        if (legalContext && typeof attributeModal.showZoneLegalDetails === "function") {
          attributeModal.showZoneLegalDetails(modalTitle, baseProps, legalContext);
        } else {
          attributeModal.show(modalTitle, baseProps);
        }
      });
    } else {
      pinMarker.setLatLng([lat, lng]);
    }

    atualizarCoordenadas(lat, lng);
    if (aiSearchEngine && typeof aiSearchEngine.onPinChanged === "function") {
      aiSearchEngine.onPinChanged(lat, lng);
    }
    mostrarToast("Local selecionado!");
  }

  if (btnSelectLocation) {
    btnSelectLocation.addEventListener("click", () => {
      modoSelecaoAtivo = !modoSelecaoAtivo;
      btnSelectLocation.classList.toggle("active-fab", modoSelecaoAtivo);
      btnSelectLocation.setAttribute("aria-pressed", String(modoSelecaoAtivo));

      if (modoSelecaoAtivo) {
        if (!pinMarker) {
          const center = map.getCenter();
          posicionarPin(center.lat, center.lng);
        } else {
          map.panTo(pinMarker.getLatLng(), { animate: true });
        }
        mostrarToast("Clique no mapa ou arraste o pino para selecionar");
      } else {
        if (pinMarker) {
          map.removeLayer(pinMarker);
          pinMarker = null;
          if (aiSearchEngine && typeof aiSearchEngine.onPinRemoved === "function") {
            aiSearchEngine.onPinRemoved();
          }
          atualizarCoordenadas(config.center[0], config.center[1]);
          mostrarToast("Seleção removida");
        }
      }
    });
  }

  map.on("click", (e) => {
    if (modoSelecaoAtivo) {
      posicionarPin(e.latlng.lat, e.latlng.lng);
    } else {
      atualizarCoordenadas(e.latlng.lat, e.latlng.lng);
    }
  });

  map.on("mousemove", (e) => {
    if (!modoSelecaoAtivo && !pinMarker) {
      atualizarCoordenadas(e.latlng.lat, e.latlng.lng);
    }
  });

  // 9. Seletor de Basemaps
  const basemapChips = document.querySelectorAll(".basemap-chip");
  basemapChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      basemapChips.forEach((c) => {
        c.classList.remove("active");
        c.setAttribute("aria-checked", "false");
      });
      chip.classList.add("active");
      chip.setAttribute("aria-checked", "true");

      const chosen = chip.getAttribute("data-basemap");
      Object.keys(basemaps).forEach((key) => {
        if (map.hasLayer(basemaps[key])) map.removeLayer(basemaps[key]);
      });
      if (basemaps[chosen]) basemaps[chosen].addTo(map);
    });
  });

  // Tecla Escape fecha modais e painel flutuante
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (attributeModal && attributeModal.isOpen && attributeModal.isOpen()) {
        attributeModal.hide();
      }
      if (floatingPanel && floatingPanel.isOpen()) {
        floatingPanel.close();
      }
    }
  });

  // 11. Centralizar São Roque
  const btnReset = document.getElementById("btn-reset-zoom");
  if (btnReset) {
    btnReset.addEventListener("click", () => {
      map.setView(config.center, config.defaultZoom, { animate: true });
    });
  }

  // 12. Inicializar Acordeões de Legenda
  // Configura todos os acordeões de legenda para permitir expandir/colapsar
  const legendAccordions = document.querySelectorAll('.legend-accordion');
  legendAccordions.forEach(accordion => {
    const toggle = accordion.querySelector('.legend-toggle');
    const content = accordion.querySelector('.zone-legend-grid');
    
    if (toggle && content) {
      toggle.addEventListener('click', () => {
        const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        const newState = !isExpanded;
        
        toggle.setAttribute('aria-expanded', String(newState));
        content.setAttribute('aria-hidden', String(!newState));
        
        // Atualiza o texto e ícone do botão
        const toggleText = toggle.querySelector('.legend-toggle-text');
        const toggleIcon = toggle.querySelector('.legend-icon');
        
        if (toggleText) {
          toggleText.textContent = newState ? '📊 Ocultar Legenda' : '📊 Ver Legenda';
        }
        if (toggleIcon) {
          toggleIcon.textContent = newState ? '▲' : '▼';
        }
        
        // Animação
        if (newState) {
          content.style.maxHeight = content.scrollHeight + 'px';
          content.style.opacity = '1';
        } else {
          content.style.maxHeight = '0';
          content.style.opacity = '0';
        }
      });
    }
  });

  // 13. Carregar Camadas Dinamicamente usando LayerRegistry
  // Esta abordagem permite adicionar/remover camadas sem modificar o app.js
  console.log("[*] Iniciando carregamento dinâmico de camadas...");
  
  if (config.layers && config.layers.length > 0) {
    await layerRegistry.loadLayersFromConfig(config.layers, { 
      autoRegisterOpacity: true 
    });
    console.log("[*] Todas as camadas carregadas com sucesso!");
  } else {
    console.warn("[!] Nenhuma camada configurada para carregamento.");
  }

  // 13. Configurações Específicas do Projeto (Legado - pode ser movido para módulos)
  // Estas configurações específicas podem ser mantidas aqui ou movidas para arquivos de camadas
  
  // Se precisar de configurações específicas para camadas existentes:
  // Exemplo: layerRegistry.setupSpecialHandling('zoneamento_pmd2006', { ... });

  console.log("[*] São Roque GIS Hub: Interface imersiva full-screen com painel flutuante de camadas ativa.");
});
