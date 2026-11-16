/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · MOTOR DE CONTEXTO E PROMPTS DE IA (GEMINI 4 ARGON)
 * ===============================================================================
 * Módulo desacoplado responsável por:
 *  1. Montar o Dossiê Multidimensional de Alta Densidade (Semantic Shorthand)
 *  2. Injetar a totalidade das 33 camadas cartográficas oficiais e suas leis
 *  3. Formatar o System Prompt pericial com os 5 eixos estruturais
 *  4. Classificar a intenção pericial da consulta (spot zoning, casuísmo, anomalias)
 * ===============================================================================
 */

import { ALL_33_LAYERS } from "../spatial/layer-intelligence-catalog.js";

export class AIContextBuilder {
  constructor() {
    this.layersCatalog = ALL_33_LAYERS;
  }

  /**
   * Classificador ontológico de intenção pericial, diagnóstica e dialética
   */
  isDiagnosticQuery(qNorm) {
    const triggers = [
      "ruim", "ruins", "problema", "problemas", "fragilidade", "fragilidades", "critico", "crítico",
      "gargalo", "gargalos", "risco", "riscos", "vulnerabilidade", "vulnerabilidades", "proibido",
      "proibidos", "vedado", "vedados", "ilegal", "ilegais", "conflito", "conflitos", "deficit",
      "déficit", "saturado", "saturacao", "saturação", "inundacao", "inundação", "alagamento",
      "passivo", "passivos", "nao pode", "não pode", "inviavel", "inviável", "reclamacao", "reclamação",
      "reclamacoes", "reclamações", "pior", "piores", "irregular", "irregulares", "clandestino", "clandestinos",
      "spot zoning", "casuismo", "casuísmo", "casuistico", "casuística", "perimetro", "perímetro",
      "anomalia", "anomalias", "favorecimento", "escuso", "escusa", "preferencia", "preferência",
      "erro grosseiro", "erros grosseiros", "incoerente", "incoerencia", "incoerência", "polsby popper",
      "salto de ca", "especulacao", "especulação", "auditoria", "pericial", "pericia", "perícia",
      // TRIGGERS DE AVALIAÇÃO DIALÉTICA E CRÍTICA DE POLÍTICAS URBANAS:
      "maleficio", "maleficios", "beneficio", "beneficios", "vantagem", "vantagens", "desvantagem", "desvantagens",
      "positivo", "positivos", "negativo", "negativos", "pros e contras", "critica", "criticas", "prejuizo", "prejuizos",
      "dano", "danos", "impacto", "impactos", "impacto negativo", "impacto positivo", "retrocesso", "avanco", "avancos",
      "alteracao", "alteracoes", "mudanca", "mudancas", "minuta", "minutas", "modificacao", "modificacoes", "revisao",
      "avaliacao", "parecer", "diagnostico", "plano diretor", "lc 39", "lc 40", "consequencia", "consequencias"
    ];
    return triggers.some((t) => qNorm.includes(t));
  }

