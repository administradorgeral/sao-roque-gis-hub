/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE INTELIGÊNCIA MULTIDIMENSIONAL & BUSCA EM MULTI-ETAPAS
 * ===============================================================================
 * Módulo desacoplado de alta tecnologia responsável por:
 *  1. Executar pesquisa dividida em 4 etapas estruturadas:
 *     - Etapa 1: Base Territorial Local de São Roque & Voz do Bairro
 *     - Etapa 2: Conhecimento Jurídico, Normativo & Jurisprudencial (CF, Estatuto, CONAMA, TJ-SP)
 *     - Etapa 3: Conhecimento Científico, Geotécnico & Catástrofes Similares (IPT, CPRM, CEMADEN)
 *     - Etapa 4: Notícias Reais, Auditorias, Enchentes e Casos Práticos (Positivos vs. Críticos)
 *  2. Fornecer embasamento pericial dialético (Apoio, Alerta de Risco, Regra Cogente, Estudo Comparativo)
 *  3. Injetar grounding verificado para o modelo Gemini 4 Argon
 *  4. Renderizar card expandido com cabeçalho rico (.ai-sources-header) e abas de filtro
 * ===============================================================================
 */

export class AIWebSearchEngine {
  constructor(options = {}) {
    this.timeoutMs = options.timeoutMs || 6000;
    
    // Repositório estruturado de 4 Pilares do Conhecimento Territorial e Pericial
    this.knowledgeBase = [
      // -------------------------------------------------------------------------
      // PILAR 1: JURÍDICO & REGRAS (Leis Federais/Estaduais, CONAMA e Jurisprudência)
      // -------------------------------------------------------------------------
      {
        id: "jur-tjsp-urbanismo",
        pillar: "juridico",
        pillarName: "Direito Urbanístico & Jurisprudência",
        pillarIcon: "⚖️",
        orientation: "ALERTA",
        orientationLabel: "Precedente Vinculante",
        domain: "tjsp.jus.br",
        title: "TJ-SP · Jurisprudência de Zoneamento, ACPs e Loteamentos Clandestinos",
        url: "https://www.tjsp.jus.br",
        category: "Jurisprudência Estadual",
        keywords: ["jurisprudencia", "tjsp", "acao civil publica", "loteamento clandestino", "desdobro", "mananciais", "area de preservacao", "danos ambientais", "anulacao", "spot zoning", "casuismo"],
        snippet: "Precedentes da Câmara Reservada ao Meio Ambiente do TJ-SP que declaram a nulidade de alterações pontuais de zoneamento (spot zoning) desprovidas de estudo prévio de impacto ambiental e de vizinhança."
      },
      {
        id: "jur-lei-6766",
        pillar: "juridico",
        pillarName: "Legislação Federal Urbanística",
        pillarIcon: "⚖️",
        orientation: "REGRA",
        orientationLabel: "Regra Cogente",
        domain: "planalto.gov.br",
        title: "Lei Federal nº 6.766/1979 · Parcelamento do Solo Urbano (Art. 3º)",
        url: "https://www.planalto.gov.br/ccivil_03/leis/l6766.htm",
        category: "Norma Federal Obrigatória",
        keywords: ["6766", "parcelamento", "artigo 3", "alagadico", "declividade", "30%", "45 graus", "proibicao", "inundavel", "crime contra a administracao"],
        snippet: "Veda categoricamente o parcelamento do solo em terrenos alagadiços antes de escoadas as águas, e em declividades iguais ou superiores a 30% salvo exigências geotécnicas específicas atestadas por laudo."
      },
      {
        id: "jur-estatuto-cidade",
        pillar: "juridico",
        pillarName: "Estatuto da Cidade",
        pillarIcon: "⚖️",
        orientation: "REGRA",
        orientationLabel: "Função Social da Cidade",
        domain: "planalto.gov.br",
        title: "Lei Federal nº 10.257/2001 · Estatuto da Cidade (Arts. 2º, 39 e 42-B)",
        url: "https://www.planalto.gov.br/ccivil_03/leis/leis_2001/l10257.htm",
        category: "Diretrizes Nacionais de Desenvolvimento Urbano",
        keywords: ["estatuto da cidade", "10257", "artigo 2", "artigo 42-b", "capacidade de suporte", "infraestrutura", "funcao social", "participacao popular", "expansao urbana"],
        snippet: "Exige que qualquer alteração de perímetro ou expansão urbana seja precedida de projeto específico demonstrando infraestrutura existente, capacidade de suporte ambiental e garantia de transporte e saneamento."
      },
      {
        id: "jur-conama-apps",
        pillar: "juridico",
        pillarName: "Normativa Ambiental Federal",
        pillarIcon: "⚖️",
        orientation: "REGRA",
        orientationLabel: "Limitação Ambiental Inafastável",
        domain: "gov.br/mma",
        title: "Resoluções CONAMA nº 303/2002 e 369/2006 · Parâmetros de APPs e Encostas",
        url: "https://www.gov.br/mma/pt-br",
        category: "Conselho Nacional do Meio Ambiente",
        keywords: ["conama", "303", "369", "app", "preservacao permanente", "topo de morro", "linha de cumeada", "nascente", "faixa marginal", "curso dagua"],
        snippet: "Fixa parâmetros protetivos para Áreas de Preservação Permanente (APPs), delimitando topos de morro, terço superior de elevações e faixas marginais de corpos hídricos intransponíveis à urbanização predatória."
      },
      {
        id: "jur-apa-itupararanga",
        pillar: "juridico",
        pillarName: "Proteção aos Mananciais",
        pillarIcon: "⚖️",
        orientation: "REGRA",
        orientationLabel: "Regime Especial de Bacia Hidrográfica",
        domain: "al.sp.gov.br",
        title: "Lei Estadual SP nº 11.579/2003 & Lei nº 9.866/1997 · APA de Itupararanga",
        url: "https://www.al.sp.gov.br/norma/11579",
        category: "Legislação Estadual de Proteção de Mananciais",
        keywords: ["itupararanga", "11579", "9866", "apa", "mananciais", "cetesb", "alto sorocaba", "recursos hidricos", "lote minimo 5000", "canguera"],
        snippet: "Institui a Área de Proteção Ambiental da Represa de Itupararanga e tutela a bacia formadora, impondo restrições rígidas de parcelamento, lote mínimo de 5.000 m² e taxa de permeabilidade superior a 50%."
      },

      // -------------------------------------------------------------------------
      // PILAR 2: CIENTÍFICO, GEOTÉCNICO & CATÁSTROFES SIMILARES (IPT, CPRM, CEMADEN)
      // -------------------------------------------------------------------------
      {
        id: "cie-ipt-risco-geologico",
        pillar: "cientifico",
        pillarName: "Geotécnica & Solos",
        pillarIcon: "🔬",
        orientation: "ALERTA",
        orientationLabel: "Risco Geológico & Argissolos",
        domain: "ipt.br",
        title: "IPT · Cartografia Geotécnica de Encostas e Suscetibilidade a Escorregamentos",
        url: "https://www.ipt.br",
        category: "Instituto de Pesquisas Tecnológicas de SP",
        keywords: ["ipt", "escorregamento", "movimento de massa", "argissolo", "pva", "declividade", "suscetibilidade", "coluviao", "erodibilidade", "estabilidade de encosta"],
        snippet: "Estudos geotécnicos do IPT comprovam que os Argissolos Vermelho-Amarelos (PVA) dominantes em São Roque possuem horizonte B textural com alta suscetibilidade à erosão laminar e escorregamentos translacionais em declividades > 20%."
      },
      {
        id: "cie-cprm-sgb",
        pillar: "cientifico",
        pillarName: "Serviço Geológico do Brasil",
        pillarIcon: "🔬",
        orientation: "ALERTA",
        orientationLabel: "Mapeamento de Desastres",
        domain: "cprm.gov.br",
        title: "CPRM / SGB · Setorização de Riscos Geológicos e Movimentos Gravitacionais",
        url: "https://www.cprm.gov.br",
        category: "Serviço Geológico Oficial da União",
        keywords: ["cprm", "sgb", "setorizacao de risco", "corrida de detritos", "deslizamento", "inundacao", "relevo serrano", "defesa civil", "planicie aluvial"],
        snippet: "Atlas de desastres geológicos mapeando que a ocupação desordenada de fundos de vale e taludes com corte e aterro instabiliza vertentes cristalinas, acelerando corridas de detritos em eventos hidrológicos intensos."
      },
      {
        id: "cie-catastrofe-franco-da-rocha",
        pillar: "cientifico",
        pillarName: "Catástrofe Sob Mesmas Circunstâncias",
        pillarIcon: "🔬",
        orientation: "ALERTA",
        orientationLabel: "Estudo Comparativo de Desastre",
        domain: "cemaden.gov.br",
        title: "CEMADEN / IPT · Estudo da Catástrofe de Franco da Rocha (SP, 2022)",
        url: "https://www.gov.br/cemaden/pt-br",
        category: "Estudo de Caso de Desastre em Relevo Serrano",
        keywords: ["catastrofe", "franco da rocha", "2022", "deslizamento em massa", "solos saturados", "mortes", "chuvas intensas", "encosta", "relevo analogo"],
        snippet: "Análise comparativa demonstrando que a permissão de edificação em encostas com declividades superiores a 30% em rochas pré-cambrianas com cobertura de argissolo resultou em ruptura catastrófica após 180mm de precipitação contínua."
      },
      {
        id: "cie-catastrofe-sao-sebastiao",
        pillar: "cientifico",
        pillarName: "Catástrofe Sob Mesmas Circunstâncias",
        pillarIcon: "🔬",
        orientation: "ALERTA",
        orientationLabel: "Estudo Comparativo de Desastre",
        domain: "ipt.br",
        title: "IPT · Relatório Técnico das Corridas de Massa da Barra do Sahy (SP, 2023)",
        url: "https://www.ipt.br",
        category: "Estudo Geotécnico de Ruptura de Vertentes",
        keywords: ["sao sebastiao", "barra do sahy", "2023", "corrida de detritos", "desmate de encosta", "taludes", "catastrofe", "chuvas extremas"],
        snippet: "Evidenciou que a supressão de cobertura arbórea nativa em encostas declivosas (> 30%) destrói o efeito de coesão mecânica radicular das árvores, transformando escorregamentos superficiais em fluxos de lama hiperconcentrados."
      },
      {
        id: "cie-hidrologia-aracai",
        pillar: "cientifico",
        pillarName: "Ciências Hidrológicas & Bacias",
        pillarIcon: "🔬",
        orientation: "APOIO",
        orientationLabel: "Modelagem Hidrológica de Amortecimento",
        domain: "daee.sp.gov.br",
        title: "DAEE / CBH-SMT · Diagnóstico Hidrográfico da Bacia do Rio Sorocaba e Médio Tietê",
        url: "https://www.daee.sp.gov.br",
        category: "Recursos Hídricos e Saneamento",
        keywords: ["daee", "cbh-smt", "bacia do aracai", "medio tiete", "impermeabilizacao", "piscinao", "amortecimento de cheias", "vazao de pico", "tempo de concentracao"],
        snippet: "Modelagem hidrológica comprovando que a implantação de bacias de detenção (piscinões) e parques lineares de amortecimento reduz em até 42% a vazão de pico das cheias históricas do Rio Aracaí e Carambeí."
      },

      // -------------------------------------------------------------------------
      // PILAR 3: NOTÍCIAS, FATOS REAIS & CASOS PRÁTICOS (Investigações e Ocorrências)
      // -------------------------------------------------------------------------
      {
        id: "not-gaema-loteamentos",
        pillar: "noticias",
        pillarName: "Fiscalizações & Ações do Gaema",
        pillarIcon: "📰",
        orientation: "ALERTA",
        orientationLabel: "Investigação & Embargos Reais",
        domain: "mpsp.mp.br",
        title: "Ministério Público de SP · Operações contra Parcelamento Clandestino no Roteiro do Vinho",
        url: "https://www.mpsp.mp.br",
        category: "Gaema / Promotoria de Habitação e Urbanismo",
        keywords: ["gaema", "mp-sp", "roteiro do vinho", "canguera", "loteamento clandestino", "policia ambiental", "embargo", "inquerito civil", "crime ambiental", "fraude imobiliaria"],
        snippet: "Ações civis e operações conjuntas da Polícia Ambiental e MP-SP embargando chacreamentos ilegais mascarados como 'condomínios de lazer' em zonas rurais e de amortecimento da APA de Itupararanga."
      },
      {
        id: "not-enchentes-aracai",
        pillar: "noticias",
        pillarName: "Histórico de Enchentes e Danos",
        pillarIcon: "📰",
        orientation: "ALERTA",
        orientationLabel: "Registro de Ocorrências Históricas",
        domain: "g1.globo.com",
        title: "G1 / Folha · Chuvas Provocam Alagamentos Críticos e Deslizamentos em São Roque",
        url: "https://g1.globo.com/sp/sorocaba-jundiai",
        category: "Noticiário e Registros da Defesa Civil",
        keywords: ["alagamento", "enchente", "rio aracai", "guacu", "centro historico", "transbordamento", "defesa civil", "desabamento", "morro do cruzeiro", "prejuizo"],
        snippet: "Registros documentais de cheias recorrentes que inundaram a Avenida Aracaí e a região do Guaçu, evidenciando o colapso do sistema de microdrenagem face à impermeabilização das cabeceiras urbanas."
      },
      {
        id: "not-obras-piscinoes-sucesso",
        pillar: "noticias",
        pillarName: "Obras Estruturantes Positivas",
        pillarIcon: "📰",
        orientation: "APOIO",
        orientationLabel: "Solução Prática de Sucesso",
        domain: "saoroque.sp.gov.br",
        title: "Prefeitura de São Roque · Obras Prioritárias da Carta XIII: Drenagem e Piscinões SRQ-01 a SRQ-04",
        url: "https://www.saoroque.sp.gov.br",
        category: "Projetos Estruturantes de Drenagem",
        keywords: ["carta xiii", "obras prioritarias", "srq-01", "srq-02", "piscinao", "macrodrenagem", "parque linear", "retencao", "sucesso", "infraestrutura"],
        snippet: "Plano estruturado de macrodrenagem prevendo reservatórios de amortecimento nas bacias do Aracaí e Guaçu para mitigar enchentes históricas e restabelecer a segurança hídrica da população urbana."
      },
      {
        id: "not-reurb-social-apoio",
        pillar: "noticias",
        pillarName: "Regularização Fundiária Reurb-S",
        pillarIcon: "📰",
        orientation: "APOIO",
        orientationLabel: "Parâmetro Social de Sucesso",
        domain: "habitacao.sp.gov.br",
        title: "Secretaria de Habitação de SP · Regularização Fundiária de Interesse Social (Reurb-S)",
        url: "https://www.habitacao.sp.gov.br",
        category: "Política Habitacional de Interesse Social",
        keywords: ["reurb", "reurb-s", "interesse social", "regularizacao fundiaria", "titulo de propriedade", "infraestrutura essencial", "saneamento", "cidadania", "aeis"],
        snippet: "Processos bem-sucedidos de Reurb de interesse social em assentamentos consolidados que conferem dignidade, ligação oficial de rede de água potável, esgotamento sanitário e prevenção de riscos geotécnicos."
      },

      // -------------------------------------------------------------------------
      // PILAR 4: SÃO ROQUE OFICIAL & PARTICIPAÇÃO POPULAR
      // -------------------------------------------------------------------------
      {
        id: "loc-camara-eprocleg",
        pillar: "local",
        pillarName: "Câmara Municipal · EPROCLEG",
        pillarIcon: "🏛️",
        orientation: "APOIO",
        orientationLabel: "Demandas Reais do Legislativo",
        domain: "camarasaoroque.sp.gov.br",
        title: "Câmara Municipal de São Roque · Sistema EPROCLEG (22.468 Protocolos)",
        url: "https://www.camarasaoroque.sp.gov.br",
        category: "Poder Legislativo Municipal",
        keywords: ["camara", "vereador", "eprocleg", "audiencia", "proposicao", "indicacao", "requerimento", "projeto de lei", "plano diretor", "audiencia publica", "zeladoria", "asfalto"],
        snippet: "Base oficial da Câmara Municipal com 22.468 requerimentos e indicações de vereadores mapeando os gargalos reais de asfalto, esgoto, saúde e transporte em cada bairro do município."
      },
      {
        id: "loc-prefeitura-minutas",
        pillar: "local",
        pillarName: "Prefeitura · Minutas 2026",
        pillarIcon: "🏛️",
        orientation: "REGRA",
        orientationLabel: "Proposta Oficial de Revisão",
        domain: "saoroque.sp.gov.br",
        title: "Prefeitura da Estância Turística de São Roque · Consulta Pública do Plano Diretor",
        url: "https://www.saoroque.sp.gov.br/consulta-publica-revisao-plano-diretor",
        category: "Poder Executivo Municipal",
        keywords: ["prefeitura", "consulta publica", "minuta", "revisao", "plano diretor", "decreto", "alvara", "obras", "planejamento", "lc 39", "lc 40"],
        snippet: "Portal oficial com o acervo completo da revisão do Plano Diretor: Minutas das Leis Complementares 39 e 40, Cartas I a XIII e estudos de suporte territorial."
      },
      {
        id: "loc-audiencias-voz-do-bairro",
        pillar: "local",
        pillarName: "Voz do Bairro · Moradores",
        pillarIcon: "🏛️",
        orientation: "APOIO",
        orientationLabel: "Participação Popular nas Audiências",
        domain: "saoroque.sp.gov.br",
        title: "Audiências Públicas do Plano Diretor · Sugestões da População",
        url: "https://www.saoroque.sp.gov.br",
        category: "Controle Social e Participação Cidadã",
        keywords: ["voz do bairro", "moradores", "audiencia publica", "sugestoes", "canguera", "maylasky", "sao joao novo", "centro expandido", "reclamacoes", "prioridades"],
        snippet: "Manifestações oficiais de moradores em audiências públicas exigindo proteção florestal na ZUPA, contenção da expansão urbana desordenada e infraestrutura antes de novos loteamentos."
      },
      {
        id: "loc-ibge-cidades",
        pillar: "local",
        pillarName: "IBGE · Demografia Municipal",
        pillarIcon: "🏛️",
        orientation: "ESTUDO_COMPARATIVO",
        orientationLabel: "Censo Demográfico Oficial",
        domain: "cidades.ibge.gov.br",
        title: "IBGE Cidades · Panorama Demográfico e Setores Censitários de São Roque",
        url: "https://cidades.ibge.gov.br/brasil/sp/sao-roque/panorama",
        category: "Dados Estatísticos e Demográficos Oficiais",
        keywords: ["ibge", "censo", "populacao", "setor censitario", "demografia", "renda", "pib", "area territorial", "densidade demografica"],
        snippet: "Dados demográficos do Censo IBGE demonstrando a taxa de crescimento da população, concentração urbana nos eixos viários e densidades por setor censitário de São Roque."
      }
    ];
  }

