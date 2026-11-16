/**
 * Central de Inteligência de Mapas - São Roque (SP)
 * Configuração Geral e Definições de Sistema
 * Datum Oficial: SIRGAS 2000 / UTM Fuso 23S (EPSG: 31983)
 * 
 * Esta configuração pode ser estendida ou substituída por módulos de camadas
 */

export const CONFIG = {
  municipio: "São Roque",
  uf: "SP",
  codigo_ibge: "3550605",
  center: [-23.5376, -47.1141],
  defaultZoom: 13,
  minZoom: 10,
  maxZoom: 19,

  // Definição Proj4 para SIRGAS 2000 / UTM 23S (EPSG: 31983)
  proj4Def: "+proj=utm +zone=23 +south +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs",

  // Basemaps 100% Gratuitos e sem Chave de API
  basemaps: {
    osm: {
      name: "OpenStreetMap",
      url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      options: {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
      }
    },
    satellite: {
      name: "Satélite (Esri)",
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      options: {
        maxZoom: 19,
        attribution: "Esri, Maxar, Earthstar Geographics"
      }
    },
    topo: {
      name: "Topografia Relevo",
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
      options: {
        maxZoom: 19,
        attribution: "Esri, HERE, Garmin"
      }
    },
    gray: {
      name: "Claro (Esri Gray)",
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
      options: {
        maxZoom: 19,
        attribution: "Esri, HERE"
      }
    }
  },

  // Configurações de Opacidade
  opacitySettings: {
    defaultOpacity: 0.75,
    fillOpacityMultiplier: 0.75,
    strokeOpacity: 0.95
  },

  // Registro de Camadas Homologadas do Sistema
  // NOTA: Estas camadas podem ser carregadas dinamicamente a partir de js/layers/
  // ou substituídas completamente por importações de módulos
  layers: []
};

// Função para carregar camadas dinamicamente
export async function loadLayersFromModules() {
  try {
    // Tenta importar camadas do diretório js/layers/
    const layersModule = await import(`./layers/index.js?v=${Date.now()}`);
    return layersModule.ALL_LAYERS || [];
  } catch (error) {
    console.log('[CONFIG] Carregamento dinâmico de camadas não disponível, usando configuração estática');
    // Retorna camadas padrão se o carregamento dinâmico falhar
    // Usando IDs que correspondem aos elementos no HTML
    return [
      {
        id: "zoneamento",
        name: "Zoneamento Municipal (Plano Diretor 2006)",
        esfera: "Municipal",
        orgao: "Prefeitura da Estância Turística de São Roque",
        marco_legal: "Lei Complementar nº 40/2006",
        escala: "1:10.000",
        url: "data/pmsr_zoneamento_pmd2006.geojson",
        defaultVisible: true,
        defaultOpacity: 0.55,
        cor: "#7c3aed"
      },
      {
        id: "minuta-zoneamento",
        name: "Minuta do Zoneamento (Estudo Técnico PMD 2006)",
        esfera: "Municipal",
        orgao: "Prefeitura da Estância Turística de São Roque",
        marco_legal: "Estudo Técnico Urbanístico / Minuta Técnica",
        escala: "1:10.000",
        url: "data/pmsr_zoneamento_minuta_pmd2006.geojson",
        defaultVisible: false,
        defaultOpacity: 0.50,
        cor: "#007fff"
      }
    ];
  }
}

// Função para inicializar configuração com camadas
export async function initializeConfig() {
  const config = { ...CONFIG };
  config.layers = await loadLayersFromModules();
  return config;
}