  /**
   * Monta o System Prompt de alta densidade semântica para o Gemini 4 Argon
   */
  buildSystemPrompt(deepContext) {
    return `[ROLE] Motor Central de Inteligência Geoespacial, Topologia Cruzada e Direito Urbanístico do São Roque GIS Hub (Modelo: Gemini 4 Argon).
Base: 33 camadas geográficas interligadas, Grafo Territorial Multicamadas (3.222 logradouros, 22 bairros, 4 distritos, 14 zonas LC 40/06, 13 Cartas Oficiais 2026, 22 Obras da Carta XIII, Pedologia, Geologia, Declividade, APA Itupararanga, 227 leis, 1.709 artigos de lei e audiências públicas).

[POSTURA PERICIAL DIALÉTICA - O TRIPÉ DE EMBASAMENTO CRÍTICO]
Quando o usuário formular perguntas avaliativas, críticas ou prospectivas (ex: "o que traz de malefícios?", "quais os impactos?", "pontos positivos e negativos", "o que muda com a revisão?"), você NÃO deve emitir respostas rasas nem burocráticas.
Você deve atuar com o rigor de um Perito Judicial e Consultor de Políticas Urbanas de Elite, estruturando a resposta no TRIPÉ DE EMBASAMENTO:
1. EMBASAMENTO JURÍDICO E NORMATIVO:
   - Estatuto da Cidade (Lei Federal 10.257/2001, Arts. 2º e 42-B) e CF/88 (Arts. 37, 182 e 225).
   - Lei Federal nº 6.766/1979 (Art. 3º - vedação expressa de loteamentos em declividades >= 30% e áreas alagadiças).
   - Código Florestal (Lei Federal 12.651/2012) e Leis Estaduais de Mananciais (Leis 11.579/03, 10.100/98 e 9.866/97 da APA de Itupararanga).
   - Confronto analítico direto: LC 39/06 e LC 40/06 vigentes vs. Minutas e PLCs 03/2026 e 04/2026 da Câmara Municipal.
2. EMBASAMENTO CIENTÍFICO E GEOTÉCNICO:
   - Pedologia e Solos: Argissolos PVA (alta suscetibilidade a voçorocas e erosão laminar).
   - Geologia: Granito Ibiúna, vulcanismo, fraturamentos e instabilidade de encostas.
   - Hidrologia e Geomorfologia: Várzeas do Aracaí/Guaçu sujeitas a refluxo e inundações; declividades críticas > 30% e > 45°.
   - Saneamento ambiental: Capacidade de suporte de bacias hidrográficas e riscos de contaminação do lençol freático por fossas rudimentares.
3. EMBASAMENTO DE NOTÍCIAS, FATOS REAIS E VOZ DO BAIRRO:
   - Câmara Municipal de São Roque: base EPROCLEG disponível nesta consulta; quando o dossiê da Seção 5 trouxer números da região, use SOMENTE esses números. Se o dossiê não estiver presente, não atribua contagens de protocolos a nenhum bairro.
   - Audiências Públicas do Plano Diretor: Reivindicações populares de Canguera (Rota do Vinho), Maylasky, Centro e São João Novo.
   - Notícias e Debates Públicos: Histórico de enchentes no centro, gargalos da SP-270 Raposo Tavares, pressões de adensamento e regularização de núcleos clandestinos.

[ESTRUTURA DIALÉTICA OBRIGATÓRIA DA ANÁLISE]:
Para qualquer análise crítica da Minuta 2026 e alterações de leis, estruture a resposta de forma dialética e aprofundada:
- 1. ASPECTOS CRÍTICOS, RISCOS E IMPACTOS ADVERSOS ("MALEFÍCIOS" E FRAGILIDADES):
  Aponte com clareza os riscos de adensamento sem infraestrutura, pressão sobre mananciais da APA Itupararanga, spot zoning/casuísmo em ZUEs, saturação de eixos viários (Estrada do Vinho e Raposo Tavares), risco de expansão de loteamentos irregulares e omissão de cronograma orçamentário para as obras.
- 2. ASPECTOS POSITIVOS, AVANÇOS E MODERNIZAÇÕES URBANAS:
  Destaque o que a minuta avança: modernização dos índices de aproveitamento, previsão vinculante das 22 Obras Estruturantes da Carta XIII, regularização fundiária (REURB / Carta IX), delimitação de zonas de interesse turístico e proteção de áreas de preservação permanente.
- 3. ANÁLISE DE CONFORMIDADE COM A JURISPRUDÊNCIA E DOUTRINA URBANÍSTICA:
  Avalie a conformidade com as teses fixadas pelo TJ-SP e STF (vedação a retrocesso ambiental, princípio da proibição do desdobro sem saneamento, necessidade de EIV prévio).
- 4. RECOMENDAÇÕES PERICIAIS E CONDICIONANTES TÉCNICAS:
  Quais emendas, travas e condicionantes devem ser inseridas pela Câmara Municipal antes da aprovação final para blindar o município contra passivos futuros.

[DISTINÇÃO JURÍDICO-TEMPORAL CRÍTICA: VIGENTE VS. PROPOSTA EM REVISÃO]
Você deve SEMPRE distinguir com rigor técnico absoluto dois regimes jurídicos e territoriais complementares:
1. REGIME JURÍDICO VIGENTE (Direito Positivo Atual / Em Vigor):
   • Lei Complementar nº 39/2006: Plano Diretor Físico e Territorial vigente (princípios, diretrizes, macrozonas e instrumentos urbanísticos em vigor).
   • Lei Complementar nº 40/2006: Lei de Uso, Ocupação, Parcelamento e Regularização do Solo HOMOLOGADA VIGENTE (ZCU, ZCC, ZCS, ZI, ZUI, ZDB, ZDM, etc., com seus índices urbanísticos vigentes de TO, CA, lote mínimo e recuos).
   • É esta legislação vigente que confere eficácia jurídica atual para expedição de certidões de uso do solo, alvarás de construção, desdobros e fiscalização municipal.
2. PROPOSTA EM TRAMITAÇÃO / REVISÃO (Plano Diretor 2026 & Minutas de Alteração):
   • Minuta Prévia de Alteração da LC 39 (Revisão Geral do Plano Diretor).
   • Minuta Prévia de Alteração da LC 40 (Revisão da Lei de Zoneamento, Uso e Ocupação: Quadros I a IX de Índices Urbanísticos e novas tipologias ZUE).
   • As 13 Cartas Oficiais do Plano Diretor 2026:
     - Carta I: Macrozoneamento Municipal (2026)
     - Carta II: ZUE - Urbanização Específica (2026)
     - Carta III: Consolidação Urbana - Geral (2026)
     - Carta IV: Consolidação Urbana - Sede (2026)
     - Carta V: Consolidação Urbana - Maylasky (2026)
     - Carta VI: Consolidação Urbana - São João Novo (2026)
     - Carta VII: Consolidação Urbana - Canguera (2026)
     - Carta VIII: Corredores de Comércio, Serviços e Turismo (2026)
     - Carta IX: Áreas de Especial Interesse - AEIS, AEIT, AEIU (2026)
     - Carta X: Sistema Viário e Drenagem - Sede (2026)
     - Carta XI: Sistema Viário e Drenagem - Maylasky (2026)
     - Carta XII: Sistema Viário e Drenagem - Canguera (2026)
     - Carta XIII: Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (2026)
   • Minuta Prévia / Estudo Técnico PMD 2006: Base técnica histórica de diagnósticos que fundamentou o plano original.
3. CONFRONTO COMPARATIVO PERICIAL (VIGENTE VS. MINUTA/PROPOSTA):
   Sempre que analisar zoneamento, parâmetros ou perímetros, realize o confronto direto e estruturado: o que vigora hoje pela LC 39/06 e LC 40/06 versus o que a Minuta de Revisão 2026 e as Cartas propõem modificar, evidenciando o impacto real para o proprietário, investidor e para o território.

[REGRA DE OURO - SEMÂNTICA TERRITORIAL (OGC / GeoSPARQL)]
NUNCA, sob hipótese alguma, utilize identificadores numéricos ou genéricos como "FID X" ou "FID Y".
Toda e qualquer menção a objetos, zonas, vias, solos ou polígonos deve ser formulada OBRIGATORIAMENTE pela LEGENDA OFICIAL e sua respectiva CAMADA (exemplo: "ZUE - Interesse Turístico da Carta II", "Argissolos Vermelho-Amarelos (PVA) da camada de Pedologia e Solos", "Estrada do Vinho (SPV-077) do Sistema Viário Municipal", "Zona de Proteção e Amortecimento da APA de Itupararanga", "Declividade Forte-Ondulado (20 a 45%)").

[TECNOLOGIA CRUZADA DE PONTA - TUDO LIGADO A TUDO]
As 33 camadas do município estão totalmente interligadas em rede topológica bidirecional:
1. SE UM PONTO OU COORDENADA É CITADO/MARCADO: Descreva sua situação em CADA camada: qual o logradouro mais próximo e distância, qual o bairro, qual o distrito, qual o zoneamento 2006 (LC 40/06) e parâmetros (CA, TO, recuos), quais Cartas do Plano Diretor 2026 incidem, qual o tipo de solo (pedologia), qual a litologia geológica, qual a declividade, se está inserido na APA de Itupararanga (e exigências de saneamento), quais obras estruturantes da Carta XIII estão no raio de influência, quais demandas da comunidade afetam a área, e quais as regras jurídicas incidentes específicas com seus artigos de lei.
2. SE UMA RUA / LOGRADOURO É CITADO: Informe onde ela fica (bairros e distrito), que zonas ela atravessa, qual a pedologia predominante, se passa pela APA Itupararanga e quais obras da Carta XIII a beneficiam diretamente.
3. SE UMA CAMADA OU LEGENDA É CITADA (ex: ZUE-DT, Argissolo, APA Itupararanga, Declividade > 30%, Proteção Aeroportuária): Informe onde ela ocorre no território, quais vias e bairros a atravessam, quais outras camadas se sobrepõem e quais leis a regulam.

[DIRECTIVE]
1. EXAUSTIVIDADE & RIGOR CONCISO: Forneça parecer técnico aprofundado, fundamentado em dados numéricos e leis, com alta densidade de informação. Evite prolixidade desnecessária para garantir entrega ágil.
2. ZERO TRUNCAMENTO: Cada um dos tópicos técnicos deve ser objetivo e direto, garantindo que o texto completo tenha entre 800 e 1.200 palavras. Conclua OBRIGATORIAMENTE todas as seções e finalize com a linha exata: [FIM DO PARECER TÉCNICO].
3. ESTRUTURA PARA PERGUNTAS AMPLAS OU AVALIATIVAS ("o que é ruim?", gargalos, riscos, problemas):
   Estruture a resposta obrigatoriamente nos 5 EIXOS ESTRUTURAIS:
   - 1. Vulnerabilidades Físico-Ambientais e Áreas de Risco Geotécnico/Hidrológico (Declividade >= 30%, inundações do Aracaí/Guaçu, APA Itupararanga, APPs).
   - 2. Gargalos Estruturais de Mobilidade e Conectividade Viária (SP-270 Raposo Tavares, Estrada do Vinho SPV-077, ferrovia São João Novo, 22 Obras da Carta XIII).
   - 3. Conflitos de Uso do Solo, Saneamento Básico e Habitação (Núcleos clandestinos em Mailasqui/Caetê/Carmo, carência de esgoto Sabesp, desdobros).
   - 4. Vedações, Ilegalidades e Restrições Normativas Expressas (Art. 3º Lei 6.766/79, Lei 12.651/12, Leis Estaduais 10.100/98 e 9.866/97, LC 40/06, Minuta 2026).
   - 5. Críticas e Reivindicações das Audiências Públicas (COMDEMA, moradores de Maylasky, Canguera, ACIA).
4. DIRETRIZES DO PLANO DIRETOR 2026 & PARTICIPAÇÃO POPULAR: Se a consulta tratar de zoneamento, perímetros ou propostas da Minuta 2026, fundamente nos quadros técnicos oficiais (Quadros I a IX da LC 40/2026), Macrozoneamento (Carta I), ZUE (Carta II), Consolidação Urbana (Cartas III a VII), Corredores (Carta VIII) e 22 Obras Estruturantes (Carta XIII). Cite Precedentes jurisprudenciais pertinentes, Art. 37 CF/88 e Arts. 2º e 42-B do Estatuto da Cidade quando aplicável.
5. ACTION TAGS: Insira tags de ação interativa para controle do Leaflet:
   - [[ACTION:LAYER:id_da_camada|Nome da Camada]]
   - [[ACTION:FLYTO:lat,lng,zoom|Nome do Local]]
   - [[ACTION:OBRA:SRQ-XX|Nome da Obra]]
   - [[ACTION:ZONA:SIGLA|Nome da Zona]]
6. FORMATAÇÃO: Use Markdown rico com títulos hierárquicos, tabelas comparativas limpas, listas analíticas e artigos de lei explícitos.

CONTEXTO TERRITORIAL DE ALTA DENSIDADE:
${deepContext}`;
  }

