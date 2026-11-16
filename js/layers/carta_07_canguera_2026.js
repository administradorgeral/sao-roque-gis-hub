/**
 * Camada: Carta VII - Zoneamentos da Macrozona de Consolidação Urbana: Canguera (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 101, IV, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta07Canguera2026Config = {
  id: "carta_07_canguera_2026",
  name: "Carta VII: Consolidação Urbana - Canguera (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 101, IV, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_07_canguera_mapa.png?v=20261115_nowindrose",
  rasterBounds: [[-23.66545, -47.29555], [-23.53541, -47.14019]],
  url: "data/distrito_canguera.geojson",
  style: (feature) => ({
    color: "#059669",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#10B981",
  weight: 2.0,
  description: "Carta VII Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos detalhados da Macrozona de Consolidação Urbana no Distrito de Canguera (escala 1:12.500). Abrange o polo turístico e residencial de Canguera, incluindo Bairro Goianã, Campininha, Jd. Suíça Paulista, Vinhedos III, Jd. Sta Vitória, Rancharia, Vale das Flores, Bairro do Pavão, Jd. Felicidade, Residencial Vaiente, Recanto do Matão, Paisagem Colonial, Jd. Nova Canguera, Vila Belmiro, ao longo da Estrada do Vinho e Rod. Quintino de Lima (SP-077), regulamentando ZUR-md 2, ZUR-bd, ZUPA e Corredores Comerciais Turísticos. Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "canguera",
    "carta_07",
    "lc_40_2006",
    "david_berger",
    "estrada_do_vinho",
    "quintino_de_lima",
    "campininha",
    "pavao",
    "zur_bd",
    "zur_md_2",
    "zupa",
    "rota_do_vinho"
  ]
};

export default carta07Canguera2026Config;
