/**
 * Camada: Carta V - Zoneamentos da Macrozona de Consolidação Urbana: Maylasky (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 101, II, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta05Maylasky2026Config = {
  id: "carta_05_maylasky_2026",
  name: "Carta V: Consolidação Urbana - Maylasky (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 101, II, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_05_maylasky_mapa.png?v=20261115_nowindrose",
  rasterBounds: [[-23.67791, -47.09913], [-23.54788, -46.94378]],
  url: "data/distrito_maylasky_sao_roque.geojson",
  style: (feature) => ({
    color: "#D97706",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#EF4444",
  weight: 2.0,
  description: "Carta V Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos detalhados da Macrozona de Consolidação Urbana no Distrito de Maylasky (escala 1:12.500). Abrange bairros estruturantes como Sun Valley, Las Brisas, Recanto do Sabiá, Patrimônio do Carmo, Vila Vilma, Sanroqville, Jd. Vera Cruz, além da Zona de Urbanização de Média Densidade 2 (ZUR-md 2), ZUR-bd, e o polo industrial e logístico ao longo da ferrovia e Rod. Engº Renê Benedito da Silva. Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "maylasky",
    "mailasqui",
    "carta_05",
    "lc_40_2006",
    "david_berger",
    "sun_valley",
    "las_brisas",
    "patrimonio_do_carmo",
    "zur_bd",
    "zur_md_2",
    "zona_industrial",
    "zupa",
    "ferrovia",
    "rene_benedito"
  ]
};

export default carta05Maylasky2026Config;
