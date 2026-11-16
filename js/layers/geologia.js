/**
 * Camada: Unidades Geológicas e Substrato Rochoso (Anexo 4.3.5-1 - PDA 2019 / CPRM / IPT)
 * Geologia Estratigráfica e Litológica do Município de São Roque
 * Vetor Nativo de Alta Fidelidade (SIRGAS 2000 UTM 23S)
 */

export const geologiaConfig = {
  id: "geologia",
  name: "Geologia e Substrato Rochoso (Anexo 4.3.5-1)",
  categoria: "Geotécnica e Geomorfologia",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / CPRM / SGB / IPT",
  marco_legal: "CPRM (2006), IPT (1981), LCs nº 39/06, 40/06 e 41/06, Lei Estadual nº 11.579/03, Leis Federais nº 6.766/79 e 12.608/12",
  escala: "1:50.000",
  url: "data/geologia_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.60,
  cor: "#CDAA66",
  weight: 1.2,
  description: "7 Unidades Litoestratigráficas (CPRM 2006) · Granitos São Roque, Ibiúna e Itapevi, Fms. Estrada dos Romeiros e Piragibu, Grupos Itaberaba e Votuverava",
  tags: ["geologia", "substrato_rochoso", "cprm", "sgb", "granito_sao_roque", "granito_ibiuna", "estrada_romeiros", "piragibu", "votuverava", "pda2019"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#CDAA66";
    return {
      fillColor: cor,
      fillOpacity: 0.60,
      color: "#333333",
      weight: 1.2,
      opacity: 0.85
    };
  }
};

export default geologiaConfig;
