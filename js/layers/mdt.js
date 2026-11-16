/**
 * Camada: MDT - Relevo e Hipsometria (Anexo 4.3.2-2 - PDA 2019 / IGC 1978)
 * Modelo Digital de Terreno Classificado em 5 Faixas Hipsométricas
 * Vetor Nativo SIRGAS 2000 UTM 23S (EPSG: 31983)
 */

export const mdtConfig = {
  id: "mdt",
  name: "MDT - Relevo e Hipsometria (Anexo 4.3.2-2)",
  categoria: "Topografia e Hipsometria",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / IGC SP",
  marco_legal: "Lei Federal nº 12.651/2012 Art. 4º, IX, STF ADPF 747/749, Resolução CONAMA nº 303/2002 e LC Municipal nº 39/2006 (Arts. 22 e 23 - Patrimônio Natural e Morros)",
  escala: "1:50.000",
  url: "data/mdt_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#7AAB00",
  weight: 1,
  description: "5 Faixas Altimétricas (630m a 1.125m) · Vetor Nativo SIRGAS 2000",
  tags: ["mdt", "hipsometria", "relevo", "altitude", "saboo", "topo_de_morro", "pda2019"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#7AAB00";
    return {
      fillColor: cor,
      fillOpacity: 0.65,
      color: cor,
      weight: 1,
      opacity: 0.85
    };
  }
};

export default mdtConfig;
