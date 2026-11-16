/**
 * Camada: Carta X - Propostas do Sistema Viário e de Drenagem: Sede (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Diretrizes do Sistema Viário Estruturador e Bacias de Macrodrenagem (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta10ViarioSede2026Config = {
  id: "carta_10_viario_sede_2026",
  name: "Carta X: Sistema Viário e Drenagem - Sede (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Diretrizes Viárias e de Drenagem da Minuta do Plano Diretor 2026 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_10_viario_sede_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.58853, -47.18916], [-23.47295, -47.09810]],
  url: "data/distrito_sede_sao_roque.geojson",
  style: (feature) => ({
    color: "#1E293B",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#3B82F6",
  weight: 2.0,
  description: "Carta X Oficial da Revisão do Plano Diretor: Propostas viárias estruturantes, anéis de contorno, ciclovias, faixas non aedificandi e bacias de retenção de macrodrenagem do Distrito Sede de São Roque.",
  tags: ["plano_diretor_2026", "carta_10", "sede", "sistema_viario", "drenagem", "mobilidade"]
};

export default carta10ViarioSede2026Config;
