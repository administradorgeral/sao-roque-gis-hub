/**
 * Camada: Carta II - Zoneamentos da Macrozona de Urbanização Específica (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 66 a 100 e Quadros I, II, III e IV da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta02Zue2026Config = {
  id: "carta_02_zue_2026",
  name: "Carta II: Zoneamentos da Macrozona de Urbanização Específica (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 66 a 100 e Quadros I a IV da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_02_zue_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#007FFF",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#007FFF",
  weight: 2.0,
  description: "Carta II Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos da Macrozona de Urbanização Específica (153,33 km² totais). Divide o território periurbano em 5 zonas: ZUE - Chácaras em Manancial (49,19 km²), ZUE - Interesse Turístico (89,92 km²), ZUE - Ocupação Estratégica (7,58 km²), ZUE - Desenvolvimento Econômico (4,77 km²) e ZUE - Atividades Especiais Raposo Tavares (1,87 km²). Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "zue",
    "urbanizacao_especifica",
    "carta_02",
    "lc_40_2006",
    "david_berger",
    "chacaras_manancial",
    "interesse_turistico",
    "mombaca",
    "castello_branco",
    "desenvolvimento_economico",
    "ocupacao_estrategica",
    "raposo_tavares",
    "apa_itupararanga"
  ]
};

export default carta02Zue2026Config;