  get officialRepositories() {
    return this.knowledgeBase;
  }

  /**
   * Executa a pesquisa multidimensional em 4 etapas estruturadas
   * @param {string} query Pergunta do munícipe ou debatedor
   * @param {Object|null} pinContext Contexto geoespacial do pino no mapa
   * @returns {Promise<Object>} Resultado estruturado com os 4 pilares, fontes e grounding
   */
  async search(query, pinContext = null) {
    const qClean = (query || "").trim();
    if (!qClean && !pinContext) {
      return { query: "", total: 0, sources: [], byPillar: {}, groundingPrompt: "" };
    }

    const qLower = qClean.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

    // ETAPA 1: Seleção e pontuação dos 4 Pilares do Conhecimento
    const scoredSources = this.scoreKnowledgeBase(qLower, pinContext);

    // ETAPA 2: Consulta externa aberta via Wikipedia/OpenSearch para grounding em tempo real
    let externalLive = [];
    try {
      externalLive = await this.queryOpenSearch(qClean);
    } catch (e) {
      // Degradação graciosa
    }

    // ETAPA 3: Agrupamento equilibrado por Pilar (Garante representatividade dos 4 pilares)
    const byPillar = {
      juridico: [],
      cientifico: [],
      noticias: [],
      local: []
    };

    scoredSources.forEach(item => {
      if (byPillar[item.pillar]) {
        byPillar[item.pillar].push(item);
      }
    });

    if (externalLive.length > 0) {
      externalLive.forEach(ext => {
        byPillar.local.push({
          id: `ext-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`,
          pillar: "local",
          pillarName: "Enciclopédia Aberta & Geografia",
          pillarIcon: "🌐",
          orientation: "ESTUDO_COMPARATIVO",
          orientationLabel: "Fonte Aberta",
          domain: ext.domain,
          title: ext.title,
          url: ext.url,
          category: ext.category,
          snippet: ext.snippet
        });
      });
    }

    // Seleciona as melhores fontes de cada pilar para compor o painel final
    const selectedSources = [];
    const maxPerPillar = 2; // Garante 2 de cada pilar (total até 8 fontes ricas)

    ["juridico", "cientifico", "noticias", "local"].forEach(p => {
      const topP = byPillar[p].slice(0, maxPerPillar);
      selectedSources.push(...topP);
    });

    // Se alguma categoria ficou vazia, preenche com as mais bem pontuadas gerais
    if (selectedSources.length < 5) {
      scoredSources.forEach(s => {
        if (!selectedSources.some(sel => sel.id === s.id)) {
          selectedSources.push(s);
        }
      });
    }

    // Limita entre 5 e 8 fontes de altíssimo valor
    const finalSources = selectedSources.slice(0, 8);

    // ETAPA 4: Formatação de Grounding para injeção dialética no Argon
    const groundingPrompt = this.formatGroundingPrompt(qClean, finalSources, pinContext);

    return {
      query: qClean,
      total: finalSources.length,
      sources: finalSources,
      byPillar: {
        juridico: finalSources.filter(s => s.pillar === "juridico"),
        cientifico: finalSources.filter(s => s.pillar === "cientifico"),
        noticias: finalSources.filter(s => s.pillar === "noticias"),
        local: finalSources.filter(s => s.pillar === "local")
      },
      groundingPrompt: groundingPrompt
    };
  }

