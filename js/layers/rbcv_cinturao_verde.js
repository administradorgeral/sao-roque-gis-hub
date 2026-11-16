/**
 * Camada: Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo (RBCV / UNESCO)
 * Programa O Homem e a Biosfera (Man and the Biosphere - MaB / UNESCO 1994)
 * Marco Estatutário da Rede Mundial de Reservas da Biosfera (Resolução 28 C/2.4 UNESCO 1995)
 * Marco Legal Federal: Lei Federal nº 9.985/2000 (SNUC Art. 41), Dec. 4.340/2002, Dec. 12.035/2024 (COBRAMAB)
 * Marco Estadual e Municipal: Dec. Estadual nº 47.094/2002, LC Municipal nº 39/2006 (Arco Florestal da Macrozona Rural) e Lei nº 2.499/1999 (Parque Mata da Câmara - Zona Núcleo)
 * Abrangência Macroregional: 73 municípios paulistas (Macrometrópole e Interior)
 */

export const rbcvCinturaoVerdeConfig = {
  id: "rbcv_cinturao_verde",
  name: "Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
  categoria: "Patrimônio Internacional e Governança Regional",
  esfera: "Internacional / Federal / Estadual",
  orgao: "UNESCO / MaB / COBRAMAB / Instituto Florestal / Fundação Florestal",
  marco_legal: "Resolução 28 C/2.4 UNESCO, Lei Federal nº 9.985/00 (Art. 41), Dec. 12.035/24, Dec. Est. 47.094/02, LC nº 39/06",
  escala: "1:1.300.000 (Macroregional)",
  url: "data/rbcv_cinturao_verde_web.geojson",
  rasterUrl: "data/rbcv_cinturao_verde_regional.png?v=20261115_depara",
  rasterBounds: [[-25.35371, -47.53558], [-22.44058, -45.30193]],
  defaultVisible: false,
  defaultOpacity: 0.75,
  cor: "#38A800",
  weight: 2.2,
  description: "Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo (RBCV / UNESCO 1994): Abrange São Roque e 72 municípios paulistas. Zonas-Núcleo de proteção integral estrita (Parque da Mata da Câmara), Zonas de Amortecimento (APA Itupararanga) e Perímetro Regional Homologado.",
  tags: ["rbcv", "cinturao_verde", "unesco", "mab", "reserva_biosfera", "cobramab", "mata_atlantica", "mata_da_camara", "patrimonio_mundial"],
  
  style: (feature) => {
    const props = feature?.properties || {};
    const cod = props.codigo;

    // 1. Limite Oficial RBCV (Linha regional contínua)
    if (cod === 'RBCV_LIMITE' || props.id === 'rbcv_limite') {
      return {
        color: "#0F172A",
        weight: 2.5,
        opacity: 1.0,
        dashArray: "6, 4",
        fill: false
      };
    }

    // 2. Zonas-Núcleo (Verde Esmeralda - Proteção Integral Estrita)
    return {
      fillColor: "#38A800",
      fillOpacity: 0.65,
      color: "#267300",
      weight: 1.5,
      opacity: 0.95
    };
  }
};

export default rbcvCinturaoVerdeConfig;
