/**
 * ===============================================================================
 * SUÍTE DE TESTES: BASE DE CONHECIMENTO MULTIDIMENSIONAL, REGRAS & 4 PILARES
 * ===============================================================================
 * Valida programaticamente:
 *  1. Divisão da pesquisa em 4 etapas estruturadas:
 *     - Jurídico & Regras Cogentes
 *     - Científico, Geotécnico & Catástrofes Similares
 *     - Notícias, Fatos Reais & Comparações Práticas (Positivas vs. Críticas)
 *     - São Roque Oficial & Voz do Bairro
 *  2. Qualidade e profundidade do embasamento (Desastres análogos, Leis, CONAMA)
 *  3. Presença de papéis dialéticos (APOIO, ALERTA, REGRA, ESTUDO_COMPARATIVO)
 *  4. Renderização do cabeçalho rico (.ai-sources-header) com abas interativas
 * ===============================================================================
 */

import assert from "assert";
import { AIWebSearchEngine } from "../js/modules/ai/ai-web-search.js";
import { AIAnswerRenderer } from "../js/modules/ai/ai-answer-renderer.js";

async function runTestSuite() {
  console.log("======================================================================");
  console.log("SUÍTE DE TESTES: BASE DE CONHECIMENTO MULTIDIMENSIONAL & 4 PILARES");
  console.log("======================================================================\n");

  const engine = new AIWebSearchEngine();

  // -------------------------------------------------------------------------
  // TESTE 1: Estrutura da Base de Conhecimento nos 4 Pilares
  // -------------------------------------------------------------------------
  console.log("--- TESTE 1: Cobertura da Base nos 4 Pilares ---");
  const base = engine.knowledgeBase;
  assert(base.length >= 12, "Base deve conter no mínimo 12 fontes estruturadas");

  const pilares = new Set(base.map(b => b.pillar));
  assert(pilares.has("juridico"), "Pilar Jurídico deve existir");
  assert(pilares.has("cientifico"), "Pilar Científico deve existir");
  assert(pilares.has("noticias"), "Pilar de Notícias/Fatos deve existir");
  assert(pilares.has("local"), "Pilar São Roque Local deve existir");
  console.log(`[OK] 4 Pilares fundamentais presentes na base (${base.length} fontes catalogadas).`);

  // -------------------------------------------------------------------------
  // TESTE 2: Conhecimento Jurídico, Normativo & Jurisprudência
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 2: Conhecimento Jurídico & Regras Cogentes ---");
  const jurLei6766 = base.find(b => b.id === "jur-lei-6766");
  assert(jurLei6766, "Lei 6.766/79 deve estar catalogada");
  assert(jurLei6766.snippet.includes("30%"), "Deve citar proibição de declividade >= 30%");
  assert(jurLei6766.orientation === "REGRA", "Papel deve ser REGRA");

  const jurEstatuto = base.find(b => b.id === "jur-estatuto-cidade");
  assert(jurEstatuto, "Estatuto da Cidade deve estar catalogado");
  assert(jurEstatuto.domain === "planalto.gov.br", "Domínio oficial do Planalto");

  const jurConama = base.find(b => b.id === "jur-conama-apps");
  assert(jurConama, "Resoluções CONAMA de APPs devem estar catalogadas");

  const jurTjsp = base.find(b => b.id === "jur-tjsp-urbanismo");
  assert(jurTjsp, "Jurisprudência do TJ-SP sobre spot zoning deve estar presente");
  console.log("[OK] Conhecimento jurídico (Lei 6.766/79, Estatuto, CONAMA e TJ-SP) 100% verificado.");

  // -------------------------------------------------------------------------
  // TESTE 3: Conhecimento Científico & Catástrofes Similares
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 3: Conhecimento Científico & Catástrofes Similares ---");
  const cieIpt = base.find(b => b.id === "cie-ipt-risco-geologico");
  assert(cieIpt, "IPT deve estar presente com risco de Argissolos PVA");
  assert(cieIpt.orientation === "ALERTA", "Deve atuar como ALERTA de risco");

  const catFranco = base.find(b => b.id === "cie-catastrofe-franco-da-rocha");
  assert(catFranco, "Catástrofe similar de Franco da Rocha (2022) deve estar catalogada");
  assert(catFranco.snippet.includes("Franco da Rocha") || catFranco.title.includes("Franco da Rocha"), "Citação explícita");

  const catSaoSebastiao = base.find(b => b.id === "cie-catastrofe-sao-sebastiao");
  assert(catSaoSebastiao, "Catástrofe similar de São Sebastião / Barra do Sahy (2023) deve estar catalogada");

  const hidAracai = base.find(b => b.id === "cie-hidrologia-aracai");
  assert(hidAracai, "Modelagem hidrológica do DAEE para o Rio Aracaí deve estar presente");
  console.log("[OK] Casos reais de catástrofes e estudos geotécnicos do IPT/CPRM/CEMADEN 100% verificados.");

  // -------------------------------------------------------------------------
  // TESTE 4: Notícias, Fatos Reais & Comparações Práticas (Positivas e Críticas)
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 4: Notícias, Comparações e Casos Práticos ---");
  const notGaema = base.find(b => b.id === "not-gaema-loteamentos");
  assert(notGaema, "Ações do GAEMA / MP-SP contra loteamentos ilegais no Roteiro do Vinho");
  assert(notGaema.orientation === "ALERTA", "Investigações atuam como ALERTA");

  const notPiscinoes = base.find(b => b.id === "not-obras-piscinoes-sucesso");
  assert(notPiscinoes, "Obras da Carta XIII (Piscinões SRQ) como solução positiva de APOIO");
  assert(notPiscinoes.orientation === "APOIO", "Papel deve ser APOIO");

  const notReurb = base.find(b => b.id === "not-reurb-social-apoio");
  assert(notReurb, "Reurb-S regularização de interesse social presente");
  console.log("[OK] Notícias, investigações do Gaeco e casos comparativos positivos/críticos validados.");

  // -------------------------------------------------------------------------
  // TESTE 5: Pesquisa Multidimensional em 4 Etapas com Contexto Espacial
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 5: Execução da Pesquisa em 4 Etapas ---");
  const searchCritica = await engine.search("Quais os malefícios, riscos de catástrofe e leis desrespeitadas?", {
    distrito: "Canguera",
    insideAPA: true,
    zonaNome: "ZUR-bd (Consolidação)",
    declividade: { angulo_graus: 22, classe: "Declividade Forte (20 a 30%)" }
  });

  assert(searchCritica.total >= 4, "Deve retornar no mínimo 4 fontes multidimensionais");
  assert(searchCritica.byPillar.juridico.length > 0, "Deve conter fontes do pilar Jurídico");
  assert(searchCritica.byPillar.cientifico.length > 0, "Deve conter fontes do pilar Científico");
  assert(searchCritica.byPillar.noticias.length > 0, "Deve conter fontes do pilar Notícias");
  assert(searchCritica.byPillar.local.length > 0, "Deve conter fontes do pilar São Roque Local");

  // Verifica se o grounding contém a diretriz de citar catástrofes similares
  assert(searchCritica.groundingPrompt.includes("Franco da Rocha") || searchCritica.groundingPrompt.includes("6.766") || searchCritica.groundingPrompt.includes("IPT"), "Grounding deve conter embasamento robusto");
  console.log(`[OK] Pesquisa executada com sucesso: ${searchCritica.total} fontes auditáveis em 4 pilares.`);

  // -------------------------------------------------------------------------
  // TESTE 6: Renderização do Card Expandido com Abas e Header Rico
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 6: Renderização de UI (.ai-sources-header e Abas) ---");
  const html = engine.renderSourcesHtml(searchCritica.sources);
  assert(html.includes("ai-sources-card"), "Deve conter o container .ai-sources-card");
  assert(html.includes("ai-sources-header"), "Deve conter o cabeçalho .ai-sources-header");
  assert(html.includes("ai-sources-subtitle"), "Deve conter o subtítulo com os 4 pilares");
  assert(html.includes("ai-sources-tabs"), "Deve conter a barra de abas de filtro");
  assert(html.includes("data-filter=\"juridico\""), "Deve conter aba de filtro para Jurídico");
  assert(html.includes("data-filter=\"cientifico\""), "Deve conter aba de filtro para Científico");
  assert(html.includes("data-filter=\"noticias\""), "Deve conter aba de filtro para Notícias");
  assert(html.includes("data-filter=\"local\""), "Deve conter aba de filtro para São Roque");
  assert(html.includes("ai-source-role-badge"), "Deve conter badges dialéticos de papel");
  console.log("[OK] Marcação HTML do cabeçalho rico (.ai-sources-header) e abas de filtro validada.");

  // -------------------------------------------------------------------------
  // TESTE 7: Integração com AIAnswerRenderer
  // -------------------------------------------------------------------------
  console.log("\n--- TESTE 7: Integração no AIAnswerRenderer (Turno Inicial & Réplica) ---");
  const renderer = new AIAnswerRenderer();

  // Simula ambiente DOM mínimo para teste
  const fakeElement = {
    innerHTML: "",
    querySelector: (selector) => {
      if (selector.includes("markdown-body") || selector.includes("ai-response-text")) {
        return {
          appendChild: (child) => {},
          innerHTML: ""
        };
      }
      return null;
    },
    querySelectorAll: (selector) => []
  };

  // Turno inicial
  renderer.renderAnswer(fakeElement, {
    titulo: "Parecer Técnico Territorial",
    origem: "Gemini 4 Argon",
    isArgon: true,
    markdownText: "Análise crítica do zoneamento...",
    webSources: searchCritica.sources
  });

  assert(fakeElement.innerHTML.includes("ai-sources-card"), "Turno inicial deve renderizar o card de fontes");
  assert(fakeElement.innerHTML.includes("Base de Conhecimento Multidimensional"), "Deve conter o título enriquecido");

  console.log("[OK] Integração no renderizador de respostas verificado com sucesso.");

  console.log("\n======================================================================");
  console.log("[SUCESSO TOTAL] Base de Conhecimento Multidimensional, Regras e 4 Pilares 100% OPERACIONAIS!");
  console.log("======================================================================");
}

runTestSuite().catch(err => {
  console.error("Falha no teste:", err);
  process.exit(1);
});
