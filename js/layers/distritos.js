/**
 * Camada: Distritos Municipais Oficiais de São Roque (SP)
 * Base: Censo Demográfico IBGE 2022 e Lei Orgânica Municipal nº 1.801/1990
 * 4 Distritos: São Roque (Sede), Canguera, São João Novo e Mailasqui
 */

export const distritosConfig = {
  id: "distritos",
  name: "Distritos Municipais (IBGE 2022)",
  categoria: "Divisão Político-Administrativa",
  esfera: "Municipal",
  orgao: "Prefeitura de São Roque / IBGE (Cód. 3550605)",
  marco_legal: "Lei Orgânica nº 1.801/90, Lei Estadual de Criação de Distritos e Censo IBGE 2022",
  escala: "1:50.000",
  url: "data/distritos_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.70,
  cor: "#2563EB",
  weight: 2.2,
  description: "Divisão territorial oficial nos 4 Distritos Municipais: São Roque (Sede - 12.336 ha), Canguera (8.639 ha), São João Novo (6.409 ha) e Mailasqui (3.316 ha).",
  tags: ["distritos", "divisao_administrativa", "ibge2022", "sao_roque", "canguera", "mailasqui", "sao_joao_novo"],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const color = props.cor_hex || "#2563EB";
    return {
      fillColor: color,
      fillOpacity: 0.18,
      color: color,
      weight: 2.5,
      opacity: 0.95,
      dashArray: "6, 4"
    };
  }
};

export default distritosConfig;
