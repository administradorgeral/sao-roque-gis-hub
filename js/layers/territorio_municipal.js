/**
 * Camada: Território Municipal (Estância Turística de São Roque)
 * Limite Municipal Contínuo Oficial (IBGE Censo 2022 - Cód. 3550605)
 * Base de Governança, Plano Diretor (LC 39/06) e Regime de Estância Turística (Lei Estadual nº 6.899/90 / LCE nº 1.261/15 / LC nº 140/25)
 * Vetor Nativo de Alta Precisão (SIRGAS 2000 UTM 23S) - 30.701,47 ha / 115,35 km de Perímetro
 */

export const territorioMunicipalConfig = {
  id: "territorio_municipal",
  name: "Território Municipal (Estância Turística)",
  categoria: "Planejamento Urbano e Governança Municipal",
  esfera: "Municipal / Estadual",
  orgao: "Prefeitura da Estância Turística de São Roque / IBGE (Cód. 3550605)",
  marco_legal: "Lei Orgânica nº 1.801/90, Lei Estadual nº 6.899/90, LCE nº 1.261/15, LC nº 39/06, LC nº 140/25, Lei nº 2.871/04",
  escala: "1:50.000",
  url: "data/territorio_municipal_sao_roque_web.geojson",
  defaultVisible: true,
  defaultOpacity: 0.85,
  cor: "#D4AF37",
  weight: 2.2,
  description: "Contorno municipal oficial contínuo (30.701,47 ha / 115,35 km de perímetro) · Regime Jurídico de Estância Turística, DADETUR, Plano Diretor (LC 39/06) e PDTur (LC 140/25)",
  tags: ["territorio_municipal", "estancia_turistica", "plano_diretor", "pdtur", "comtur", "dadetur", "ibge3550605"],
  
  style: (feature) => {
    return {
      fillColor: "#D4AF37",
      fillOpacity: 0.12,
      color: "#1E293B",
      weight: 2.2,
      opacity: 0.95,
      dashArray: null
    };
  }
};

export default territorioMunicipalConfig;