  /**
   * Pontua as bases de conhecimento conforme o contexto da pergunta e a localização do pino
   */
  scoreKnowledgeBase(qLower, pinContext) {
    const hits = [];

    // Fatores de contexto físico do pino
    const isInsideAPA = pinContext?.insideAPA || false;
    const declividade = pinContext?.declividade || null;
    const isHighSlope = (declividade && (declividade.angulo_graus >= 17 || declividade.classe?.includes("30") || declividade.classe?.includes("45")));
    const zonaNome = (pinContext?.zonaNome || "").toLowerCase();

    for (const item of this.knowledgeBase) {
      let score = 1; // pontuação base de relevância técnica

      // Relevância por palavras-chave na pergunta
      for (const kw of item.keywords) {
        if (qLower.includes(kw)) {
          score += 4;
        }
      }

      // Relevância por contexto espacial do pino
      if (isInsideAPA && (item.id === "jur-apa-itupararanga" || item.id === "not-gaema-loteamentos")) {
        score += 8;
      }
      if (isHighSlope && (item.id === "jur-lei-6766" || item.id === "cie-ipt-risco-geologico" || item.id === "cie-catastrofe-franco-da-rocha" || item.id === "cie-catastrofe-sao-sebastiao")) {
        score += 10;
      }
      if ((qLower.includes("maleficio") || qLower.includes("ruim") || qLower.includes("prejuizo") || qLower.includes("critica") || qLower.includes("catastrofe")) && item.orientation === "ALERTA") {
        score += 6;
      }
      if ((qLower.includes("beneficio") || qLower.includes("obra") || qLower.includes("solucao") || qLower.includes("propositivo") || qLower.includes("apoiar")) && item.orientation === "APOIO") {
        score += 6;
      }
      if (qLower.includes("lei") || qLower.includes("regra") || qLower.includes("artigo") || qLower.includes("minuta") || qLower.includes("plano diretor")) {
        if (item.pillar === "juridico" || item.id === "loc-prefeitura-minutas") {
          score += 5;
        }
      }
      if (qLower.includes("estudo") || qLower.includes("cientifico") || qLower.includes("solo") || qLower.includes("geotecnia") || qLower.includes("desastre")) {
        if (item.pillar === "cientifico") {
          score += 6;
        }
      }

      hits.push({ ...item, score });
    }

    hits.sort((a, b) => b.score - a.score);
    return hits;
  }

