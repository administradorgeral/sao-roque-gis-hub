/**
 * Camada: Vegetação Nativa Arbórea (Bioma Mata Atlântica)
 * Plano Diretor Ambiental de São Roque (PDA 2019) - Anexo 5.3.2.1-1
 * Cobertura Florestal Nativa Oficial: 15.613,05 ha (50,85% do território de São Roque)
 * Estágio Avançado e Médio (#267300 - 15.145,72 ha / 49,33%) e Estágio Inicial (#55FF00 - 467,33 ha / 1,52%)
 * Marco Legal: Lei Federal nº 11.428/2006 (Lei da Mata Atlântica), Decreto Federal nº 6.660/2008, 
 * Lei Federal nº 12.651/2012 (Código Florestal), Lei Estadual nº 11.579/2003 (APA Itupararanga) e LC Municipal nº 39/2006 (Arts. 60-64)
 */

export const vegetacaoArboreaConfig = {
  id: "vegetacao_arborea",
  name: "Vegetação Nativa Arbórea (Mata Atlântica)",
  categoria: "Cobertura Vegetal e Biodiversidade",
  esfera: "Federal / Estadual / Municipal",
  orgao: "Prefeitura de São Roque / CETESB / Fundação Florestal / IBAMA",
  marco_legal: "Lei Federal nº 11.428/06 (Mata Atlântica), Dec. Federal nº 6.660/08, Res. CONAMA 1/94, Lei Estadual nº 11.579/03, LC nº 39/06",
  escala: "1:35.000",
  url: "data/vegetacao_arborea_sao_roque_web.geojson",
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#267300",
  weight: 1.0,
  description: "Mapeamento oficial de Vegetação Nativa Arbórea (PDA 2019 / Anexo 5.3.2.1-1): 15.613,05 ha de remanescentes da Mata Atlântica (50,85% do município), compreendendo Estágio Avançado/Médio (15.145,72 ha / 49,33%) e Estágio Inicial (467,33 ha / 1,52%). Base do Ecoturismo e Patrimônio Natural da Estância Turística.",
  tags: ["vegetacao_arborea", "mata_atlantica", "floresta", "biodiversidade", "cetesb", "pda2019", "ecoturismo", "reserva_legal"],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const cod = props.codigo_classe || props.codigo;
    
    // 1. Estágio Inicial (#55FF00 - Verde Claro / Lima)
    if (cod === 'VN_INICIAL' || cod === 'VN_INI' || props.cor_hex === '#55FF00') {
      return {
        fillColor: "#55FF00",
        fillOpacity: 0.75,
        color: "#3BB300",
        weight: 1.0,
        opacity: 0.95
      };
    }
    
    // 2. Estágio Avançado e Médio (#267300 - Verde Escuro Florestal)
    return {
      fillColor: "#267300",
      fillOpacity: 0.70,
      color: "#1A4D00",
      weight: 1.0,
      opacity: 0.95
    };
  }
};

export default vegetacaoArboreaConfig;
