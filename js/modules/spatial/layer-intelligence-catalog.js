/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · CATÁLOGO DE INTELIGÊNCIA DAS 33 CAMADAS TERRITORIAIS
 * ===============================================================================
 * Desacoplado para prover à IA (Gemini 4 Argon) e ao Motor Espacial conhecimento
 * exaustivo e estruturado sobre TODAS as 33 camadas cartográficas oficiais.
 * ===============================================================================
 */

export const ALL_33_LAYERS = [
  {
    id: "declividade",
    nome: "Declividade do Terreno",
    categoria: "Geotécnica e Geomorfologia",
    fonte: "IGC / PDA 2018 (Anexo 4.3.3-1)",
    escala: "1:50.000 (SIRGAS 2000 UTM 23S)",
    legislacao_base: "Lei Federal nº 6.766/79 (Art. 3º), LC Municipal nº 40/2006 (Art. 13 e 43), Lei 12.651/12 (Art. 4º, V)",
    alerta_critico: "Ponto cego legal: o mapa agrupa 20% a 45% (Forte Ondulado), ocultando o teto legal impeditivo de 30% para parcelamento urbano e condomínios.",
    grau_restricao: "Impeditiva para declividade >= 30% sem estabilização e laudo geotécnico."
  },
  {
    id: "mdt",
    nome: "MDT - Relevo e Hipsometria",
    categoria: "Topografia e Hipsometria",
    fonte: "IGC / PDA 2018 (Anexo 4.3.2-2)",
    escala: "1:50.000",
    legislacao_base: "Lei Federal nº 12.651/12 (Código Florestal), ADPF 747/749 STF",
    alerta_critico: "Delimita fundos de vale sujeitos a inundações (630 a 760m) e topos de morro/cristas (Morro do Saboó, 1.125m) protegidos contra edificações.",
    grau_restricao: "Condicionante e protetiva de cumes e várzeas."
  },
  {
    id: "hidrografia",
    nome: "Hidrografia e Corpos Hídricos",
    categoria: "Recursos Hídricos e Saneamento",
    fonte: "IGC / DAEE / PDA 2019",
    escala: "1:10.000 / 1:50.000",
    legislacao_base: "Lei Federal nº 12.651/12 (Art. 4º), Lei Estadual nº 9.866/97, LC nº 40/06, Resolução CONAMA nº 357/05",
    alerta_critico: "APPs marginais obrigatórias (mínimo de 30m para cursos d'água < 10m e raio de 50m em nascentes). Vedado parcelamento em terrenos alagadiços.",
    grau_restricao: "Impeditiva total para edificações na faixa non aedificandi de APP."
  },
  {
    id: "geomorfologico",
    nome: "Compartimentos Geomorfológicos",
    categoria: "Geotécnica e Geomorfologia",
    fonte: "IPT / PDA 2019",
    escala: "1:50.000",
    legislacao_base: "Lei Federal nº 12.608/12 (Defesa Civil), LC Municipal nº 39/2006 (Art. 18)",
    alerta_critico: "Divide o município em Planalto de Ibiúna, Serras de São Roque e Colinas Médias, orientando a suscetibilidade a escorregamentos.",
    grau_restricao: "Diretriz estratégica para expansão urbana e contenção de encostas."
  },
  {
    id: "zoneamento",
    nome: "Zoneamento Municipal Homologado (LC 40/2006)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Prefeitura Municipal de São Roque / IGC (PMD 2006)",
    escala: "1:25.000",
    legislacao_base: "Lei Complementar nº 40/2006 (e alterações: LC 66/12, 99/18, 102/20, 106/20, 120/22, 128/23, 142/25)",
    alerta_critico: "Regime jurídico vigente e eficaz para alvarás, certidões de uso do solo, desdobros e fiscalização edilícia.",
    grau_restricao: "Regulamentadora de índices: TO, CA, gabaritos, recuos e usos admitidos."
  },
  {
    id: "geologia",
    nome: "Unidades Geológicas e Substrato Rochoso",
    categoria: "Geotécnica e Geomorfologia",
    fonte: "CPRM / PDA 2019",
    escala: "1:50.000",
    legislacao_base: "Código de Mineração (Decreto-Lei nº 227/67), LC Municipal nº 40/2006",
    alerta_critico: "Distingue o Complexo Granítico Ibiúna (sul), o Grupo São Roque (metassedimentos a norte) e coberturas coluvionares.",
    grau_restricao: "Condicionante para fundações profundas, poços artesianos e estabilidade de taludes."
  },
  {
    id: "fragilidade_potencial",
    nome: "Fragilidade Potencial e Erosão",
    categoria: "Ambiental e Geotécnica",
    fonte: "IPT / PDA 2019",
    escala: "1:50.000",
    legislacao_base: "Lei Federal nº 12.608/12, Lei nº 6.766/79",
    alerta_critico: "Mapeia as classes Muito Fraca a Muito Forte de risco a voçorocamento e perda de solo.",
    grau_restricao: "Impeditiva para desmatamento e terraplenagem sem plano de controle erosivo."
  },
  {
    id: "pedologico",
    nome: "Solos e Unidades Pedológicas",
    categoria: "Ambiental e Geotécnica",
    fonte: "Embrapa / Lepsch (1983) / PDA 2019",
    escala: "1:50.000",
    legislacao_base: "Lei Federal nº 6.766/79, LC nº 40/2006",
    alerta_critico: "Argissolos Vermelho-Amarelos (PVA) cobrem mais de 50% do município, com horizonte B textural suscetível a erosão sob chuvas concentradas.",
    grau_restricao: "Condicionante de drenagem, permeabilidade e taxa de infiltração."
  },
  {
    id: "zoneamento_ambiental_pda2019",
    nome: "Zoneamento Ambiental (PDA 2019)",
    categoria: "Ambiental e Geotécnica",
    fonte: "Plano Diretor Ambiental de São Roque (2019)",
    escala: "1:50.000",
    legislacao_base: "Decreto Municipal de Homologação do PDA 2019, Lei nº 9.985/00 (SNUC)",
    alerta_critico: "Classifica o território em ZPA, ZCA, ZOR e ZUR ambiental.",
    grau_restricao: "Condicionante para empreendimentos de impacto e compensação ambiental."
  },
  {
    id: "apa_itupararanga_limite",
    nome: "Limite Norte da APA Itupararanga",
    categoria: "Unidade de Conservação Estadual",
    fonte: "Fundação Florestal / IG / SMA",
    escala: "1:25.000",
    legislacao_base: "Lei Estadual nº 11.579/2003 (Art. 2º)",
    alerta_critico: "Linha do divisor hidrográfico setentrional da bacia do Rio Sorocaba, marco divisor entre bacias protegidas e bacias urbanas centrais.",
    grau_restricao: "Divisor legal de competência federativa estadual."
  },
  {
    id: "apa_itupararanga",
    nome: "Área de Proteção Ambiental da Represa de Itupararanga",
    categoria: "Unidade de Conservação Estadual",
    fonte: "Fundação Florestal / Decreto Estadual nº 52.879/2008",
    escala: "1:25.000",
    legislacao_base: "Lei Estadual nº 11.579/2003, Decreto nº 52.879/2008, Lei Estadual nº 9.866/97",
    alerta_critico: "Lote mínimo obrigatório de 1.000m² a 5.000m²; esgotamento autônomo com tratamento biológico auditado; vedado lançamento in natura e indústrias poluentes.",
    grau_restricao: "Impeditiva e restritiva com primazia de preservação de mananciais."
  },
  {
    id: "territorio_municipal",
    nome: "Território Municipal (São Roque)",
    categoria: "Planejamento Urbano e Governança Municipal",
    fonte: "IBGE / IGC (Área: 306,9 km²)",
    escala: "1:25.000",
    legislacao_base: "Constituição Federal (Arts. 30 e 182), Lei Orgânica Municipal de São Roque",
    alerta_critico: "Limite jurisdicional pleno da Estância Turística de São Roque.",
    grau_restricao: "Marco de competência executiva e legislativa de ordenamento territorial."
  },
  {
    id: "zona_protecao_aeroportuaria_catarina",
    nome: "Proteção Aeroportuária Catarina (SBJH / DECEA)",
    categoria: "Infraestrutura Aeronáutica e Servidão Federal",
    fonte: "DECEA / COMAER / ANAC (Plano Básico de Zona de Proteção)",
    escala: "Oficial DECEA (Superfícies Cônicas e de Aproximação)",
    legislacao_base: "Lei Federal nº 7.565/86 (CBA - Arts. 43 a 46), Portaria DECEA, RBAC 139",
    alerta_critico: "Gabaritos de altura absoluta para edificações, antenas e postes; servidão aeronáutica federal com prevalência sobre a lei municipal.",
    grau_restricao: "Impeditiva aeronáutica absoluta para alturas que violem as superfícies limitadoras."
  },
  {
    id: "ahs",
    nome: "Áreas Hidrologicamente Sensíveis (AHS)",
    categoria: "Recursos Hídricos e Proteção Ambiental",
    fonte: "PDA 2019 / IGC",
    escala: "1:25.000",
    legislacao_base: "Lei Federal nº 9.433/97, Lei Estadual nº 9.866/97",
    alerta_critico: "Várzeas e zonas de recarga do aquífero freático com alta permeabilidade.",
    grau_restricao: "Condicionante severa com vedação a impermeabilização massiva."
  },
  {
    id: "vegetacao_arborea",
    nome: "Vegetação Nativa Arbórea (Mata Atlântica)",
    categoria: "Cobertura Vegetal e Biodiversidade",
    fonte: "Inventário Florestal do Estado de SP / SMA / PDA 2019",
    escala: "1:25.000",
    legislacao_base: "Lei Federal nº 11.428/2006 (Lei da Mata Atlântica), Decreto Federal nº 6.660/08",
    alerta_critico: "Proibição de supressão de vegetação primária ou secundária em estágio avançado.",
    grau_restricao: "Impeditiva com necessidade de autorização prévia da CETESB / DEPAVE."
  },
  {
    id: "rbcv_cinturao_verde",
    nome: "Reserva da Biosfera do Cinturão Verde (UNESCO)",
    categoria: "Patrimônio Internacional e Governança Regional (UNESCO)",
    fonte: "Instituto Florestal / Programa MAB UNESCO (1994)",
    escala: "Regional (Fator de Integração)",
    legislacao_base: "Lei Federal nº 9.985/2000 (SNUC - Art. 41), Diretrizes Internacionais MAB/UNESCO",
    alerta_critico: "Proteção das funções ecossistêmicas e da paisagem cultural e gastronômica regional.",
    grau_restricao: "Diretriz sustentável internacional para agroecologia e turismo ordenado."
  },
  {
    id: "distritos",
    nome: "Divisão Distrital Oficial",
    categoria: "Divisão Político-Administrativa e Cidadania",
    fonte: "IBGE / Prefeitura Municipal de São Roque (4 Distritos)",
    escala: "1:25.000",
    legislacao_base: "Lei Complementar nº 39/2006, Legislação Estadual de Divisão Territorial",
    alerta_critico: "Quatro polos administrativos: Distrito Sede, Distrito de Maylasky, Distrito de São João Novo e Distrito de Canguera.",
    grau_restricao: "Marco de descentralização de serviços e planejamento comunitário."
  },
  {
    id: "setores_censitarios",
    nome: "Setores Censitários (IBGE Censo 2022)",
    categoria: "Demografia e Estatística Territorial",
    fonte: "IBGE (188 setores censitários)",
    escala: "1:10.000",
    legislacao_base: "Lei Federal nº 5.534/1968 (Estatística Pública)",
    alerta_critico: "Base de microdados populacionais, densidade demográfica real e carências habitacionais.",
    grau_restricao: "Base diagnóstica socioespacial."
  },
  {
    id: "logradouros",
    nome: "Sistema Viário e Logradouros (3.222 Ruas)",
    categoria: "Infraestrutura Urbana e Mobilidade",
    fonte: "Cadastro Técnico Multifinalitário / OpenStreetMap / PMS São Roque",
    escala: "Cadastral (1:2.000)",
    legislacao_base: "Lei Federal nº 9.503/1997 (CTB), LC nº 40/2006 (Hierarquia Viária)",
    alerta_critico: "Rede conectada com larguras de caixa, hierarquia (arterial, coletora, local) e obras da Carta XIII.",
    grau_restricao: "Regulamentadora de recuos e acessibilidade."
  },
  {
    id: "revisao_plano_diretor_2026",
    nome: "Revisão do Plano Diretor Municipal (2024–2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Prefeitura Municipal de São Roque / DPMA / Audiências Públicas",
    escala: "Processual / Normativa",
    legislacao_base: "Estatuto da Cidade (Lei 10.257/01 Arts. 39 a 42-B), Minuta Revisão LC 39 e 40",
    alerta_critico: "Proposta em tramitação legislativa que consolida as 13 Cartas e as 22 Obras Estruturantes.",
    grau_restricao: "Regime Proposto em debate público."
  },
  {
    id: "carta_01_macrozoneamento_2026",
    nome: "Carta I: Macrozoneamento Municipal (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Minuta da nova LC do Plano Diretor (Revisão LC 39), Estatuto da Cidade Art. 42-B",
    alerta_critico: "Fixa as 4 Macrozonas: Consolidação Urbana, Urbanização Específica (ZUE), Proteção Ambiental e Rural.",
    grau_restricao: "Diretriz macrozonal compulsória."
  },
  {
    id: "carta_02_zue_2026",
    nome: "Carta II: Zoneamento da ZUE (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadro VII), Lei Estadual nº 11.579/03",
    alerta_critico: "Disciplina ZUE de Interesse Turístico (Roteiro do Vinho) e ZUE Chácaras em Manancial.",
    grau_restricao: "Condicionante ambiental e de baixíssima densidade construtiva."
  },
  {
    id: "carta_03_consolidacao_urbana_2026",
    nome: "Carta III: Consolidação Urbana - Geral (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadros I a VI)",
    alerta_critico: "Perímetros urbanos contínuos e articulados dos quatro distritos.",
    grau_restricao: "Delimitação do perímetro urbano para fins de incidência tributária e IPTU."
  },
  {
    id: "carta_04_sede_2026",
    nome: "Carta IV: Consolidação Urbana - Distrito Sede (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadros I e II)",
    alerta_critico: "Zoneamento de adensamento qualificado na Sede (ZUR, ZUC, ZUI) com fachadas ativas.",
    grau_restricao: "Regulamentadora de coeficientes de aproveitamento e gabaritos centrais."
  },
  {
    id: "carta_05_maylasky_2026",
    nome: "Carta V: Consolidação Urbana - Maylasky (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadro III)",
    alerta_critico: "Reconhecimento das demandas de desdobro familiar de chácaras de 500m² sob condição de 55% permeável.",
    grau_restricao: "Condicionante de saneamento autônomo e drenagem local."
  },
  {
    id: "carta_06_sao_joao_novo_2026",
    nome: "Carta VI: Consolidação Urbana - São João Novo (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadro IV)",
    alerta_critico: "Eixos habitacionais e regularização de núcleos do vale do Carambeí.",
    grau_restricao: "Condicionante de afastamento da faixa de domínio ferroviário da concessionária Rumo."
  },
  {
    id: "carta_07_canguera_2026",
    nome: "Carta VII: Consolidação Urbana - Canguera (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadro V), Lei Estadual nº 11.579/03",
    alerta_critico: "Compatibilização entre o núcleo urbano consolidado e a bacia de mananciais de Itupararanga.",
    grau_restricao: "Restritiva ambiental com vedação a sobrecarga de densidade."
  },
  {
    id: "carta_08_corredores_2026",
    nome: "Carta VIII: Corredores de Comércio, Serviços e Turismo (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Minuta Revisão LC 40/2006 (Quadro VIII), Lei Federal nº 9.503/97",
    alerta_critico: "Eixos ao longo da Raposo Tavares, Lívio Tagliassachi, Estrada do Vinho e Marginal Aracaí.",
    grau_restricao: "Regulamentadora de recuos comerciais e estacionamento obrigatório."
  },
  {
    id: "carta_09_aeis_2026",
    nome: "Carta IX: Áreas de Especial Interesse - AEIS, AEIT, AEIU (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Lei Federal nº 13.465/2017 (REURB), Estatuto da Cidade (Lei 10.257/01 Art. 4º)",
    alerta_critico: "Instrumento prioritário de moradia digna, regularização jurídica de posse e investimentos públicos.",
    grau_restricao: "Condicionante de elaboração de plano de urbanização específica."
  },
  {
    id: "carta_10_viario_sede_2026",
    nome: "Carta X: Sistema Viário e Drenagem - Sede (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 39/2006 (Arts. 80 a 86), Lei Federal nº 12.587/2012",
    alerta_critico: "Projetos de canalização, piscinões e novas avenidas marginais para mitigar enchentes no centro.",
    grau_restricao: "Diretriz prioritária de drenagem pluvial e mobilidade ativa."
  },
  {
    id: "carta_11_viario_maylasky_2026",
    nome: "Carta XI: Sistema Viário e Drenagem - Maylasky (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "Minuta Revisão LC 39/2006 (Arts. 87 a 91), Normas ARTESP / DER-SP",
    alerta_critico: "Adequação dos acessos perigosos à Rodovia Raposo Tavares (SP-270) e travessias seguras.",
    grau_restricao: "Condicionante de segurança viária interdistrital."
  },
  {
    id: "carta_12_viario_canguera_2026",
    nome: "Carta XII: Sistema Viário e Drenagem - Canguera (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:10.000",
    legislacao_base: "LC Municipal nº 140/2025 (PDTur), Lei Estadual nº 11.579/03 (Art. 6º)",
    alerta_critico: "Pavimentação com dissipadores de energia na Estrada do Vinho para conter erosão de sedimentos na APA.",
    grau_restricao: "Condicionante de drenagem sustentável na bacia de mananciais."
  },
  {
    id: "carta_13_obras_prioritarias_2026",
    nome: "Carta XIII: 22 Obras Estruturantes Prioritárias (2026)",
    categoria: "Planejamento Urbano e Ordenamento Territorial",
    fonte: "Plano Diretor 2026 (DPMA)",
    escala: "1:25.000",
    legislacao_base: "Art. 182 da CF/88, Minuta Revisão LC 39/2006 (Art. 102 - Quadro de Obras)",
    alerta_critico: "As 22 intervenções fundamentais: SRQ-01 a SRQ-22 (piscinões Aracaí, ciclovias, viadutos, Parque Saboó).",
    grau_restricao: "Vinculação ao Plano Plurianual (PPA) e à Lei de Diretrizes Orçamentárias (LDO)."
  }
];

export const ALL_33_LAYERS_MAP = new Map(ALL_33_LAYERS.map(l => [l.id, l]));

export class LayerIntelligenceCatalog {
  static getAllLayers() {
    return ALL_33_LAYERS;
  }

  static getLayer(layerId) {
    return ALL_33_LAYERS_MAP.get(layerId) || null;
  }

  static searchLayers(query) {
    if (!query) return [];
    const q = query.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
    return ALL_33_LAYERS.filter(l => {
      const nomeNorm = l.nome.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      const catNorm = l.categoria.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
      const idNorm = l.id.toLowerCase().replace(/_/g, " ");
      return nomeNorm.includes(q) || catNorm.includes(q) || idNorm.includes(q);
    });
  }
}
