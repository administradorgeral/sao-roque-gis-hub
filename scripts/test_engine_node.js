import { AISearchEngine } from '../js/modules/ai-search.js';
import fs from 'fs';

// Mock minimal DOM / Leaflet
global.window = {
  GIS: {
    getPinLocation: () => null
  },
  marked: null
};
global.localStorage = {
  getItem: (k) => null
};
global.document = {
  getElementById: () => null,
  querySelector: () => null,
  querySelectorAll: () => []
};

async function test() {
  const engine = new AISearchEngine(null, null, null, null);
  
  // Load knowledge base
  const kbRaw = fs.readFileSync('data/base_conhecimento_ia.json', 'utf8');
  engine.knowledgeBase = JSON.parse(kbRaw);

  console.log("Testing AISearchEngine.synthesizeAnswer('o que é ruim?')...");
  const result = await engine.synthesizeAnswer("o que é ruim?");

  console.log("--- RESULT META ---");
  console.log("Titulo:", result.titulo);
  console.log("Origem:", result.origem);
  console.log("isArgon:", result.isArgon);
  
  if (result.isArgon) {
    console.log("Markdown length:", result.markdownText.length);
    fs.writeFileSync('scripts/last_response.md', result.markdownText, 'utf8');
    console.log("Full response saved to scripts/last_response.md");
    console.log("Snippet:", result.markdownText.slice(0, 500));
  } else {
    console.log("Resumo snippet:", result.resumo.slice(0, 500));
  }
}

test().catch(console.error);
