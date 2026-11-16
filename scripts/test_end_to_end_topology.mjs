/**
 * Teste End-to-End Programático de Topologia Cruzada e Modais
 * Validação de 100% dos fluxos por código puro sem navegador
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const baseDir = path.resolve(__dirname, '..');

// Mock DOM
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

  addEventListener() {}
  setAttribute(name, val) { this.attributes.set(name, String(val)); }
  getAttribute(name) { return this.attributes.get(name) || null; }
  appendChild(child) {
    this.children.push(child);
    if (child instanceof MockElement) {
      this.innerHTML += child.outerHTML || child.innerHTML || child.textContent;
    }
  }
  focus() {}
}

global.document = {
  getElementById: (id) => new MockElement(id),
  createElement: (tag) => new MockElement('', tag),
  createDocumentFragment: () => new MockElement('', 'fragment'),
  addEventListener: () => {}
};

// Importar módulos
const { AttributeModal } = await import('../js/modules/attribute-modal.js');
const { SpatialCrossEngine } = await import('../js/modules/spatial-cross-engine.js');
const { LegislationCatalog } = await import('../js/modules/legislation-catalog.js');

const modal = new AttributeModal();
const catalog = new LegislationCatalog(modal);
catalog.data = JSON.parse(fs.readFileSync(path.join(baseDir, 'data', 'rol_legislacao_territorial.json'), 'utf8'));

const crossEngine = new SpatialCrossEngine();
crossEngine.graph = JSON.parse(fs.readFileSync(path.join(baseDir, 'data', 'grafo_territorial_sao_roque.json'), 'utf8'));
crossEngine.buildIndices();
crossEngine.isLoaded = true;

console.log('='.repeat(70));
console.log('TESTE END-TO-END PROGRAMÁTICO: TOPOLOGIA CRUZADA & MODAIS');
console.log('='.repeat(70));

let passes = 0;
let fails = 0;

function check(cond, msg) {
  if (cond) {
    passes++;
    console.log(`  [PASS] ${msg}`);
  } else {
    fails++;
    console.error(`  [FAIL] ${msg}`);
  }
}

// 1. Simulação: Ponto em Canguera (Estrada do Vinho / APA)
console.log('\n[CENÁRIO 1] Ponto no Distrito de Canguera (-23.5869, -47.1201):');
const dossierCanguera = crossEngine.buildCrossDossierForPoint(-23.5869, -47.1201);
const legalCanguera = catalog.getZoneLegalMetadata(dossierCanguera.zoneamento_2006.sigla);
modal.showMultiLayerDossier(dossierCanguera, legalCanguera);

check(modal.titleEl.textContent.includes("Canguera") || modal.titleEl.textContent.includes("Raio"), "Título do modal identifica Canguera / via próxima");
check(modal.bodyEl.innerHTML.includes("APA da Represa de Itupararanga"), "Identifica APA de Itupararanga no dossiê");
check(modal.bodyEl.innerHTML.includes("Carta VII: Consolidação Urbana - Canguera"), "Identifica Carta VII de Canguera");
check(modal.bodyEl.innerHTML.includes("Carta XII: Sistema Viário e Drenagem - Canguera"), "Identifica Carta XII de drenagem e viário");
check(modal.bodyEl.innerHTML.includes("SRQ-15") || modal.bodyEl.innerHTML.includes("SRQ-16"), "Identifica obras prioritárias de Canguera da Carta XIII");
check(!modal.bodyEl.innerHTML.toLowerCase().includes("fid_"), "Zero FID_ no modal");

// 2. Simulação: Ponto em Maylasky (-23.5542, -47.0867)
console.log('\n[CENÁRIO 2] Ponto no Distrito de Maylasky (-23.5542, -47.0867):');
const dossierMaylasky = crossEngine.buildCrossDossierForPoint(-23.5542, -47.0867);
const legalMaylasky = catalog.getZoneLegalMetadata(dossierMaylasky.zoneamento_2006.sigla);
modal.showMultiLayerDossier(dossierMaylasky, legalMaylasky);

check(modal.bodyEl.innerHTML.includes("Carta V: Consolidação Urbana - Maylasky"), "Identifica Carta V de Maylasky");
check(modal.bodyEl.innerHTML.includes("Carta XI: Sistema Viário e Drenagem - Maylasky"), "Identifica Carta XI de Maylasky");
check(modal.bodyEl.innerHTML.includes("SRQ-09") || modal.bodyEl.innerHTML.includes("SRQ-10") || modal.bodyEl.innerHTML.includes("SRQ-11"), "Identifica obras prioritárias de Maylasky da Carta XIII");
check(!modal.bodyEl.innerHTML.toLowerCase().includes("fid "), "Zero FID no modal de Maylasky");

// 3. Simulação: Ponto na Sede (-23.5320, -47.1350)
console.log('\n[CENÁRIO 3] Ponto no Distrito Sede / Centro (-23.5320, -47.1350):');
const dossierSede = crossEngine.buildCrossDossierForPoint(-23.5320, -47.1350);
const legalSede = catalog.getZoneLegalMetadata("ZUC");
modal.showMultiLayerDossier(dossierSede, legalSede);

check(modal.bodyEl.innerHTML.includes("Carta IV: Consolidação Urbana - Distrito Sede"), "Identifica Carta IV da Sede");
check(modal.bodyEl.innerHTML.includes("Carta X: Sistema Viário e Drenagem - Sede"), "Identifica Carta X da Sede");
check(modal.bodyEl.innerHTML.includes("SRQ-01") || modal.bodyEl.innerHTML.includes("SRQ-02") || modal.bodyEl.innerHTML.includes("SRQ-03"), "Identifica piscinão Aracaí ou obras centrais");
check(!modal.bodyEl.innerHTML.toLowerCase().includes("fid "), "Zero FID no modal da Sede");

// 4. Confronto Rigoroso de Zoneamento (Vigente vs Proposta)
console.log('\n[CENÁRIO 4] Confronto Direto de Zoneamento (LC 40/06 vs Minuta 2026):');
const legalZCU = catalog.getZoneLegalMetadata("ZCU");
modal.showZoneLegalDetails("ZCU - Zona de Consolidação Urbana", {}, legalZCU);

check(modal.bodyEl.innerHTML.includes("Regime Vigente: Parâmetros Urbanísticos (LC 40/2006 & LC 39/2006)"), "Exibe explicitamente o Regime Vigente");
check(modal.bodyEl.innerHTML.includes("Regime Proposto: Minutas de Revisão (LC 39 e 40) & Cartas 2026"), "Exibe explicitamente o Regime Proposto");
check(modal.bodyEl.innerHTML.includes("Precedência das Leis Aplicáveis a este Local"), "Exibe Pirâmide de Kelsen com precedência federativa");

console.log('\n' + '='.repeat(70));
console.log(`TOTAL DE ASSERÇÕES: ${passes}/${passes + fails} PASSARAM`);
console.log('='.repeat(70));

if (fails > 0) process.exit(1);
