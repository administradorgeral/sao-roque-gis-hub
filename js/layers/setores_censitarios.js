/**
 * Camada: Setores Censitários de São Roque (IBGE Censo Demográfico 2022)
 * 188 Setores Censitários: 134 Urbanos e 54 Rurais
 * Base para indicadores demográficos, domicílios particulares e planejamento de serviços públicos
 */

export const setoresCensitariosConfig = {
  id: "setores_censitarios",
  name: "Setores Censitários (IBGE Censo 2022)",
  categoria: "Demografia e Estatística Territorial",
  esfera: "Federal / Municipal",
  orgao: "Instituto Brasileiro de Geografia e Estatística (IBGE)",
  marco_legal: "Lei Federal nº 5.534/1968, Censo Demográfico 2022 (IBGE 3550605)",
  escala: "1:25.000",
  url: "data/setores_censitarios_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#64748B",
  weight: 1.2,
  description: "Malha com os 188 Setores Censitários oficiais do IBGE para o Censo 2022 em São Roque: 134 setores urbanos e 54 rurais, base para densidade de moradores e domicílios.",
  tags: ["setores_censitarios", "ibge2022", "demografia", "censo", "moradores", "domicilios"],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const isUrbano = props.situacao === 'Urbana';
    return {
      fillColor: isUrbano ? "#3B82F6" : "#10B981",
      fillOpacity: 0.12,
      color: isUrbano ? "#1D4ED8" : "#047857",
      weight: 1.0,
      opacity: 0.85
    };
  }
};

export default setoresCensitariosConfig;
