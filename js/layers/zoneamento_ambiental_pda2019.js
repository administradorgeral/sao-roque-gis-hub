/**
 * Camada: Zoneamento Ambiental (PDA 2019 - Anexo 8.3.1-1)
 * Macrozoneamento Ambiental e Zonas Prioritárias da Estância Turística de São Roque
 * Vetor Nativo de Alta Precisão (SIRGAS 2000 UTM 23S) - 9 Zonas e Subzonas
 */

export const zoneamentoAmbientalConfig = {
  id: "zoneamento_ambiental_pda2019",
  name: "Zoneamento Ambiental (PDA 2019)",
  categoria: "Ambiental e Geotécnica",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / PDA 2019",
  marco_legal: "PDA (2019), LCs nº 39/06, 40/06 e 41/06, Lei Estadual nº 11.579/03, Leis Federais nº 12.651/12, 11.428/06 e 6.766/79",
  escala: "1:50.000",
  url: "data/zoneamento_ambiental_pda2019_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#4CE600",
  weight: 1.2,
  description: "9 Zonas e Subzonas Ambientais Oficiais (Anexo 8.3.1-1) · ZPBIO, ZPURB, ZPED (Erosivos e Pluviais), ZPHID (Sensíveis, Rurais, Urbanos) e ZDES (Castelo e Socioambiental)",
  tags: ["zoneamento_ambiental", "pda2019", "macrozoneamento", "biodiversidade", "mananciais", "erosao", "castelo_branco", "itupararanga"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#4CE600";
    return {
      fillColor: cor,
      fillOpacity: 0.65,
      color: "#222222",
      weight: 1.2,
      opacity: 0.85
    };
  }
};

export default zoneamentoAmbientalConfig;
