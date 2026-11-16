/**
 * Camada: Carta VIII - Corredores de Comércio, Serviços e Turismo (Revisão do Plano Diretor 2024–2026)
 * Base Legal: Arts. 151 a 165 da Minuta de Revisão da LC nº 40/2006 (Revisão 05 - Agosto/2026)
 * Autoria Técnica: Eng. Civil David de Mello Berger (CREA: 5070025188)
 */

export const carta08Corredores2026Config = {
  id: "carta_08_corredores_2026",
  name: "Carta VIII: Corredores de Comércio, Serviços e Turismo (Plano Diretor 2026)",
  categoria: "Planejamento Urbano e Ordenamento Territorial",
  esfera: "Municipal",
  orgao: "Prefeitura da Estância Turística de São Roque / DPMA",
  marco_legal: "Arts. 151 a 165 da Minuta de Revisão da LC nº 40/2006 (Agosto/2026 - Revisão 05)",
  escala: "1:25.000 (Indicada)",
  rasterUrl: "data/carta_08_corredores_mapa.png?v=20261115_transp",
  rasterBounds: [[-23.65394, -47.20889], [-23.41153, -46.99093]],
  url: "data/territorio_municipal_sao_roque_web.geojson",
  style: (feature) => ({
    color: "#2563EB",
    weight: 2.5,
    fillOpacity: 0.0,
    opacity: 0.95
  }),
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#F59E0B",
  weight: 2.0,
  description: "Carta VIII Oficial da Revisão do Plano Diretor: Corredores de Comércio, Serviços e Turismo ao longo dos eixos estruturantes (Estrada do Vinho, Rod. Raposo Tavares SP-270, Rod. Lívio Tagliassachi, Rod. Quintino de Lima SP-077 e Rod. Engº Renê Benedito da Silva).",
  tags: ["plano_diretor_2026", "carta_08", "corredores_comerciais", "rota_do_vinho", "turismo", "raposo_tavares"]
};

export default carta08Corredores2026Config;
