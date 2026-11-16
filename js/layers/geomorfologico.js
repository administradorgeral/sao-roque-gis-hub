/**
 * Camada: Compartimentos Geomorfológicos (Anexo 4.3.4-1 - PDA 2019 / Ross & Moroz 1997)
 * Unidades Morfoesculturais do Município de São Roque
 * Vetor Nativo de Alta Fidelidade (SIRGAS 2000 UTM 23S)
 */

export const geomorfologicoConfig = {
  id: "geomorfologico",
  name: "Compartimentos Geomorfológicos (Ross & Moroz)",
  categoria: "Geotécnica e Geomorfologia",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / IPT / Ross & Moroz",
  marco_legal: "Ross & Moroz (1997), IPT (1981), LCs nº 39/06, 40/06 e 41/06, Lei Estadual nº 11.579/03, Leis Federais nº 6.766/79, 12.608/12, 12.651/12 e STF ADPF 747/749",
  escala: "1:50.000",
  url: "data/geomorfologico_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.60,
  cor: "#FFAA00",
  weight: 1.5,
  description: "3 Unidades Morfoesculturais (Ross & Moroz 1997) · Planaltos de Jundiaí, Ibiúna e Paulistano",
  tags: ["geomorfologia", "relevo", "ross_moroz", "planalto_jundiai", "planalto_ibiuna", "planalto_paulistano", "ipt", "pda2019"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#FFAA00";
    return {
      fillColor: cor,
      fillOpacity: 0.60,
      color: "#333333",
      weight: 1.5,
      opacity: 0.85
    };
  }
};

export default geomorfologicoConfig;