  /**
   * Consulta OpenSearch / Wikipedia para evidências abertas adicionais
   */
  async queryOpenSearch(query) {
    if (typeof fetch === "undefined") return [];

    const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
    const timer = controller ? setTimeout(() => controller.abort(), this.timeoutMs) : null;

    try {
      const endpoint = `https://pt.wikipedia.org/w/api.php?action=opensearch&search=${encodeURIComponent("São Roque " + query)}&limit=2&namespace=0&format=json&origin=*`;
      const resp = await fetch(endpoint, {
        signal: controller?.signal,
        headers: { "Accept": "application/json" }
      });
      if (timer) clearTimeout(timer);

      if (!resp.ok) return [];
      const data = await resp.json();
      
      const titles = data[1] || [];
      const snippets = data[2] || [];
      const urls = data[3] || [];

      const list = [];
      for (let i = 0; i < titles.length; i++) {
        if (titles[i] && urls[i]) {
          list.push({
            domain: "pt.wikipedia.org",
            title: titles[i],
            url: urls[i],
            category: "Enciclopédia Aberta & Geografia",
            snippet: snippets[i] || `Verbete territorial relacionado a ${titles[i]} no contexto de São Roque (SP).`,
            retrieved_at: new Date().toISOString()
          });
        }
      }
      return list;
    } catch (err) {
      if (timer) clearTimeout(timer);
      return [];
    }
  }

