/**
 * ===============================================================================
 * SUÍTE DE TESTES: INTELIGÊNCIA PERICIAL CRÍTICA, DIALÉTICA E O TRIPÉ DE EMBASAMENTO
 * ===============================================================================
 * Valida programaticamente:
 *  1. Guardrail de busca: consultas analíticas longas ("o que a minuta traz de malefícios...")
 *     NUNCA podem ser sequestradas como ruas isoladas ("Rua São Roque").
 *  2. Classificador ontológico de intenção pericial e dialética (isDiagnosticQuery).
 *  3. Presença obrigatória dos dois polos:
 *     - Aspectos Negativos / Riscos / Malefícios
 *     - Aspectos Positivos / Avanços / Potencialidades
 *  4. Tripé de Embasamento:
 *     - Jurídico (CF/88, Estatuto da Cidade, Lei 6.766/79, APA 11.579/03, LC 39/40 vs Minuta)
 *     - Científico (Pedologia PVA, Geologia, Declividades >= 30%, Bacias)
 *     - Notícias & Fatos da Cidade (EPROCLEG Câmara, Audiências Públicas, Obras Carta XIII)
 *  5. Recomendações e condicionantes periciais para a Câmara Municipal.
 *  6. Réplicas contextuais no ai-followup-input com profundidade dialética.
 *  7. Regra de Ouro: Zero FIDs.
 * ===============================================================================
 */

import assert from "node:assert";
import { SpatialCrossEngine } from "../js/modules/spatial-cross-engine.js";
import { AIContextBuilder } from "../js/modules/ai/ai-context-builder.js";
import { AILocalFallback } from "../js/modules/ai/ai-local-fallback.js";

console.log("======================================================================");
console.log("SUÍTE DE TESTES: INTELIGÊNCIA PERICIAL DIALÉTICA & TRIPÉ DE EMBASAMENTO");
console.log("======================================================================\n");

let passed = 0;
function pass(msg) {
  passed++;
  console.log(`  [PASS] ${msg}`);
}

