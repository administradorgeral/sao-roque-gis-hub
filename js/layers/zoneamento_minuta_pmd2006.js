/**
 * Camada: Minuta do Zoneamento PMD 2006
 * Módulo individual para a camada de minuta de zoneamento
 * Pode ser adicionado/removido independentemente do código principal
 */

export const minutaZoneamentoConfig = {
  id: "minuta-zoneamento",
  name: "Minuta do Zoneamento (Estudo Técnico PMD 2006)",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque",
  marco_legal: "Estudo Técnico Urbanístico / Minuta Técnica",
  escala: "1:10.000",
  url: "data/pmsr_zoneamento_minuta_pmd2006.geojson",
  defaultVisible: false,
  defaultOpacity: 0.50,
  cor: "#007fff",
  weight: 2,
  description: "33 Zonas/Polígonos · 14.638 Vértices · Áreas e Perímetros",
  tags: ["zoneamento", "municipal", "minuta", "estudo-tecnico", "pmd2006"]
};

export default minutaZoneamentoConfig;

