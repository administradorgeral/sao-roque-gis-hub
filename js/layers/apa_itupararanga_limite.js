/**
 * Camada: Limite Norte da APA da Represa de Itupararanga
 * Linha Divisória Oficial Estadual (Lei Estadual nº 11.579/2003 / Decreto Estadual nº 52.879/2008)
 * Vetor Nativo de Alta Precisão (SIRGAS 2000 UTM 23S) - 18,59 km de Extensão
 */

export const apaItupararangaLimiteConfig = {
  id: "apa_itupararanga_limite",
  name: "APA da Represa de Itupararanga",
  categoria: "Unidade de Conservação Estadual",
  esfera: "Estadual",
  orgao: "Governo do Estado de São Paulo / Fundação Florestal / SEMIL-SP",
  marco_legal: "Lei Estadual nº 11.579/2003, Decreto Estadual nº 52.879/2008, Lei Estadual nº 9.866/1997, LCs Municipais nº 39/06 e 40/06",
  escala: "1:50.000",
  url: "data/apa_itupararanga_limite_sao_roque_web.geojson",
  defaultVisible: true,
  defaultOpacity: 0.85,
  cor: "#0070FF",
  weight: 2,
  description: "Área de Proteção Ambiental da Represa de Itupararanga: Polígono Territorial Sul (10.805,84 ha / 35,19% do município) delimitado ao norte pela linha divisória oficial de águas (18,59 km)",
  tags: ["apa_itupararanga", "limite_norte", "mananciais", "estadual", "fundacao_florestal", "semil", "lei11579"],
  
  style: (feature) => {
    const geomType = feature?.geometry?.type;
    const props = feature?.properties || {};
    const isLine = geomType === 'LineString' || 
                   props.codigo === 'LIMITE_NORTE_APA' || 
                   props.tipo_elemento === 'Linha Limite Setentrional';

    if (isLine) {
      return {
        color: "#E60000",
        weight: 3.5,
        opacity: 1.0,
        dashArray: "8, 4",
        lineCap: "round",
        lineJoin: "round"
      };
    }

    // Polígono Territorial da APA ao Sul da Linha (10.805,84 ha / 35,19% de São Roque)
    return {
      fillColor: props.cor_hex || "#0070FF",
      fillOpacity: 0.28,
      color: props.cor_borda || "#E60000",
      weight: 1.8,
      opacity: 0.9,
      dashArray: null
    };
  }
};

export default apaItupararangaLimiteConfig;
