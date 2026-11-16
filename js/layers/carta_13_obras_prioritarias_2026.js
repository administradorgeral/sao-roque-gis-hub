/**
 * Camada: Carta XIII - Intervenções e Obras Prioritárias SRQ-01 a SRQ-22 (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Anexo de Obras Estruturantes e Ações Prioritárias da Minuta de Revisão do Plano Diretor (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta13ObrasPrioritarias2026Config = {
  id: "carta_13_obras_prioritarias_2026",
  name: "Carta XIII: Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Programa de Intervenções e Obras Prioritárias da Minuta do Plano Diretor (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_13_obras_prioritarias_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#DC2626",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.80,
  cor: "#DC2626",
  weight: 2.2,
  description: "Carta XIII Oficial da Revisão do Plano Diretor: Mapeamento oficial das 22 Obras Estruturantes Prioritárias (SRQ-01 a SRQ-22) abrangendo intervenções em áreas de risco geológico/inundação, canalizações, novas pontes, duplicações de acessos e grandes eixos de infraestrutura.",
  tags: ["plano_diretor_2026", "carta_13", "obras_prioritarias", "srq01_srq22", "infraestrutura", "areas_de_risco", "drenagem"]
};

export default carta13ObrasPrioritarias2026Config;
