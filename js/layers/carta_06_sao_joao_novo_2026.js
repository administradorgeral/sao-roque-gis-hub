/**
 * Camada: Carta VI - Zoneamentos da Macrozona de Consolidação Urbana: São João Novo (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 101, III, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura da Estância Turística de São Roque
 */

export const carta06SaoJoaoNovo2026Config = {
  id: "carta_06_sao_joao_novo_2026",
  name: "Carta VI: Consolidação Urbana - São João Novo (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 101, III, 102 a 150 e Quadros V a IX da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:12.500 (Indicada)",
  rasterUrl: "data/carta_06_sao_joao_novo_mapa.png?v=20261115_nowindrose",
  rasterBounds: [[-23.55159, -47.08063], [-23.42156, -46.92527]],
  url: "data/distrito_sao_joao_novo.geojson",
  style: (feature) => ({
    color: "#7C3AED",
    weight: 3.0,
    dashArray: "4, 4",
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#06B6D4",
  weight: 2.0,
  description: "Carta VI Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Zoneamentos detalhados da Macrozona de Consolidação Urbana no Distrito de São João Novo (escala 1:12.500). Abrange núcleos residenciais e chácaras como Boqueirão, Mont Serrat, Vila Bello, São Julião, Vila Santa Terezinha, Vila Vinhas, Vila Antártica, Mirante da Serra, Sítio Bela Vista, Chácaras Alpinas, além de ZUR-md 2, ZUR-bd, ZUPA e a interface aeroportuária com o Aeroporto Catarina (SBJH). Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: [
    "plano_diretor_2026",
    "sao_joao_novo",
    "carta_06",
    "lc_40_2006",
    "david_berger",
    "boqueirao",
    "mont_serrat",
    "sao_juliao",
    "zur_bd",
    "zur_md_2",
    "zupa",
    "catarina",
    "ferrovia",
    "rene_benedito"
  ]
};

export default carta06SaoJoaoNovo2026Config;
