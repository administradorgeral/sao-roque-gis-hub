/**
 * Camada: Carta IX - Áreas de Especial Interesse (AEIS, AEIT, AEIU) (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 166 a 180 da Minuta de Revisão da LC nº 40/2006 e LC nº 39/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta09Aeis2026Config = {
  id: "carta_09_aeis_2026",
  name: "Carta IX: Áreas de Especial Interesse - AEIS, AEIT, AEIU (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 166 a 180 da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_09_aeis_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#9333EA",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#8B5CF6",
  weight: 2.0,
  description: "Carta IX Oficial da Revisão do Plano Diretor: Delimitação das Áreas de Especial Interesse Social (AEIS 1, 2 e 3 para habitação de interesse social e regularização fundiária), Áreas de Especial Interesse Turístico (AEIT) e Áreas de Especial Interesse Urbanístico (AEIU).",
  tags: ["plano_diretor_2026", "carta_09", "aeis", "aeit", "aeiu", "habitacao_social", "regularizacao_fundiaria"]
};

export default carta09Aeis2026Config;
