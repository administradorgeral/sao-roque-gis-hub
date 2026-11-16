/**
 * Camada: Sistema Viário e Logradouros de São Roque (SP)
 * 4.868 Trechos de Vias e 3.241 Logradouros Cadastrados
 * Rodovias (Castello Branco, Raposo Tavares, Quintino de Lima), Estradas Turísticas (Roteiro do Vinho), Avenidas e Ruas Residenciais
 * Base: OpenStreetMap 2024/2026, DER-SP e Plano Diretor (LC nº 39/06 e LC nº 40/06)
 */

export const logradourosConfig = {
  id: "logradouros",
  name: "Sistema Viário e Logradouros (3.241 Ruas)",
  categoria: "Infraestrutura Urbana e Mobilidade",
  esfera: "Municipal / Estadual / Federal",
  orgao: "Prefeitura de São Roque / DER-SP / CCR ViaOeste / OpenStreetMap",
  marco_legal: "Código de Trânsito Brasileiro (Lei nº 9.503/97), LC nº 40/06 (Sistema Viário e Recuos)",
  escala: "1:10.000",
  url: "data/logradouros_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.85,
  cor: "#475569",
  weight: 2.0,
  description: "Malha completa de logradouros de São Roque (3.241 ruas, avenidas, alamedas e estradas turísticas), com classificação hierárquica, tipo de pavimentação e sentidos de circulação.",
  tags: ["logradouros", "ruas", "sistema_viario", "enderecos", "mobilidade", "rodovias", "roteiro_do_vinho"],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const t = props.tipo_via || "";
    
    // 1. Rodovias Principais (Castello Branco, Raposo Tavares, Rod. Quintino de Lima)
    if (t === 'motorway' || t === 'trunk' || t === 'primary') {
      return {
        color: "#DC2626",
        weight: 3.2,
        opacity: 0.95
      };
    }
    
    // 2. Avenidas Coletoras e Estradas Turísticas (Estrada do Vinho, etc.)
    if (t === 'secondary' || t === 'tertiary') {
      return {
        color: "#D97706",
        weight: 2.2,
        opacity: 0.90
      };
    }
    
    // 3. Ruas Locais, Residenciais e Alamedas
    return {
      color: "#64748B",
      weight: 1.4,
      opacity: 0.80
    };
  }
};

export default logradourosConfig;
