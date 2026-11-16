/**
 * Camada: Carta XI - Propostas do Sistema Viário e de Drenagem: Maylasky (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Diretrizes do Sistema Viário e Drenagem Distrital (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta11ViarioMaylasky2026Config = {
  id: "carta_11_viario_maylasky_2026",
  name: "Carta XI: Sistema Viário e Drenagem - Maylasky (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Diretrizes Viárias e de Drenagem da Minuta do Plano Diretor 2026 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_11_viario_maylasky_mapa.png?v=20261115_nowindrose",
  rasterBounds: [[-23.67791, -47.09913], [-23.54788, -46.94378]],
  url: "data/distrito_maylasky_sao_roque.geojson",
  style: (feature) => ({
    color: "#B45309",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#0284C7",
  weight: 2.0,
  description: "Carta XI Oficial da Revisão do Plano Diretor: Propostas viárias e diretrizes de drenagem do Distrito de Maylasky, integrando o eixo da Rodovia Engº Renê Benedito da Silva, travessias da ferrovia e escoamento hídrico do Córrego Maylasky.",
  tags: ["plano_diretor_2026", "carta_11", "maylasky", "sistema_viario", "drenagem", "rene_benedito"]
};

export default carta11ViarioMaylasky2026Config;