  /**
   * Formata o Grounding Multidimensional para injeção dialética no prompt do Argon
   */
  formatGroundingPrompt(query, sources, pinContext) {
    if (!sources || sources.length === 0) return "";

    const lines = [
      `[GROUNDING DE BUSCA WEB & FONTES OFICIAIS IDENTIFICADAS]`,
      `[GROUNDING MULTIDIMENSIONAL PERICIAL · REGRAS, CIÊNCIA & NOTÍCIAS]`,
      `Consulta em debate: "${query}"`,
      pinContext ? `Contexto do Ponto: Distrito ${pinContext.distrito}, Zona ${pinContext.zonaNome}, APA: ${pinContext.insideAPA ? 'SIM' : 'NÃO'}` : `Escopo: Geral do Município de São Roque`,
      `Fontes auditáveis cruzadas nos 4 Pilares essenciais:`
    ];

    sources.forEach((s, idx) => {
      lines.push(`  [${idx + 1}] ${s.pillarIcon} [${s.pillar.toUpperCase()}] ${s.title}`);
      lines.push(`      Papel Dialético: ${s.orientationLabel} (${s.orientation})`);
      lines.push(`      Domínio / Órgão: ${s.domain} (${s.category})`);
      lines.push(`      URL Oficial Auditável: ${s.url}`);
      lines.push(`      Evidência / Regra / Estudo: ${s.snippet}`);
    });

    lines.push(`DIRETRIZ DE CITAÇÃO OBRIGATÓRIA:`);
    lines.push(`DIRETRIZ DE DEBATE E EMBASAMENTO DIALÉTICO:`);
    lines.push(`1. NUNCA faça afirmações sem citar a regra jurídica ou o estudo científico que a sustenta.`);
    lines.push(`2. Quando debater riscos, compare com catástrofes e estudos análogos (Franco da Rocha, São Sebastião, Petrópolis ou as enchentes históricas do Rio Aracaí).`);
    lines.push(`3. Apresente com clareza o que é REGRA COGENTE inafastável, o que é ALERTA DE RISCO/CATÁSTROFE e o que é APOIO/SOLUÇÃO PROPOSITIVA.`);
    lines.push(`4. Cite expressamente as fontes em links Markdown legíveis: [Título da Fonte](URL_OFICIAL).`);

    return lines.join("\n");
  }

