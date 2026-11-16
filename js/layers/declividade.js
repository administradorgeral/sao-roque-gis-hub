/**
 * Camada: Declividade do Terreno (Anexo 4.3.3-1 - PDA 2019 / IGC 1978)
 * Classificação Pedológica de Lepsch (1983) / Embrapa
 * Vetor Nativo extraído com precisão submétrica (SIRGAS 2000 UTM 23S)
 */

export const declividadeConfig = {
  id: "declividade",
  name: "Declividade do Terreno (Lepsch/Embrapa)",
  categoria: "Meio Físico e Topografia",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / IGC SP",
  marco_legal: "Lei Federal nº 6.766/79 (Art. 3º), LC Municipal nº 40/2006 (Art. 13 e 43), LC Municipal nº 39/2006 (Art. 18), Lei Federal nº 12.608/2012 (Art. 22 - PNPDEC) e Lei Federal nº 12.651/2012 (Art. 4º, V)",
  escala: "1:50.000",
  url: "data/declividade_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#FF5500",
  weight: 1,
  description: "5 Classes Lepsch/Embrapa · Vetor Nativo SIRGAS 2000",
  tags: ["declividade", "relevo", "topografia", "lepsch", "embrapa", "pda2019", "geotecnica"],
  
  // Função de estilo por classe de declividade
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#FFAA00";
    return {
      fillColor: cor,
      fillOpacity: 0.65,
      color: cor,
      weight: 1,
      opacity: 0.85
    };
  }
};

export default declividadeConfig;
