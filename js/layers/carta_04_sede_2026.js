/**
 * Camada: Carta IV - Zoneamentos da Macrozona de Consolidação Urbana: Sede (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 101, I, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta04Sede2026Config = {
  id: "carta_04_sede_2026",
  name: "Carta IV: Consolidação Urbana - Sede (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 101, I, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_04_sede_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.58853, -47.18916], [-23.47295, -47.09810]],
  url: "data/distrito_sede_sao_roque.geojson",
  style: (feature) => ({
    color: "#2563EB",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#DDA56E",
  weight: 2.0,
  description: "Carta IV Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos detalhados da Macrozona de Consolidação Urbana no Distrito Sede (escala 1:12.500). Abrange o Centro Histórico (Zona Central), ZUR-bd, ZUR-md 1, ZUR-ad, Zona Industrial e ZUPA (Preservação Ambiental / Mata da Câmara), regulamentando coeficientes, recuos, IPTU progressivo e Transferência do Potencial Construtivo (TPC). Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "sede",
    "carta_04",
    "lc_40_2006",
    "david_berger",
    "centro_historico",
    "zur_bd",
    "zur_md",
    "zur_ad",
    "zona_central",
    "zona_industrial",
    "zupa",
    "brasital",
    "mata_da_camara",
    "ferrovia"
  ]
};

export default carta04Sede2026Config;
