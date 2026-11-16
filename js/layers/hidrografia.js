/**
 * Camada: Hidrografia e Corpos Hídricos (Anexo 4.3.7-1 - PDA 2019 / IGC 1978 / SABESP)
 * Rede Hidrográfica Vetorial Nativa (Rios, Córregos, Represas e Nascentes)
 * SIRGAS 2000 UTM 23S (EPSG: 31983)
 */

export const hidrografiaConfig = {
  id: "hidrografia",
  name: "Hidrografia e Corpos Hídricos (Anexo 4.3.7-1)",
  categoria: "Recursos Hídricos e Saneamento",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / IGC SP / SABESP",
  marco_legal: "Lei Federal nº 12.651/2012 (Art. 4º), Lei Federal nº 6.766/1979 (Art. 3º e 4º), Lei Estadual nº 11.579/2003 (APA Itupararanga), Lei Estadual nº 9.866/1997 (Mananciais SP), Resolução CONAMA nº 357/2005 e LC Municipal nº 39/2006 (Arts. 60-64 - Zonas de Proteção aos Mananciais)",
  escala: "1:50.000",
  url: "data/hidrografia_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.85,
  cor: "#00A2E8",
  weight: 2,
  description: "972 km de Cursos d'Água e 2.355 ha de Represas · Vetor Nativo SIRGAS 2000",
  tags: ["hidrografia", "rios", "corregos", "represas", "itupararanga", "app_hidrica", "nascentes", "sabesp", "pda2019"],
  
  // Função de estilo dinâmica para Linhas e Polígonos
  style: (feature) => {
    const props = (feature && feature.properties) || {};
    const geomType = (feature && feature.geometry && feature.geometry.type) || "";
    const isPoly = geomType.includes("Polygon");
    const cor = props.cor_hex || "#00A2E8";
    
    if (isPoly) {
      return {
        fillColor: cor,
        fillOpacity: 0.75,
        color: "#0077BE",
        weight: 1,
        opacity: 0.95
      };
    } else {
      const isMain = (props["Tipo de Feição"] || "").includes("Principal");
      return {
        color: cor,
        weight: isMain ? 2.5 : 1.5,
        opacity: 0.90
      };
    }
  }
};

export default hidrografiaConfig;
