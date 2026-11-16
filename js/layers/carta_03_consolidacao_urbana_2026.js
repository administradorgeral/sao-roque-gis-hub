/**
 * Camada: Carta III - Zoneamentos da Macrozona de Consolidação Urbana (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 101 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta03ConsolidacaoUrbana2026Config = {
  id: "carta_03_consolidacao_urbana_2026",
  name: "Carta III: Zoneamentos da Macrozona de Consolidação Urbana (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 101 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_03_consolidacao_urbana_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#FF7F00",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#FF7F00",
  weight: 2.0,
  description: "Carta III Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos da Macrozona de Consolidação Urbana (39,22 km² totais). Articula a malha urbana dos 4 perímetros consolidados (Sede, Maylasky, São João Novo e Canguera) em 6 zonas urbanas estruturantes: ZUR-bd (6,31 km²), ZUR-md (18,88 km²), ZUR-ad (2,70 km²), Zona Urbana Central (0,63 km²), Zona Urbana Industrial (1,55 km²) e ZUPA - Preservação Ambiental (9,15 km²). Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "consolidacao_urbana",
    "carta_03",
    "lc_40_2006",
    "david_berger",
    "zur_bd",
    "zur_md",
    "zur_ad",
    "zona_central",
    "zona_industrial",
    "zupa",
    "sede",
    "maylasky",
    "sao_joao_novo",
    "canguera"
  ]
};

export default carta03ConsolidacaoUrbana2026Config;