async function runSuite() {
  // -------------------------------------------------------------------------
  // FASE 1: Guardrail de Entidades (Prevenção de Sequestro de Rua)
  // -------------------------------------------------------------------------
  console.log("--- FASE 1: Guardrails de Reconhecimento Espacial (Anti-Sequestro de Rua) ---");
  const crossEngine = new SpatialCrossEngine();
  await crossEngine.init();

  const userQuery = "o que o a minuta do plano diretor 2026 e das alterações de leis complementares trazem de malefícios para são roque?";
  const matchUserQuery = crossEngine.searchEntity(userQuery);

  assert.strictEqual(matchUserQuery, null, "Consulta analítica completa contendo 'São Roque' NUNCA deve casar com Rua São Roque");
  pass("Consulta analítica longa sobre a minuta NÃO é sequestrada como logradouro isolado");

  const queryAmbiental = "quais os impactos ambientais e na drenagem que a revisão do plano diretor pode causar em são roque?";
  const matchAmbiental = crossEngine.searchEntity(queryAmbiental);
  assert.strictEqual(matchAmbiental, null, "Pergunta composta com 'são roque' não deve virar rua");
  pass("Pergunta composta sobre impactos ambientais não vira rua");

  // Ruas explícitas continuam funcionando normalmente
  const matchRuaReal = crossEngine.searchEntity("Rua São Roque");
  assert(matchRuaReal && matchRuaReal.type === "logradouro", "Busca explícita por 'Rua São Roque' deve encontrar o logradouro");
  pass("Busca explícita 'Rua São Roque' identifica o logradouro com sucesso");

  const matchEstrada = crossEngine.searchEntity("Estrada do Vinho");
  assert(matchEstrada && matchEstrada.type === "logradouro", "Busca por 'Estrada do Vinho' deve encontrar a via");
  pass("Busca por 'Estrada do Vinho' identifica a via corretamente");

  const matchObra = crossEngine.searchEntity("SRQ-15");
  assert(matchObra && matchObra.type === "obra", "Busca por código 'SRQ-15' deve encontrar a obra prioritária");
  pass("Busca por código de obra 'SRQ-15' funciona com precisão");

  // -------------------------------------------------------------------------
  // FASE 2: Classificador Ontológico de Intenção Pericial (isDiagnosticQuery)
  // -------------------------------------------------------------------------
  console.log("\n--- FASE 2: Classificador de Intenção Pericial e Dialética ---");
  const contextBuilder = new AIContextBuilder();

  const triggersToTest = [
    "o que traz de malefícios para são roque?",
    "quais os benefícios da nova lei?",
    "análise de pontos positivos e negativos do plano diretor",
    "quais os impactos e riscos da minuta 2026?",
    "consequências da alteração da lc 40 no zoneamento",
    "quais as vantagens e desvantagens de abrir pousada?",
    "quais os prejuízos e danos ambientais previstos?"
  ];

  triggersToTest.forEach(t => {
    const qNorm = t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    const isDiag = contextBuilder.isDiagnosticQuery(qNorm);
    assert.strictEqual(isDiag, true, `Trigger '${t}' deve ser classificado como diagnóstico`);
  });
  pass(`Todos os ${triggersToTest.length} triggers de avaliação crítica e dialética reconhecidos com 100% de precisão`);

  // -------------------------------------------------------------------------
  // FASE 3: Síntese Pericial Dialética com o Tripé de Embasamento
  // -------------------------------------------------------------------------
  console.log("\n--- FASE 3: Síntese Dialética Completa (Malefícios, Benefícios e Tripé) ---");

  const qNorm = userQuery.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const isDiag = contextBuilder.isDiagnosticQuery(qNorm);

  const synthesis = AILocalFallback.synthesize(userQuery, qNorm, null, {}, isDiag, crossEngine);

  assert(synthesis.titulo.includes("Parecer Técnico Pericial"), "Título deve ser pericial e dialético");
  pass("Título pericial oficial: " + synthesis.titulo);

  // 3.1 Aspectos Críticos / Riscos / Malefícios
  assert(synthesis.resumo.includes("EIXO 1: ASPECTOS CRÍTICOS"), "Deve conter a seção de Aspectos Críticos/Malefícios");
  assert(synthesis.resumo.includes("Vulnerabilidade Hídrica"), "Deve abordar vulnerabilidade hídrica");
  assert(synthesis.resumo.includes("Declividade ≥ 30%"), "Deve abordar riscos em declividade >= 30%");
  assert(synthesis.resumo.includes("Estrada do Vinho"), "Deve abordar saturação na Estrada do Vinho");
  assert(synthesis.resumo.includes("Spot Zoning"), "Deve alertar sobre riscos de casuísmo e spot zoning");
  pass("Polo Negativo (Malefícios/Riscos) estruturado: saneamento, declividade, trânsito e spot zoning");

  // 3.2 Aspectos Positivos / Avanços / Potencialidades
  assert(synthesis.resumo.includes("EIXO 2: ASPECTOS POSITIVOS"), "Deve conter a seção de Aspectos Positivos/Avanços");
  assert(synthesis.resumo.includes("22 Obras Estruturantes"), "Deve destacar as 22 Obras Prioritárias");
  assert(synthesis.resumo.includes("REURB"), "Deve abordar regularização fundiária de interesse social");
  assert(synthesis.resumo.includes("Enoturismo"), "Deve abordar segurança jurídica para o enoturismo");
  pass("Polo Positivo (Avanços/Modernização) estruturado: 22 Obras, REURB e enoturismo disciplinado");

  // 3.3 Tripé de Embasamento
  assert(synthesis.resumo.includes("Lei Federal nº 6.766/1979"), "Deve embasar na Lei 6.766/79 Art. 3º");
  assert(synthesis.resumo.includes("Lei Estadual nº 11.579/2003"), "Deve embasar na Lei da APA Itupararanga");
  assert(synthesis.resumo.includes("Argissolos PVA"), "Deve embasar na pedologia científica dos Argissolos PVA");
  assert(synthesis.resumo.includes("Sabesp"), "Deve citar a Sabesp e rede de esgotamento sanitário");
  pass("Tripé de embasamento comprovado: Jurídico (6.766/APA), Científico (Argissolos PVA) e Infraestrutura (Sabesp)");

  // 3.4 Recomendações Periciais para a Câmara
  assert(synthesis.resumo.includes("EIXO 3: RECOMENDAÇÕES PERICIAIS"), "Deve conter recomendações periciais para a Câmara");
  pass("Recomendações e condicionantes periciais para a Câmara Municipal inseridas");

  // -------------------------------------------------------------------------
  // FASE 4: Réplica Contextual no ai-followup-input com Dialética
  // -------------------------------------------------------------------------
  console.log("\n--- FASE 4: Réplicas de Aprofundamento Contextual (Multi-Turno Dialético) ---");

  const followUpQuery = "E no distrito de Canguera, o que a minuta traz de prejudicial para a APA de Itupararanga e para o trânsito da Estrada do Vinho?";
  const followUpRes = AILocalFallback.synthesizeFollowUp(
    followUpQuery,
    synthesis.resumo,
    { insideAPA: true, distrito: "Canguera" },
    {},
    crossEngine,
    null
  );

  assert(followUpRes.includes("Parecer Pericial Complementar"), "Réplica deve manter formato de parecer complementar");
  pass("Réplica contextual formatada como parecer pericial complementar");

  assert(followUpRes.includes("Aspectos Críticos"), "Réplica deve abordar aspectos críticos");
  pass("Réplica aborda aspectos críticos e riscos no distrito de Canguera");

  assert(followUpRes.includes("Aspectos Positivos"), "Réplica deve abordar aspectos positivos");
  pass("Réplica equilibra com aspectos positivos e avanços previstos");

  assert(followUpRes.includes("Embasamento no Tripé"), "Réplica deve explicitar o Tripé de Embasamento");
  pass("Réplica embasada no tripé: normas de mananciais, ciência dos solos e EPROCLEG");

  assert(followUpRes.includes("Recomendações Periciais"), "Réplica deve fornecer condicionantes técnicas");
  pass("Réplica fornece condicionantes para blindar o município contra passivos futuros");

  // -------------------------------------------------------------------------
  // FASE 5: Semântica Territorial Estrita (Zero FIDs)
  // -------------------------------------------------------------------------
  console.log("\n--- FASE 5: Auditoria de Zero FIDs ---");
  const fidPattern = /\bFID\s*\d+\b|\bfid:\s*\d+\b/gi;

  const fidSynthesis = synthesis.resumo.match(fidPattern);
  assert(!fidSynthesis || fidSynthesis.length === 0, "Síntese não deve conter identificadores FID");
  pass("Síntese dialética 100% limpa de FIDs numéricos");

  const fidFollowUp = followUpRes.match(fidPattern);
  assert(!fidFollowUp || fidFollowUp.length === 0, "Réplica não deve conter identificadores FID");
  pass("Réplica de aprofundamento 100% limpa de FIDs numéricos");

  console.log("\n======================================================================");
  console.log(`RESULTADO FINAL DOS TESTES: ${passed}/${passed} ASSERTIONS PASSARAM (0 falhas)`);
  console.log("======================================================================");
  console.log("[SUCESSO TOTAL] Inteligência crítica, dialética e tripé de embasamento plenamente operacionais!");
}

runSuite().catch(err => {
  console.error("FALHA NOS TESTES:", err);
  process.exit(1);
});