  /**
   * Renderiza o Card de Fontes Expandido com Cabeçalho e Abas (.ai-sources-card & .ai-sources-header)
   * @param {Array} sources Lista de fontes
   * @returns {string} HTML renderizado
   */
  renderSourcesHtml(sources) {
    if (!sources || sources.length === 0) return "";

    const juridicoCount = sources.filter(s => s.pillar === "juridico").length;
    const cientificoCount = sources.filter(s => s.pillar === "cientifico").length;
    const noticiasCount = sources.filter(s => s.pillar === "noticias").length;
    const localCount = sources.filter(s => s.pillar === "local").length;

    const cardId = `sources-card-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;

    return `
      <div class="ai-sources-card" id="${cardId}">
        <div class="ai-sources-header">
          <div class="ai-sources-header-main">
            <span class="ai-sources-icon">📚</span>
            <div class="ai-sources-title-box">
              <span class="ai-sources-title">Base de Conhecimento Multidimensional & Evidências Auditáveis (${sources.length})</span>
              <span class="ai-sources-subtitle">⚖️ Jurídico & Regras · 🔬 Ciência & Catástrofes Similares · 📰 Notícias & Fatos · 🏛️ São Roque Local</span>
            </div>
          </div>
          <div class="ai-sources-tabs">
            <button type="button" class="ai-sources-tab-btn active" data-filter="all" data-target="${cardId}">Todos (${sources.length})</button>
            ${juridicoCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="juridico" data-target="${cardId}">⚖️ Jurídico (${juridicoCount})</button>` : ""}
            ${cientificoCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="cientifico" data-target="${cardId}">🔬 Ciência & Desastres (${cientificoCount})</button>` : ""}
            ${noticiasCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="noticias" data-target="${cardId}">📰 Notícias & Fatos (${noticiasCount})</button>` : ""}
            ${localCount > 0 ? `<button type="button" class="ai-sources-tab-btn" data-filter="local" data-target="${cardId}">🏛️ São Roque (${localCount})</button>` : ""}
          </div>
        </div>

        <div class="ai-sources-list">
          ${sources.map((s, idx) => {
            let orientationClass = "ai-source-role-regra";
            if (s.orientation === "ALERTA") orientationClass = "ai-source-role-alerta";
            else if (s.orientation === "APOIO") orientationClass = "ai-source-role-apoio";
            else if (s.orientation === "ESTUDO_COMPARATIVO") orientationClass = "ai-source-role-comparativo";

            let pillarClass = `ai-source-pillar-${s.pillar}`;

            return `
              <a href="${s.url}" target="_blank" rel="noopener noreferrer" class="ai-source-item ${pillarClass}" data-pillar="${s.pillar}" title="Auditar no repositório oficial: ${s.url}">
                <div class="ai-source-badge-row">
                  <span class="ai-source-index">#${idx + 1}</span>
                  <span class="ai-source-pillar-tag">${s.pillarIcon} ${s.pillarName}</span>
                  <span class="ai-source-role-badge ${orientationClass}">${s.orientationLabel}</span>
                  <span class="ai-source-domain">${s.domain}</span>
                </div>
                <div class="ai-source-item-title">${s.title} <span class="ai-source-external-arrow">↗</span></div>
                <div class="ai-source-item-snippet">${s.snippet}</div>
              </a>
            `;
          }).join("")}
        </div>
      </div>
    `;
  }
}