  /**
   * Formata a Seção 5 (Voz do Bairro) apenas com dados apurados.
   * Se não houver dossiê do ponto, diz explicitamente que não há recorte —
   * nunca preenche com rótulos genéricos ("Base conectada", "Zeladoria, Asfalto...").
   */
  formatVozDoBairro(p) {
    const voz = p?.vozDoBairro || p?.dossier?.voz_do_bairro;
    if (!voz) {
      return `  - Sem recorte territorial da Voz do Bairro para este ponto: marque um ponto no mapa para consultar o EPROCLEG por bairro, zona e logradouro. Não invente contagens de protocolos.`;
    }

    const linhas = [];
    const regiao = voz.regiao_identificada;
    if (regiao) {
      const est = voz.estatisticas_regiao || {};
      linhas.push(`  - Região Parlamentar: ${regiao.nome_regiao} (${est.total_proposicoes || 0} proposições — ${est.indicacoes || 0} indicações, ${est.requerimentos || 0} requerimentos, ${est.projetos_de_lei || 0} projetos de lei)`);
    }
    if (voz.distancia_centroide_m != null) {
      linhas.push(`  - Distância do ponto ao centroide da região: ${voz.distancia_centroide_m} m${voz.match_por_endereco ? " (endereço confirma o bairro)" : ""}`);
    }

    const ranking = (voz.ranking_temas || []).slice(0, 4);
    if (ranking.length) {
      linhas.push(`  - Ranking real de demandas da região: ${ranking.map((t, i) => `${i + 1}º ${t.tema_nome} (${t.quantidade} protocolos / ${t.percentual}%)`).join("; ")}`);
    }

    const regProps = (voz.proposicoes_regiao || []).filter((pr) => pr && pr.titulo);
    if (regProps.length) {
      linhas.push(`  - Protocolos da região (inclui proposições sem pino GPS):`);
      regProps.slice(0, 4).forEach((pr) => {
        linhas.push(`    * ${pr.titulo} (${pr.data_formatada || pr.ano} - ${pr.autor}): ${pr.descricao_resumida || ""}`);
      });
    }

    const st = voz.logradouro_citado;
    const stProps = voz.proposicoes_mesmo_logradouro || [];
    if (st?.nome && stProps.length) {
      linhas.push(`  - Mesmo logradouro (${st.nome}) — ${stProps.length} protocolos casados por endereço:`);
      stProps.slice(0, 3).forEach((pr) => {
        linhas.push(`    * ${pr.titulo} (${pr.data_formatada || pr.ano}): ${pr.descricao_resumida}`);
      });
    }

    const gps = voz.proposicoes_proximas_gps || [];
    if (gps.length) {
      linhas.push(`  - Protocolos com coordenada no raio de 1,8 km:`);
      gps.slice(0, 3).forEach((pr) => {
        linhas.push(`    * [${pr.distancia_m}m] ${pr.titulo} (${pr.data_formatada || pr.ano} - ${pr.autor}): ${pr.descricao_resumida}`);
      });
    }

    const textos = voz.resumo_por_texto;
    if (textos?.total_protocolos) {
      const rank = (textos.ranking_temas || []).slice(0, 3).map((t) => `${t.tema_id} (${t.quantidade})`).join("; ");
      linhas.push(`  - Termos do endereço (${textos.termos.join(", ")}) aparecem em ${textos.total_protocolos} proposições: ${rank}`);
    }

    const aud = voz.pedidos_moradores_audiencias || [];
    if (aud.length) {
      linhas.push(`  - Sugestões dos moradores nas audiências do Plano Diretor:`);
      aud.slice(0, 3).forEach((pm) => {
        linhas.push(`    * [${pm.status_prefeitura}] ${pm.local_alvo}: ${String(pm.pedido_dos_moradores || "").slice(0, 160)} -> Minuta 2026: ${String(pm.resposta_oficial_minuta_2026 || "sem resposta registrada").slice(0, 160)}`);
      });
    }

    return linhas.length ? linhas.join("\n") : "  - Sem protocolos catalogados para este ponto.";
  }

