/**
 * Índice de Camadas
 * Exporta todas as configurações de camadas disponíveis
 * O app.js pode importar todas as camadas ou selecionar especificamente
 */

// Importa todas as camadas individuais
import territorioMunicipalConfig from './territorio_municipal.js';
import distritosConfig from './distritos.js';
import setoresCensitariosConfig from './setores_censitarios.js';
import logradourosConfig from './logradouros.js';
import zoneamentoConfig from './zoneamento_pmd2006.js';
import minutaZoneamentoConfig from './zoneamento_minuta_pmd2006.js';
import declividadeConfig from './declividade.js';
import mdtConfig from './mdt.js';
import hidrografiaConfig from './hidrografia.js';
import geomorfologicoConfig from './geomorfologico.js';
import geologiaConfig from './geologia.js';
import fragilidadePotencialConfig from './fragilidade_potencial.js';
import pedologicoConfig from './pedologico.js';
import zoneamentoAmbientalConfig from './zoneamento_ambiental_pda2019.js';
import apaItupararangaLimiteConfig from './apa_itupararanga_limite.js';
import zonaProtecaoAeroportuariaCatarinaConfig from './zona_protecao_aeroportuaria_catarina.js';
import ahsConfig from './ahs.js';
import vegetacaoArboreaConfig from './vegetacao_arborea.js';
import rbcvCinturaoVerdeConfig from './rbcv_cinturao_verde.js';
import carta01Macrozoneamento2026Config from './carta_01_macrozoneamento_2026.js';
import carta02Zue2026Config from './carta_02_zue_2026.js';
import carta03ConsolidacaoUrbana2026Config from './carta_03_consolidacao_urbana_2026.js';
import carta04Sede2026Config from './carta_04_sede_2026.js';
import carta05Maylasky2026Config from './carta_05_maylasky_2026.js';
import carta06SaoJoaoNovo2026Config from './carta_06_sao_joao_novo_2026.js';
import carta07Canguera2026Config from './carta_07_canguera_2026.js';
import carta08Corredores2026Config from './carta_08_corredores_2026.js';
import carta09Aeis2026Config from './carta_09_aeis_2026.js';
import carta10ViarioSede2026Config from './carta_10_viario_sede_2026.js';
import carta11ViarioMaylasky2026Config from './carta_11_viario_maylasky_2026.js';
import carta12ViarioCanguera2026Config from './carta_12_viario_canguera_2026.js';
import carta13ObrasPrioritarias2026Config from './carta_13_obras_prioritarias_2026.js';

export { 
  territorioMunicipalConfig,
  distritosConfig,
  setoresCensitariosConfig,
  logradourosConfig,
  zoneamentoConfig, 
  minutaZoneamentoConfig, 
  declividadeConfig, 
  mdtConfig, 
  hidrografiaConfig,
  geomorfologicoConfig,
  geologiaConfig,
  fragilidadePotencialConfig,
  pedologicoConfig,
  zoneamentoAmbientalConfig,
  apaItupararangaLimiteConfig,
  zonaProtecaoAeroportuariaCatarinaConfig,
  ahsConfig,
  vegetacaoArboreaConfig,
  rbcvCinturaoVerdeConfig,
  carta01Macrozoneamento2026Config,
  carta02Zue2026Config,
  carta03ConsolidacaoUrbana2026Config,
  carta04Sede2026Config,
  carta05Maylasky2026Config,
  carta06SaoJoaoNovo2026Config,
  carta07Canguera2026Config,
  carta08Corredores2026Config,
  carta09Aeis2026Config,
  carta10ViarioSede2026Config,
  carta11ViarioMaylasky2026Config,
  carta12ViarioCanguera2026Config,
  carta13ObrasPrioritarias2026Config
};

// Array com todas as configurações de camadas
export const ALL_LAYERS = [
  territorioMunicipalConfig,
  distritosConfig,
  setoresCensitariosConfig,
  logradourosConfig,
  zoneamentoConfig, 
  minutaZoneamentoConfig, 
  declividadeConfig, 
  mdtConfig, 
  hidrografiaConfig,
  geomorfologicoConfig,
  geologiaConfig,
  fragilidadePotencialConfig,
  pedologicoConfig,
  zoneamentoAmbientalConfig,
  apaItupararangaLimiteConfig,
  zonaProtecaoAeroportuariaCatarinaConfig,
  ahsConfig,
  vegetacaoArboreaConfig,
  rbcvCinturaoVerdeConfig,
  carta01Macrozoneamento2026Config,
  carta02Zue2026Config,
  carta03ConsolidacaoUrbana2026Config,
  carta04Sede2026Config,
  carta05Maylasky2026Config,
  carta06SaoJoaoNovo2026Config,
  carta07Canguera2026Config,
  carta08Corredores2026Config,
  carta09Aeis2026Config,
  carta10ViarioSede2026Config,
  carta11ViarioMaylasky2026Config,
  carta12ViarioCanguera2026Config,
  carta13ObrasPrioritarias2026Config
];

// Função para filtrar camadas por tags
export function getLayersByTag(tag) {
  return ALL_LAYERS.filter(layer => layer.tags && layer.tags.includes(tag));
}

// Função para buscar camada por ID
export function getLayerById(layerId) {
  return ALL_LAYERS.find(layer => layer.id === layerId);
}
