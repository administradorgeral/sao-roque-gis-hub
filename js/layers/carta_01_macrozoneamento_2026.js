/**
 * Camada: Carta I - Macrozoneamento Municipal (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Art. 49, Parágrafo único e Anexo I da Minuta de Revisão da LC nº 39/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188 - Chefe de Divisão de Engenharia)
 * Órgão: Departamento de Planejamento e Meio Ambiente (DPMA) / Prefeitura de São Roque
 */

export const carta01Macrozoneamento2026Config = {
  id: "carta_01_macrozoneamento_2026",
  name: "Carta I: Macrozoneamento Municipal (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Art. 49 e Anexo I da Minuta de Revisão da LC nº 39/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_01_macrozoneamento_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#E11D48",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#E11D48",
  weight: 2.0,
  description: "Carta I Oficial da Revisão do Plano Diretor (2024–2026 / Revisão 05): Macrozoneamento Municipal em 3 Macrozonas estruturantes — Macrozona de Consolidação Urbana (Sede, Maylasky, São João Novo, Canguera), Macrozona de Urbanização Específica (Turismo, Mananciais, Castello, Mombaça) e Macrozona Rural (20.000 m² mínimo INCRA, Ecoturismo e Enogastronomia). Responsável Técnico: Eng. Civil David de Mello Berger (CREA: 5070025188).",
  tags: ["plano_diretor_2026", "macrozoneamento", "carta_01", "lc_39_2006", "david_berger", "urbanizacao_especifica", "consolidacao_urbana", "rural", "mombaca", "roteiro_vinho"]
};

export default carta01Macrozoneamento2026Config;
