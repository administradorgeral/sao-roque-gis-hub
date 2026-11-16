/**
 * Camada: Fragilidade Potencial do Município de São Roque
 * Anexo 7.3.1-1 - Plano Diretor Ambiental (PDA 2019)
 * Metodologia Ross (1994) / Crepani et al. (2008) / IPT (1981) / CPRM (2006)
 * Vetor Nativo de Alta Precisão (SIRGAS 2000 UTM 23S) - 5 Classes Morfodinâmicas
 */

export const fragilidadePotencialConfig = {
  id: "fragilidade_potencial",
  name: "Fragilidade Potencial e Erosão (Anexo 7.3.1-1)",
  categoria: "Ambiental e Geotécnica",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / PDA 2019",
  marco_legal: "Ross (1994), Crepani et al. (2008), LCs nº 39/06, 40/06 e 41/06, Leis Federais nº 6.766/79 e 12.608/12",
  escala: "1:50.000",
  url: "data/fragilidade_potencial_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.65,
  cor: "#FF0000",
  weight: 0.8,
  description: "5 Classes de Fragilidade Potencial e Vulnerabilidade à Erosão (Ross 1994 / PDA 2019) · Muito Fraca, Fraca, Média, Forte e Muito Forte",
  tags: ["fragilidade_potencial", "erosao", "vulnerabilidade", "ross", "crepani", "pda2019", "geotecnica", "relevo"],
  
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const cor = props.cor_hex || "#FFFF00";
    return {
      fillColor: cor,
      fillOpacity: 0.65,
      color: "#222222",
      weight: 0.8,
      opacity: 0.85
    };
  }
};

export default fragilidadePotencialConfig;
