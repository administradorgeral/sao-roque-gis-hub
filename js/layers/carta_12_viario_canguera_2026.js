/**
 * Camada: Carta XII - Propostas do Sistema Viário e de Drenagem: Canguera (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Diretrizes do Sistema Viário e Drenagem Distrital (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta12ViarioCanguera2026Config = {
  id: "carta_12_viario_canguera_2026",
  name: "Carta XII: Sistema Viário e Drenagem - Canguera (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Diretrizes Viárias e de Drenagem da Minuta do Plano Diretor 2026 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_12_viario_canguera_mapa.png?v=20261115_nowindrose",
  rasterBounds: [[-23.66545, -47.29555], [-23.53541, -47.14019]],
  url: "data/distrito_canguera.geojson",
  style: (feature) => ({
    color: "#047857",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#0D9488",
  weight: 2.0,
  description: "Carta XII Oficial da Revisão do Plano Diretor: Propostas viárias e diretrizes de drenagem do Distrito de Canguera, contemplando a Estrada do Vinho, Rod. Quintino de Lima (SP-077), ciclovias turísticas e proteção das calhas de macrodrenagem de Itupararanga.",
  tags: ["plano_diretor_2026", "carta_12", "canguera", "sistema_viario", "drenagem", "estrada_do_vinho"]
};

export default carta12ViarioCanguera2026Config;
