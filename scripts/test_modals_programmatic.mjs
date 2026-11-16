/**
 * Teste Programático Automatizado de Modais e Inteligência Territorial
 * Sem dependência visual de navegador: Teste por código puro (Node.js)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const baseDir = path.resolve(__dirname, '..');

// Carregar bases de dados oficiais
const rolPath = path.join(baseDir, 'data', 'rol_legislacao_territorial.json');
const grafoPath = path.join(baseDir, 'data', 'grafo_territorial_sao_roque.json');
const baseKbPath = path.join(baseDir, 'data', 'base_conhecimento_ia.json');

const rolData = JSON.parse(fs.readFileSync(rolPath, 'utf8'));
const grafoData = JSON.parse(fs.readFileSync(grafoPath, 'utf8'));
const baseKbData = JSON.parse(fs.readFileSync(baseKbPath, 'utf8'));

console.log('='.repeat(70));
console.log('SUITE DE TESTES PROGRAMÁTICOS: MODAIS E DADOS PERICIAIS DE DEBATE');
console.log('='.repeat(70));

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function assert(condition, message) {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  [PASS] ${message}`);
  } else {
    failedTests++;
    console.error(`  [FAIL] ${message}`);
  }
}

// -------------------------------------------------------------
// MOCK DO DOM DO NAVEGADOR PARA TESTES PROGRAMÁTICOS DO MODAL
// -------------------------------------------------------------
class MockElement {
  constructor(id = '', tagName = 'div') {
    this.id = id;
    this.tagName = tagName;
    this.attributes = new Map();
    this.children = [];
    this.innerHTML = '';
    this.textContent = '';
    this.style = {};
    this.classList = new Set();
  }

  addEventListener(event, handler) {
    this.listeners = this.listeners || {};
    this.listeners[event] = this.listeners[event] || [];
    this.listeners[event].push(handler);
  }

  setAttribute(name, val) {
    this.attributes.set(name, String(val));
  }

  getAttribute(name) {
    return this.attributes.get(name) || null;
  }

  appendChild(child) {
    this.children.push(child);
    if (child instanceof MockElement) {
      this.innerHTML += child.outerHTML || child.innerHTML || child.textContent;
    }
  }

  focus() {
    this.focused = true;
  }
}

// Global DOM mock
global.document = {
  getElementById: (id) => new MockElement(id),
  createElement: (tag) => new MockElement('', tag),
  createDocumentFragment: () => new MockElement('', 'fragment'),
  addEventListener: () => {}
};

// Importar módulo AttributeModal
const { AttributeModal } = await import('../js/modules/attribute-modal.js');

// -------------------------------------------------------------
// TESTE 1: Mapeamento de Zonas e Resolução de Parâmetros
// -------------------------------------------------------------
console.log('\n--- TESTE 1: Resolução de Metadados Jurídicos de Zoneamento ---');
const { LegislationCatalog } = await import('../js/modules/legislation-catalog.js');

const dummyModal = new AttributeModal();
const catalog = new LegislationCatalog(dummyModal);
catalog.data = rolData;

const testZones = [
  { input: "ZCU", expectedCode: "MACROZONA_CONSOLIDACAO", label: "Consolidação Urbana (Vigente)" },
  { input: "Consolidação urbana", expectedCode: "MACROZONA_CONSOLIDACAO", label: "Consolidação Urbana por Nome" },
  { input: "ZUC", expectedCode: "ZUR_CENTRAL", label: "Zona Urbana Central" },
  { input: "Central", expectedCode: "ZUR_CENTRAL", label: "Central por Nome" },
  { input: "ZUE-DT", expectedCode: "ZUE_TURISTICO", label: "ZUE Interesse Turístico (Proposta 2026)" },
  { input: "ZUE - Interesse Turístico", expectedCode: "ZUE_TURISTICO", label: "ZUE Turístico por Extenso" },
  { input: "ZUE-CM", expectedCode: "ZUE_MANANCIAL", label: "ZUE Chácaras em Manancial (Proposta 2026)" },
  { input: "ZUR-md", expectedCode: "ZUR_MEDIA", label: "Densidade Média" },
  { input: "ZUR-bd", expectedCode: "ZUR_BAIXA", label: "Densidade Baixa" },
  { input: "ZUI", expectedCode: "ZUR_INDUSTRIAL", label: "Zona Industrial" },
  { input: "ZR", expectedCode: "MACROZONA_RURAL", label: "Zona Rural" },
  { input: "PVA", expectedCode: "PVA19", label: "Solo Argissolo PVA" },
  { input: "APA", expectedCode: "PERIMETRO_APA_ITUPARARANGA", label: "APA Itupararanga" },
  { input: "SRQ_OBRAS", expectedCode: "SRQ_OBRAS", label: "Obras Prioritárias Carta XIII" }
];

testZones.forEach(tz => {
  const meta = catalog.getZoneLegalMetadata(tz.input);
  assert(meta !== null, `Zona '${tz.input}' deve retornar metadados não nulos`);
  assert(meta?.codigo === tz.expectedCode, `Zona '${tz.input}' deve mapear para código '${tz.expectedCode}' (obtido: ${meta?.codigo})`);
  assert(meta?.parametros !== null, `Zona '${tz.input}' deve possuir parâmetros urbanísticos cadastrados`);
  assert(Array.isArray(meta?.leis_aplicaveis) && meta.leis_aplicaveis.length > 0, `Zona '${tz.input}' deve listar leis aplicáveis da pirâmide (obtido: ${meta?.leis_aplicaveis?.length})`);
});

// -------------------------------------------------------------
// TESTE 2: Modal Especializado de Norma Jurídica (showLawDetails)
// -------------------------------------------------------------
console.log('\n--- TESTE 2: Modal de Norma Jurídica (showLawDetails) ---');
const modalTest = new AttributeModal();

const sampleLaw = rolData.leis.municipal.find(l => l.numero === '40' && l.ano === 2006);
assert(sampleLaw != null, "LC 40/2006 deve existir no rol oficial");

modalTest.showLawDetails(sampleLaw);
assert(modalTest.titleEl.textContent.includes("Lei Complementar nº 40/2006"), "Título do modal de lei deve conter o diploma oficial");
assert(modalTest.bodyEl.innerHTML.includes("Em Vigor / Direito Positivo Eficaz"), "LC 40/2006 deve ser rotulada como Em Vigor / Direito Positivo");
assert(modalTest.bodyEl.innerHTML.includes("Pirâmide de Kelsen"), "Modal deve apresentar o banner da Pirâmide de Kelsen");
assert(modalTest.bodyEl.innerHTML.includes("id=157183") || modalTest.bodyEl.innerHTML.includes("legislativo.camarasaoroque"), "Modal deve incluir o link oficial direto da norma");
assert(!modalTest.bodyEl.innerHTML.toLowerCase().includes("fid "), "Modal de lei não deve conter menção a FID");

// -------------------------------------------------------------
// TESTE 3: Modal de Zoneamento com Confronto (Vigente vs Proposta)
// -------------------------------------------------------------
console.log('\n--- TESTE 3: Modal de Zoneamento (showZoneLegalDetails) ---');
const zueMeta = catalog.getZoneLegalMetadata("ZUE-DT");
modalTest.showZoneLegalDetails("ZUE - Interesse Turístico", { denominacao: "ZUE - Interesse Turístico" }, zueMeta);

assert(modalTest.titleEl.textContent === "ZUE - Interesse Turístico", "Título deve ser semântico");
assert(modalTest.bodyEl.innerHTML.includes("Regime Vigente: Parâmetros Urbanísticos"), "Deve conter cabeçalho do Regime Vigente");
assert(modalTest.bodyEl.innerHTML.includes("Regime Proposto: Minutas de Revisão"), "Deve conter cabeçalho do Regime Proposto 2026");
assert(modalTest.bodyEl.innerHTML.includes("Precedência das Leis Aplicáveis a este Local"), "Deve conter seção da Pirâmide de Kelsen");
assert(!modalTest.bodyEl.innerHTML.toLowerCase().includes("fid "), "NÃO deve conter FID");

// -------------------------------------------------------------
// TESTE 4: Modal de Obra Estruturante da Carta XIII
// -------------------------------------------------------------
console.log('\n--- TESTE 4: Modal de Obra Estruturante da Carta XIII ---');
const obraProp = {
  codigo: "SRQ-15",
  nome: "Ciclovia e Bolsões Turísticos na Estrada do Vinho",
  local: "Estrada do Vinho (SPV-077) - Canguera",
  descricao: "Implantação de ciclovia segregada de 10 km e 4 bolsões de descanso com sanitários e ponto de apoio ao cicloturista."
};
modalTest.show("Obra SRQ-15", obraProp);

assert(modalTest.titleEl.textContent === "Obra SRQ-15", "Título da obra correto");
assert(modalTest.bodyEl.innerHTML.includes("Intervenção Prioritária (Carta XIII - PD 2026)"), "Deve identificar a Carta XIII");
assert(modalTest.bodyEl.innerHTML.includes("SRQ-15"), "Deve conter o código SRQ-15");
assert(modalTest.bodyEl.innerHTML.includes("Estrada do Vinho"), "Deve conter a localização");
assert(!modalTest.bodyEl.innerHTML.toLowerCase().includes("fid "), "NÃO deve conter FID");

// -------------------------------------------------------------
// TESTE 5: Modal de Logradouro / Via Oficial
// -------------------------------------------------------------
console.log('\n--- TESTE 5: Modal de Via Pública / Logradouro ---');
const viaProp = {
  denominacao: "Estrada do Vinho",
  tipo_via: "Estrada Turística / Vicinal",
  bairro: "Canguera",
  cod_logradouro: "SPV-077"
};
modalTest.show("Estrada do Vinho", viaProp);

assert(modalTest.titleEl.textContent === "Estrada do Vinho", "Título da via correto");
assert(modalTest.bodyEl.innerHTML.includes("Eixo do Sistema Viário Oficial de São Roque"), "Deve identificar sistema viário");
assert(modalTest.bodyEl.innerHTML.includes("Estrada Turística / Vicinal"), "Deve exibir tipologia");
assert(modalTest.bodyEl.innerHTML.includes("Canguera"), "Deve exibir bairro");
assert(!modalTest.bodyEl.innerHTML.toLowerCase().includes("fid "), "NÃO deve conter FID");

// -------------------------------------------------------------
// TESTE 6: Dossiê Territorial Multidimensional Completo ("Tudo Ligado a Tudo")
// -------------------------------------------------------------
console.log('\n--- TESTE 6: Dossiê Multidimensional Completo (showMultiLayerDossier) ---');
const mockDossier = {
  coordenadas: { lat: -23.58696, lng: -47.12019 },
  logradouro: {
    nome: "Estrada do Vinho",
    camada: "Sistema Viário Municipal",
    distancia_m: 12,
    tipo_via: "Estrada Municipal"
  },
  bairro: { nome: "Canguera", camada: "Bairros Oficiais" },
  distrito: { nome: "Distrito de Canguera", camada: "Divisão Distrital" },
  zoneamento_2006: {
    camada: "Zoneamento Homologado Vigente (LC 40/2006)",
    legenda_oficial: "ZUE-DT · ZUE - Interesse Turístico",
    sigla: "ZUE-DT",
    denominacao: "ZUE - Interesse Turístico",
    parametros: zueMeta.parametros
  },
  plano_diretor_2026: {
    camada: "Revisão do Plano Diretor Municipal (2026)",
    cartas_incidentes: [
      "Carta I: Macrozoneamento Municipal (2026)",
      "Carta II: ZUE - Urbanização Específica (2026)",
      "Carta VII: Consolidação Urbana - Canguera (2026)",
      "Carta XII: Sistema Viário e Drenagem - Canguera (2026)",
      "Carta XIII: Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (2026)"
    ]
  },
  pedologia_solos: {
    camada: "Pedologia e Solos",
    legenda_oficial: "PVA19 · Argissolos Vermelho-Amarelos",
    macroclasse: "PVA",
    textura: "Média a Argilosa",
    permeabilidade: "Moderada a Lenta",
    implicacao_obras: "Exige drenagem pluvial e contenção de encostas."
  },
  geologia_geotecnia: {
    camada: "Geologia de Engenharia",
    legenda_oficial: "Granito Ibiúna",
    litologia: "Rochas graníticas intrusivas",
    comportamento_geotecnico: "Maciço rochoso estável."
  },
  unidade_conservacao_apa: {
    camada: "Área de Proteção Ambiental de Itupararanga",
    legenda_oficial: "APA da Represa de Itupararanga (Lei Estadual 11.579/03)",
    restricoes: "Lote mínimo de 5.000m²; esgotamento com tratamento biológico obrigatório."
  },
  obras_estruturantes_proximas: [obraProp],
  demandas_populares: [
    {
      tema: "Proteção Ambiental e Mananciais",
      pedido_principal: "Proteção estrita da Bacia da Represa de Itupararanga contra contaminação.",
      posicao_tecnica_prefeitura: "Acolhido integralmente na Carta II e no Quadro I da nova LC 40."
    }
  ]
};

modalTest.showMultiLayerDossier(mockDossier, zueMeta);

assert(modalTest.bodyEl.innerHTML.includes("Regime Vigente: Zoneamento Homologado (LC 40/2006 & LC 39/2006)"), "Dossiê deve conter card explícito do Regime Vigente");
assert(modalTest.bodyEl.innerHTML.includes("Regime Proposto: Minutas de Revisão (LC 39 e 40) & Cartas 2026"), "Dossiê deve conter card explícito do Regime Proposto 2026");
assert(modalTest.bodyEl.innerHTML.includes("Carta II: ZUE - Urbanização Específica (2026)"), "Dossiê deve listar a Carta II");
assert(modalTest.bodyEl.innerHTML.includes("Carta XIII: Obras Estruturantes Prioritárias"), "Dossiê deve listar a Carta XIII");
assert(modalTest.bodyEl.innerHTML.includes("PVA19 · Argissolos Vermelho-Amarelos"), "Dossiê deve conter pedologia");
assert(modalTest.bodyEl.innerHTML.includes("Granito Ibiúna"), "Dossiê deve conter geologia");
assert(modalTest.bodyEl.innerHTML.includes("APA da Represa de Itupararanga"), "Dossiê deve conter status de mananciais da APA");
assert(modalTest.bodyEl.innerHTML.includes("Vetor de Participação Popular"), "Dossiê deve conter demandas das audiências públicas");
assert(modalTest.bodyEl.innerHTML.includes("Precedência Normativa Aplicável a este Ponto"), "Dossiê deve conter a Pirâmide de Kelsen");
assert(!modalTest.bodyEl.innerHTML.toLowerCase().includes("fid "), "Dossiê NUNCA deve conter menção a FID");

// -------------------------------------------------------------
// TESTE 7: Chamada com Objeto Único { title, content } (Prevenção de Regressão)
// -------------------------------------------------------------
console.log('\n--- TESTE 7: Prevenção de Regressão de Objeto Único { title, content } ---');
modalTest.show({
  title: "Ficha Técnica Personalizada",
  content: "<p id='custom-content'>Conteúdo renderizado com sucesso sem erro de string</p>"
});

assert(modalTest.titleEl.textContent === "Ficha Técnica Personalizada", "Deve aceitar objeto com propriedade title");
assert(modalTest.bodyEl.innerHTML.includes("Conteúdo renderizado com sucesso"), "Deve aceitar objeto com propriedade content");

// -------------------------------------------------------------
// RELATÓRIO FINAL DA SUÍTE DE TESTES
// -------------------------------------------------------------
console.log('\n' + '='.repeat(70));
console.log(`RESULTADO FINAL DOS TESTES: ${passedTests}/${totalTests} PASSARAM (${failedTests} falhas)`);
console.log('='.repeat(70));

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log('[SUCESSO TOTAL] Todos os modais atendem aos objetivos e exibem informações pertinentes ao debate!');
}
