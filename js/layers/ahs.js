/**
 * Camada: Áreas Hidrologicamente Sensíveis (AHS)
 * Plano Diretor Ambiental de São Roque (PDA 2019) - Anexo 4.2.5.1-1
 * Proteção de Nascentes, Cursos d'Água, Várzeas e Recarga de Aquíferos
 * Código Florestal (Lei Federal nº 12.651/2012), Lei Estadual nº 9.866/1997 e LC Municipal nº 39/2006 (Arts. 60-64)
 * Vetor Nativo de Alta Precisão (7.527 polígonos dissolvidos contínuos / 7.514,71 ha / 24,48% do território)
 */

export const ahsConfig = {
  id: "ahs",
  name: "Áreas Hidrologicamente Sensíveis (AHS)",
  categoria: "Recursos Hídricos e Proteção Ambiental",
  esfera: "Federal / Estadual / Municipal",
  orgao: "Prefeitura de São Roque / DAEE / CETESB / Fundação Florestal",
  marco_legal: "Lei Federal nº 12.651/12 (Arts. 4º e 6º), Lei Estadual nº 9.866/97, Lei Estadual nº 11.579/03, LC nº 39/06 (Arts. 60-64)",
  escala: "1:35.000",
  url: "data/ahs_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.70,
  cor: "#A80084",
  weight: 1.2,
  description: "Mapeamento oficial de Áreas Hidrologicamente Sensíveis (AHS - PDA 2019 / Anexo 4.2.5.1-1): APPs de cursos d'água (30m a 100m) e nascentes (raio 50m), várzeas inundáveis e planícies aluviais (7.514,71 ha / 24,48% de São Roque).",
  tags: ["ahs", "hidrografia_sensivel", "apps", "nascentes", "recursos_hidricos", "pda2019", "mananciais", "codigo_florestal"],
  
  style: (feature) => {
    return {
      fillColor: "#A80084",
      fillOpacity: 0.65,
      color: "#700058",
      weight: 1.2,
      opacity: 0.95
    };
  }
};

export default ahsConfig;
