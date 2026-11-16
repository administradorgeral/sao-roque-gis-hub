/**
 * Camada: Solos e Unidades Pedológicas (Anexo 4.3.6-1 - PDA 2019 / IAC / EMBRAPA)
 * Mapeamento Pedológico Oficial da Estância Turística de São Roque
 * Vetor Nativo de Alta Precisão (SIRGAS 2000 UTM 23S) - 5 Unidades Pedológicas
 */

export const pedologicoConfig = {
  id: "pedologico",
  name: "Solos e Unidades Pedológicas (Anexo 4.3.6-1)",
  categoria: "Ambiental e Geotécnica",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / PDA 2019 / IAC / EMBRAPA",
  marco_legal: "IAC (1999), EMBRAPA Solos, LCs nº 39/06, 40/06 e 41/06, Lei Estadual nº 11.579/03, Leis Federais nº 6.766/79 e 12.608/12",
  escala: "1:50.000",
  url: "data/pedologico_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#FFA77F",
  weight: 1.2,
  description: "5 Unidades Pedológicas Oficiais (IAC 1999 / EMBRAPA) · Argissolos Vermelho-Amarelos (PVA19, PVA41, PVA46, PVA55) e Latossolos (LVA17)",
  tags: ["pedologico", "solos", "argissolos", "latossolos", "cambissolos", "iac", "embrapa", "pda2019", "geotecnica"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#FFA77F";
    return {
      fillColor: cor,
      fillOpacity: 0.65,
      color: "#444444",
      weight: 1.2,
      opacity: 0.85
    };
  }
};

export default pedologicoConfig;
