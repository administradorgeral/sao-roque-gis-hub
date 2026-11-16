/**
 * ===============================================================================
 * SÃO ROQUE GIS HUB · SUÍTE DE TESTES: SEÇÃO 5 - VOZ DO BAIRRO
 * ===============================================================================
 * Validação rigorosa e 100% programática por código (Node.js):
 *  1. Integridade da Base EPROCLEG (22.468 proposições reais) e 11 Perfis Regionais
 *  2. Resolução Espacial de Regiões Parlamentares por Proximidade e Palavras-chave
 *  3. Busca de Protocolos Georreferenciados no Raio Imediato (< 1.800m)
 *  4. Metadados de Protocolo (Dia, Hora, Autor, Nro Protocolo, Íntegra, Link Oficial)
 *  5. Ranking Temático Proporcional e Barras Visuais
 *  6. Sugestões dos Moradores nas Audiências do Plano Diretor e Respostas Técnicas
 *  7. Renderização no Dossiê Multidimensional do Modal (Zero FIDs)
 *  8. Injeção Concisa e Otimizada no Prompt de IA do Gemini 4 Argon
 * ===============================================================================
 */

import assert from "assert";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { CommunityVoiceEngine } from "../js/modules/spatial/community-voice-engine.js";
import { SpatialCrossEngine } from "../js/modules/spatial-cross-engine.js";
import { ModalDossierRenderer } from "../js/modules/modal/modal-dossier-renderer.js";
import { AIContextBuilder } from "../js/modules/ai/ai-context-builder.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

// --- Mock DOM Environment para Node.js ---
class MockElement {
  constructor(tag = "div") {
    this.tagName = tag.toUpperCase();
    this.children = [];
    this.style = {};
    this.attributes = {};
    this.innerHTML = "";
    this.textContent = "";
  }
  appendChild(child) {
    this.children.push(child);
    if (child instanceof MockElement) {
      this.innerHTML += child.innerHTML || child.textContent || "";
    }
    return child;
  }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  getAttribute(k) { return this.attributes[k]; }
  addEventListener() {}
  focus() {}
}

global.document = {
  createElement: (tag) => new MockElement(tag),
  getElementById: (id) => new MockElement("div"),
  querySelector: (sel) => new MockElement("div"),
  querySelectorAll: (sel) => [],
  addEventListener: () => {},
  removeEventListener: () => {},
  body: new MockElement("body")
};

let totalAssertions = 0;
let passedAssertions = 0;

function assertTest(desc, condition, details = "") {
  totalAssertions++;
  if (condition) {
    passedAssertions++;
    console.log(`  [PASS] ${desc}`);
  } else {
    console.error(`  [FAIL] ${desc} | ${details}`);
    throw new Error(`Falha no teste: ${desc} | ${details}`);
  }
}

