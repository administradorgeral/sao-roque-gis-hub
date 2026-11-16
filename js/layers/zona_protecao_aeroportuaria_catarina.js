/**
 * Camada: Proteção Aeroportuária, Helipontos Homologados e TMA (DECEA / ANAC)
 * Servidões Aeronáuticas Federais (CBA - Lei Federal nº 7.565/1986 Arts. 43 a 47)
 * - Aeroporto Internacional Catarina (SBJH / Portaria 230/SAGA): Pista 13/31, PBZPA e ASA 20km
 * - Heliponto Vila Don Patto (SWVD / Portaria 176/DGCEA de 2014) - Estrada do Vinho
 * - Heliponto Taxaquara Golf Club (SIZT / Portaria 394/ICA de 2018)
 * - Heliponto NÓR Hotel & Spa (Portaria 1465/SAGA de 2023) - Bairro Gabriel Piza
 * - Superfície Horizontal Externa de Congonhas (SBSP / Portaria 28/ICA) e TMA-SP (10.603 ha / 34,5%)
 */

export const zonaProtecaoAeroportuariaCatarinaConfig = {
  id: "zona_protecao_aeroportuaria_catarina",
  name: "Proteção Aeroportuária e Helipontos (DECEA / ANAC)",
  categoria: "Infraestrutura Aeronáutica e Servidão Federal",
  esfera: "Federal",
  orgao: "Comando da Aeronáutica (COMAER) / DECEA / ANAC",
  marco_legal: "Lei Federal nº 7.565/86 (CBA Arts. 43-47), Lei 12.725/12 (ASA 20km), RBAC 155 (Helipontos), RBAC 161 (Ruído), ICA 11-408",
  escala: "1:25.000",
  url: "data/zona_protecao_aeroportuaria_catarina_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.70,
  cor: "#EA580C",
  weight: 2,
  description: "Complexo de servidões aeronáuticas: Aeroporto Catarina (SBJH), 3 Helipontos Homologados (Vila Don Patto SWVD, Taxaquara SIZT, NÓR Hotel) e Superfície Horizontal Externa de Congonhas (SBSP 45km / TMA-SP).",
  tags: [
    "aeroporto_catarina", "sbjh", "helipontos", "vila_don_patto", "swvd", "taxaquara", "sizt", "nor_hotel",
    "congonhas", "sbsp", "tma_sp", "servidao_aeronautica", "decea", "sysaga", "anac", "gabarito", "pzph", "pbzpa", "asa_20km"
  ],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const cod = props.codigo || "";

    // 1. Pista 13/31 - Aeroporto Catarina (SBJH)
    if (cod === 'PISTA_SBJH') {
      return {
        fillColor: "#0284C7",
        fillOpacity: 0.95,
        color: "#0369A1",
        weight: 2.5,
        opacity: 1.0
      };
    }

    // 2. FATO / TLOF (Piso de toque dos Helipontos: Vila Don Patto, Taxaquara, NÓR)
    if (cod.startsWith('FATO_')) {
      return {
        fillColor: "#DC2626",
        fillOpacity: 1.0,
        color: "#991B1B",
        weight: 3.0,
        opacity: 1.0
      };
    }

    // 3. PZPH (Superfície de Aproximação / Funil 1.000m dos Helipontos)
    if (cod.startsWith('PZPH_')) {
      return {
        fillColor: "#F43F5E",
        fillOpacity: 0.40,
        color: "#BE123C",
        weight: 2.2,
        opacity: 0.95,
        dashArray: "5, 3"
      };
    }

    // 4. Cone de Aproximação e Ruído do Aeroporto Catarina (PBZPA / SLO)
    if (cod === 'PBZPA_CONE_SLO') {
      return {
        fillColor: "#EA580C",
        fillOpacity: 0.35,
        color: "#C2410C",
        weight: 2.0,
        opacity: 0.90,
        dashArray: "6, 4"
      };
    }

    // 5. Superfície Horizontal Externa de Congonhas (SBSP / Raio 45 km / TMA-SP)
    if (cod === 'SHE_SBSP_CONGONHAS') {
      return {
        fillColor: "#8B5CF6",
        fillOpacity: 0.12,
        color: "#6D28D9",
        weight: 2.0,
        opacity: 0.85,
        dashArray: "8, 5"
      };
    }

    // 6. Área de Segurança Aeroportuária (ASA raio 20 km do Aeroporto Catarina)
    return {
      fillColor: "#F59E0B",
      fillOpacity: 0.12,
      color: "#D97706",
      weight: 1.8,
      opacity: 0.80,
      dashArray: "4, 4"
    };
  }
};

export default zonaProtecaoAeroportuariaCatarinaConfig;
