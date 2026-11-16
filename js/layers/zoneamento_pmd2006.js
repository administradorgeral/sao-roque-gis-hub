/**
 * Camada: Zoneamento Municipal PMD 2006
 * Módulo individual para a camada de zoneamento homologado
 * Pode ser adicionado/removido independentemente do código principal
 */

export const zoneamentoConfig = {
  id: "zoneamento",
  name: "Zoneamento Municipal (Plano Diretor e Uso do Solo)",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque",
  marco_legal: "LC nº 39/2006 (Plano Diretor Estratégico), LC nº 40/2006 (Uso e Ocupação do Solo), LC nº 41/2006 (Código de Obras) e Lei Federal nº 10.257/2001 (Estatuto da Cidade)",
  escala: "1:10.000",
  url: "data/pmsr_zoneamento_pmd2006.geojson",
  defaultVisible: true,
  defaultOpacity: 0.55,
  cor: "#7c3aed",
  weight: 2,
  description: "31 Zonas Territoriais · LCs 39/06 e 40/06 · 14.974 Vértices",
  tags: ["zoneamento", "municipal", "homologado", "pmd2006", "lc39", "lc40", "plano_diretor"]
};

export default zoneamentoConfig;