async function runCommunityVoiceSuite() {
  console.log("======================================================================");
  console.log("SUÍTE DE TESTES: SEÇÃO 5 — VOZ DO BAIRRO (CÂMARA & MORADORES)");
  console.log("======================================================================\n");

  // 1. Auditoria do Arquivo Consolidado
  console.log("--- FASE 1: Auditoria da Base Consolidada Local ---");
  const resumoPath = path.join(rootDir, "data", "voz_do_bairro_resumo.json");
  const dbPath = path.join(rootDir, "data", "camara_eprocleg_sao_roque.db");
  assertTest("Arquivo data/voz_do_bairro_resumo.json existe", fs.existsSync(resumoPath));
  assertTest("Banco SQLite data/camara_eprocleg_sao_roque.db existe", fs.existsSync(dbPath));

  const resumo = JSON.parse(fs.readFileSync(resumoPath, "utf8"));
  assertTest("Metadados indicam fonte primária EPROCLEG da Câmara", resumo.metadata.fonte_primaria.includes("EPROCLEG"));
  assertTest("Total de proposições no banco é 22.468", resumo.metadata.total_proposicoes_banco === 22468);
  assertTest("Total de 11 perfis regionais cadastrados", resumo.perfis_regionais.length === 11);
  assertTest("Total de 658 proposições georreferenciadas com GPS", resumo.proposicoes_geolocalizadas.length === 658);
  assertTest("Total de 10 pedidos georreferenciados de audiências do PD", resumo.pedidos_audiencias_publicas.length === 10);

  // 2. Motor de Inteligência Comunitária
  console.log("\n--- FASE 2: Motor de Inteligência Espacial Comunitária ---");
  const cve = new CommunityVoiceEngine();
  const initCve = await cve.init(resumo);
  assertTest("CommunityVoiceEngine inicializado com sucesso", initCve === true);

  // Teste de Região no Centro
  const centroMatch = cve.matchRegionalProfile(-23.5289, -47.1353, "Praça da Matriz, Centro");
  assertTest("Ponto central mapeado para o Centro Histórico", centroMatch.primaryRegion.id === "centro_vila_marques_guilhermina");
  assertTest("Centro Histórico possui mais de 2.000 proposições", centroMatch.primaryRegion.estatisticas.total_proposicoes > 2000);

  // Teste de Região em Canguera
  const cangueraMatch = cve.matchRegionalProfile(-23.5920, -47.1480, "Estrada do Vinho, Canguera");
  assertTest("Ponto em Canguera mapeado para a região de Canguera e Roteiro do Vinho", cangueraMatch.primaryRegion.id === "canguera_roteiro_vinho_campininha");
  assertTest("Canguera possui ranking de temas com asfalto como top 1", cangueraMatch.primaryRegion.estatisticas.temas_ranking[0].tema_id.includes("ZELADORIA_VIARIA_ASFALTO"));
  assertTest("Canguera tem percentual de asfalto superior a 35%", cangueraMatch.primaryRegion.estatisticas.temas_ranking[0].percentual >= 35.0);

  // Teste de Busca em Raio (< 1.800m) no Centro
  const proximasCentro = cve.findPropositionsNearby(-23.5289, -47.1353, 1800, 8);
  assertTest("Encontra proposições no raio de 1.800m no Centro", proximasCentro.length > 0);
  assertTest("Proposição mais próxima do Centro está a menos de 200m", proximasCentro[0].distancia_m <= 200);
  assertTest("Proposição contém dia e hora de protocolo", proximasCentro[0].data_formatada && proximasCentro[0].hora_formatada);
  assertTest("Proposição contém autor (vereador)", proximasCentro[0].autor.length > 3);
  assertTest("Proposição contém link oficial auditável EPROCLEG", proximasCentro[0].url_eprocleg.includes("camarasaoroque.sp.gov.br"));
  assertTest("Proposição contém descrição completa (texto na íntegra)", proximasCentro[0].descricao_completa.length > 10);

  // 3. Integração com SpatialCrossEngine
  console.log("\n--- FASE 3: Integração no SpatialCrossEngine ---");
  const crossEngine = new SpatialCrossEngine();
  await crossEngine.init();

  const dossierCentro = crossEngine.buildCrossDossierForPoint(-23.5289, -47.1353);
  assertTest("Dossiê multicamadas inclui campo 'voz_do_bairro'", dossierCentro.voz_do_bairro !== null);
  assertTest("Dossiê traz região parlamentar identificada", dossierCentro.voz_do_bairro.regiao_identificada !== null);
  assertTest("Dossiê traz ranking de temas com percentuais", dossierCentro.voz_do_bairro.ranking_temas.length >= 3);
  assertTest("Dossiê traz protocolos com GPS próximos", dossierCentro.voz_do_bairro.proposicoes_proximas_gps.length > 0);
  assertTest("Dossiê traz demandas das audiências públicas da região", dossierCentro.voz_do_bairro.pedidos_moradores_audiencias.length > 0);

  // 4. Renderização no Modal (ModalDossierRenderer)
  console.log("\n--- FASE 4: Renderização de UI (Seção 5 — Voz do Bairro) ---");
  const renderer = new ModalDossierRenderer();
  const renderRes = renderer.render(dossierCentro, null);

  assertTest("Renderizador do dossiê executou com sucesso", renderRes !== null && renderRes.container !== null);
  const htmlOut = renderRes.container.innerHTML;
  assertTest("Modal contém cabeçalho 'Seção 5: Voz do Bairro'", htmlOut.includes("Seção 5: Voz do Bairro"));
  assertTest("Modal contém badge 'EPROCLEG · 2017–2026'", htmlOut.includes("EPROCLEG · 2017–2026"));
  assertTest("Modal exibe total de proposições reais da região", htmlOut.includes("proposições reais"));
  assertTest("Modal renderiza barras visuais de progresso", htmlOut.includes("width:") && htmlOut.includes("background: #0284c7"));
  assertTest("Modal renderiza badges de distância em metros", htmlOut.includes("📍") && htmlOut.includes("m"));
  assertTest("Modal exibe data e hora do protocolo", htmlOut.includes("Protocolado em:"));
  assertTest("Modal inclui link oficial EPROCLEG", htmlOut.includes("EPROCLEG ↗"));
  assertTest("Modal inclui elemento details para texto na íntegra", htmlOut.includes("<details") && htmlOut.includes("Ver texto na íntegra"));
  assertTest("Modal exibe deliberação da Prefeitura no Plano Diretor", htmlOut.includes("Resposta Oficial da Prefeitura na Minuta 2026:"));
  assertTest("Modal NUNCA contém identificadores FID numéricos", !/\bFID[_\s]?\d+/i.test(htmlOut));

  // 5. Injeção no Prompt de IA (AIContextBuilder)
  console.log("\n--- FASE 5: Injeção de Alta Densidade no Contexto da IA (Gemini 4 Argon) ---");
  const contextBuilder = new AIContextBuilder();
  const mockPinCtx = {
    lat: -23.5820,
    lng: -47.1450,
    utmStr: "X: 281.234m, Y: 7.391.123m (SIRGAS 2000)",
    distrito: "Canguera",
    distritoNomeCompleto: "Distrito de Canguera",
    insideAPA: true,
    zonaNome: "ZUE - Desenvolvimento Turístico",
    zonaKey: "ZUE-DT",
    zonaData: null,
    setorCensitario: dossierCentro.setor_censitario_ibge,
    zoneamentoMinuta2026: null,
    confrontoZoneamento: null,
    logradouro: { nome: "Estrada do Vinho", legenda_oficial: "Estrada do Vinho", distancia_m: 156 },
    bairro: { nome: "Canguera", legenda_oficial: "Canguera" },
    pedologia: null,
    geologia: null,
    cartasAplicaveis: ["Carta I: Macrozoneamento", "Carta VII: Canguera"],
    obrasProximas: [],
    pedidosLocais: [],
    dossier: crossEngine.buildCrossDossierForPoint(-23.5820, -47.1450)
  };

  const deepContext = contextBuilder.buildDeepContext("O que a população mais reclama em Canguera?", mockPinCtx, null, crossEngine);
  assertTest("DeepContext gerado com sucesso", deepContext.length > 500);
  assertTest("DeepContext contém a Seção 5: Voz do Bairro", deepContext.includes("Seção 5: Voz do Bairro"));
  assertTest("DeepContext traz o ranking de demandas mais recorrentes", deepContext.includes("Ranking de Demandas Mais Recorrentes:"));
  assertTest("DeepContext inclui asfalto como demanda predominante de Canguera", deepContext.includes("Pavimentação") || deepContext.includes("Asfalto"));
  assertTest("DeepContext inclui protocolos georreferenciados no raio", deepContext.includes("Protocolos Georreferenciados no Entorno Imediato"));
  assertTest("DeepContext NUNCA contém identificadores FID numéricos", !/\bFID[_\s]?\d+/i.test(deepContext));

  console.log("\n======================================================================");
  console.log(`RESULTADO FINAL DOS TESTES: ${passedAssertions}/${totalAssertions} ASSERTIONS PASSARAM (0 falhas)`);
  console.log("======================================================================");
  console.log("[SUCESSO TOTAL] Seção 5 — Voz do Bairro 100% implementada, testada e integrada!");
}

runCommunityVoiceSuite().catch(err => {
  console.error("ERRO CRÍTICO NA EXECUÇÃO DOS TESTES:", err);
  process.exit(1);
});