  /**
   * Constrói o contexto territorial e jurídico de alta densidade semântica
   */
  buildDeepContext(query, pinCtx, kb, crossEngine) {
    const parts = [];

    // 1. Verificação no Grafo Territorial de Entidades Citadas na Pergunta
    if (crossEngine) {
      const entityMatch = crossEngine.searchEntity(query);
      if (entityMatch) {
        const em = entityMatch.data;
        if (entityMatch.type === "legislacao") {
          parts.push(`=== LEGISLAÇÃO OFICIAL IDENTIFICADA NO GRAFO TERRITORIAL ===
Diploma: ${em.tipo} nº ${em.numero}/${em.ano} (${em.esfera})
Órgão Publicador: ${em.orgao || "Poder Público"}
Ementa Oficial: ${em.ementa || "Sem ementa"}
Âmbito de Aplicação: ${em.ambito_territorial || "Todo o Município de São Roque"}
Camadas e Matérias Afetas: ${em.camadas?.length ? em.camadas.join(", ") : "Zoneamento e Ordenamento Territorial"}
Link do Texto Integral: ${em.link_oficial || "Portal da Legislação"}
Dispositivos Legais: ${em.artigos?.length || em.total_artigos || 0} artigos mapeados`);
        } else {
          parts.push(`=== ENTIDADE RECONHECIDA NO GRAFO TERRITORIAL CRUZADO ===
Tipo de Entidade: ${entityMatch.type.toUpperCase()}
Camada Oficial: ${em.camada || "Cartografia Oficial de São Roque"}
Legenda Oficial: ${em.legenda_oficial || em.nome_oficial || em.nome}
${em.distritos?.length ? `- Distritos de Ocorrência: ${em.distritos.join(", ")}` : ""}
${em.bairros?.length ? `- Bairros que Atravessa / Onde Ocorre: ${em.bairros.join(", ")}` : ""}
${em.zonas_incidentes?.length ? `- Zonas de Uso que Corta: ${em.zonas_incidentes.join("; ")}` : ""}
${em.solos_predominantes?.length ? `- Solos Pedológicos Incidentes: ${em.solos_predominantes.join("; ")}` : ""}
${em.inside_apa !== undefined ? `- APA de Itupararanga: ${em.inside_apa ? "SIM - Região de Mananciais Protegida (Leis 11.579/03 e 9.866/97)" : "Fora da APA"}` : ""}
${em.obras_proximas?.length ? `- Obras da Carta XIII Próximas: ${em.obras_proximas.map(o => `${o.codigo} (${o.nome}) a ${o.distancia_km}km`).join("; ")}` : ""}
${em.descricao ? `- Descrição / Vocação Técnica: ${em.descricao}` : ""}
${em.parametros_construtivos ? `- Parâmetros Construtivos: CA Básico ${em.parametros_construtivos.coeficiente_aproveitamento_basico || "1.0"}, CA Máx ${em.parametros_construtivos.coeficiente_aproveitamento_maximo || "1.5"}, TO Máx ${(em.parametros_construtivos.taxa_ocupacao_maxima || 0.5)*100}%, Lote Mínimo ${em.parametros_construtivos.lote_minimo_m2 || 250}m²` : ""}
${em.implicacao_obras ? `- Implicações Geotécnicas e Obras: ${em.implicacao_obras}` : ""}`);
        }
      }
    }

    // 2. Contexto do Ponto Marcado (se houver selection pin)
    if (pinCtx) {
      const p = pinCtx;
      parts.push(`=== DOSSIÊ MULTICAMADAS DO PONTO MARCADO (SELECTION PIN) ===
Coordenadas Exatas: Lat ${p.lat.toFixed(5)}, Lng ${p.lng.toFixed(5)} (${p.utmStr})
• [Camada: Sistema Viário Municipal]: ${p.logradouro ? `${p.logradouro.legenda_oficial || p.logradouro.nome} (distância ortogonal exata ao eixo: ${p.logradouro.distancia_m} metros)` : "Via local consolidada"}
• [Camada: Setores Censitários IBGE 2022]: ${p.setorCensitario ? `Setor Censitário Oficial ${p.setorCensitario.cd_setor} (${p.setorCensitario.distrito} - Situação: ${p.setorCensitario.situacao}${p.setorCensitario.area_ha ? `, Área: ${p.setorCensitario.area_ha.toFixed(1)} ha` : ""})` : "Setor Censitário IBGE Mapeado"}
• [Camada: Bairros e Setores]: ${p.bairro ? p.bairro.legenda_oficial || p.bairro.nome : "São Roque Urbano"}
• [Camada: Divisão Distrital Oficial]: ${p.distritoNomeCompleto}
• [Camada: Zoneamento Homologado LC 40/2006 (Vigente)]: ${p.zonaNome} (Sigla: ${p.zonaKey || "ZCU"})
• [Camada: Minuta de Revisão 2026 (Proposta em Estudo)]: ${p.zoneamentoMinuta2026 ? p.zoneamentoMinuta2026.legenda_oficial : "Manutenção dos Parâmetros Vigentes"}
• [Confronto de Zoneamento 2006 vs. 2026]: ${p.confrontoZoneamento?.houve_alteracao ? `⚠️ ALTERAÇÃO DE ZONEAMENTO PROPOSTA: Vigente (${p.confrontoZoneamento.vigente}) -> Minuta 2026 (${p.confrontoZoneamento.proposta_2026})` : "Sem alteração perimetral na Minuta 2026"}
• [Camada: Revisão do Plano Diretor 2026]: ${p.cartasAplicaveis.join("; ")}
• [Camada: Pedologia e Solos]: ${p.pedologia ? `${p.pedologia.legenda_oficial} (Permeabilidade: ${p.pedologia.permeabilidade || "Moderada"})` : "Argissolo Vermelho-Amarelo (PVA)"}
• [Camada: Geologia e Geotecnia]: ${p.geologia ? `${p.geologia.legenda_oficial} (Litologia: ${p.geologia.litologia || "Rocha Cristalina"})` : "Granito Ibiúna / Grupo São Roque"}
• [Camada: Unidades de Conservação]: ${p.insideAPA ? "💧 APA da Represa de Itupararanga (Lei Estadual nº 11.579/03 - Bacia de Mananciais com saneamento ecológico obrigatório e vedação a contaminação do freático)" : "Fora do polígono da APA de Itupararanga"}
• Parâmetros Construtivos da Zona:
  - Lote Mínimo: ${p.zonaData?.lote_minimo || (p.insideAPA ? "5.000 m²" : "250 m²")}
  - Taxa de Ocupação Máxima: ${p.zonaData?.taxa_ocupacao || (p.insideAPA ? "50%" : "60%")}
  - Coeficiente de Aproveitamento: ${p.zonaData?.coeficiente_aproveitamento || "1.0"}
  - Gabarito Máximo: ${p.zonaData?.gabarito_altura || "12 metros"}
  - Recuos Exigidos: ${p.zonaData?.recuos || "Frente 5m, Fundos 3m, Laterais 1.5m"}
  - Usos Permitidos: ${p.zonaData?.usos_admitidos || "Residencial e Comercial de Baixo Impacto"}
  - Restrições Críticas: ${p.zonaData?.restricoes || (p.insideAPA ? "Tratamento biológico obrigatório e anuência prévia da Fundação Florestal" : "Conforme LC 40/2006")}
• [Camada: Carta XIII - 22 Obras Estruturantes]: ${p.obrasProximas.length ? p.obrasProximas.map(o => `${o.codigo} - ${o.nome}`).join("; ") : "Nenhuma intervenção imediata no raio local"}
• [Seção 5: Voz do Bairro - Câmara Municipal (EPROCLEG) & Audiências Públicas]:
${this.formatVozDoBairro(p)}`);

      if (p.dossier?.regras_juridicas_incidentes?.length) {
        parts.push(`• [Regras Jurídicas & Condicionantes Incidentes no Ponto (${p.dossier.regras_juridicas_incidentes.length} regras incidentes)]:
${p.dossier.regras_juridicas_incidentes.slice(0, 10).map(r => `  - [${r.camada_incidente}] ${r.norma} (${r.artigo}) [${r.grau_restricao}]: ${r.regra}${r.ponto_atencao ? ` | ALERTA: ${r.ponto_atencao}` : ''}`).join("\n")}`);
      }
    }

    // 3. Catálogo Conhecido das 33 Camadas Oficiais do Município
    parts.push(`=== ROL EXAUSTIVO DAS 33 CAMADAS DO SISTEMA GIS HUB ===
${this.layersCatalog.map((c, i) => `${i + 1}. [${c.id}] ${c.nome} (${c.categoria}): Regulação por ${c.legislacao_base} | Restrição: ${c.grau_restricao}`).join("\n")}`);

    // 4. Matriz Compacta de Alta Densidade Semântica (Semantic Shorthand)
    parts.push(`=== BASE CARTOGRÁFICA, JURÍDICA E DE GARGALOS (ALTA DENSIDADE) ===
[1. MATRIZ NORMATIVA E AMBIENTAL]
- Federal: Lei 6.766/79 Art. 3º (Proibição absoluta de parcelamento urbano em terrenos alagadiços/inundáveis e com declividade >= 30% sem laudo geotécnico e estabilização). Lei 12.651/12 (Código Florestal: APP de 30m em cursos d'água < 10m; raio de 50m em nascentes; topos de morro).
- Estadual: APA Itupararanga (Leis Estaduais 11.579/03, 10.100/98 e 9.866/97 + Dec. 52.879/08): bacia sul exige lote mín. 1.000m² a 5.000m² conforme subzona, saneamento autônomo auditado sem contaminação do freático, proibição a indústrias de alto potencial poluidor. Lei 11.428/06 (Mata Atlântica): compensação ambiental obrigatória.
- Municipal: LC 40/2006 (Uso e Ocupação do Solo Vigente) vs Minuta Revisão Plano Diretor 2026 (Quadros VIII e IX, adensamento nos corredores, ZPR em mananciais, instrumentos PEUC/IPTU Progressivo, OODC e TPC).

[2. TABELA DE ZONEAMENTO OFICIAL (LC 40/2006 -> REVISÃO 2026)]
- ZC | Zona Central | 250m² | TO 80% | CA 2.0-4.0 | TP 10% | Gabarito Livre (EIV) | Adensamento com fachada ativa
- ZCOR | Corredores Viários | 300-500m² | TO 70% | CA 1.5-3.0 | TP 15% | 12m-24m | Eixos Raposo Tavares / Lívio / Quintino
- ZR-1 | Residencial Baixa Dens. | 1.000m² | TO 50% | CA 1.0 | TP 30% | 9m | Transiciona p/ ZEU controlada
- ZR-2 | Residencial Média Dens. | 300m² | TO 60% | CA 1.2-2.0 | TP 20% | 12m | Padrão urbano consolidado
- ZR-3/ZEIS | Interesse Social | 125-200m² | TO 70% | CA 1.5-2.5 | TP 15% | 15m | Regularização fundiária (REURB)
- ZM | Zona Mista | 250-500m² | TO 70% | CA 1.5-3.0 | TP 15% | 15m | Comércio e habitação integrados
- ZPI | Predominância Industrial/Logística | 2.000-5.000m² | TO 60% | CA 1.0-1.5 | TP 25% | 15m | Foco Castello Branco / Raposo / Maylasky
- ZEPAM/ZPA | Proteção Ambiental / Mananciais | 5.000-20.000m² | TO 10-20% | CA 0.2-0.4 | TP 70-80% | 7m | Restrição severa
- ZEU | Expansão Urbana | 500-1.000m² | TO 50% | CA 1.0-1.5 | TP 30% | 9m | Exige infraestrutura e drenagem prévia
- ZUE/ZTUR | Turística (Canguera / Roteiro do Vinho) | 2.000-5.000m² | TO 30-50% | CA 0.5-1.0 | TP 55-60% | 9-12m | Enoturismo e pousadas
- ZRU | Zona Rural | 20.000m² (INCRA) | TO 10% | CA 0.2 | TP 80% | 7m | Atividades agropecuárias e agroecológicas

[3. AS 13 CARTAS OFICIAIS DO PLANO DIRETOR 2026]
- Carta 01 (Macrozoneamento): layer 'carta_01_macrozoneamento_2026'
- Carta 02 (ZUE em Mananciais): layer 'carta_02_zue_2026'
- Carta 03 (Consolidação Urbana Geral): layer 'carta_03_consolidacao_urbana_2026'
- Carta 04 (Consolidação Urbana Sede): layer 'carta_04_sede_2026'
- Carta 05 (Consolidação Urbana Maylasky): layer 'carta_05_maylasky_2026'
- Carta 06 (Consolidação Urbana São João Novo): layer 'carta_06_sao_joao_novo_2026'
- Carta 07 (Consolidação Urbana Canguera): layer 'carta_07_canguera_2026'
- Carta 08 (Corredores e Rodovias): layer 'carta_08_corredores_2026'
- Carta 09 (Áreas Especiais e AEIS): layer 'carta_09_aeis_2026'
- Carta 10 (Viário e Drenagem Sede): layer 'carta_10_viario_sede_2026'
- Carta 11 (Viário e Drenagem Maylasky): layer 'carta_11_viario_maylasky_2026'
- Carta 12 (Viário e Drenagem Canguera): layer 'carta_12_viario_canguera_2026'
- Carta 13 (22 Obras Prioritárias e Áreas de Risco): layer 'carta_13_obras_prioritarias_2026'

[4. AS 22 OBRAS ESTRUTURANTES PRIORITÁRIAS (CARTA XIII - SRQ-01 A SRQ-22)]
- Mobilidade/Viário: SRQ-01 (Piscinão John Kennedy/Aracaí), SRQ-02 (Canalização Antonino Dias Bastos), SRQ-03 (Marginal Aracaí), SRQ-04 (Reforma Praça da Matriz), SRQ-05 (Ponte Guaçu), SRQ-06 a SRQ-08 (Nova Av. Roberto de Mattos / Raposo Tavares), SRQ-15 (Ciclovia e bolsões na Estrada do Vinho), SRQ-19 (Viaduto / Passagem em desnível ferroviária em São João Novo).
- Drenagem/Resiliência: SRQ-09 (Piscinão Guaçu), SRQ-10 (Desassoreamento Aracaí/Carambeí), SRQ-20 (Contenção de várzeas em São João Novo).
- Equipamentos/Turismo/Meio Ambiente: SRQ-14 (Parque Municipal do Morro do Saboó), SRQ-17 (Polo Logístico Maylasky), SRQ-22 (Requalificação Brasital).

[5. SÍNTESE CRÍTICA DAS AUDIÊNCIAS PÚBLICAS (DEMANDAS COMUNITÁRIAS 2024-2026)]
- Canguera / Roteiro do Vinho (Bacia Sul): Conflito entre saturação turística de fins de semana e precariedade viária da SPV-077; moradores cobram saneamento ecológico.
- Maylasky / Monte Verde / Caetê: Pressão pelo desdobro familiar de chácaras de 5.000m² para 500m²; acolhido sob condicionante de 55% permeável e fossa com laudo técnico.
- Centro / Bacia do Aracaí: Histórico de enchentes severas no eixo Aracaí-Bandeirantes; ACIA cobra retenção de águas pluviais a montante (piscinões).
- São João Novo: Isolamento viário por bloqueio da ferrovia de carga (Rumo); pedidos de passagens em desnível.`);

    return parts.join("\n\n");
  }
}
