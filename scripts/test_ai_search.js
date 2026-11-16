const fs = require('fs');
const path = require('path');

const kbPath = path.join(__dirname, '..', 'data', 'base_conhecimento_ia.json');
const kb = JSON.parse(fs.readFileSync(kbPath, 'utf8'));

console.log('--- TESTANDO BASE DE CONHECIMENTO IA ---');
console.log('Metadados:', kb.metadata);
console.log('Tópicos IA:', kb.topicos_ia.length);
console.log('Zonas Parametrizadas:', Object.keys(kb.zonas_parametros).length);
console.log('Normas Resumo:', kb.normas_resumo.length);

const testQueries = [
  'Qual o recuo, taxa de ocupação e gabarito da Zona Central ZUC?',
  'Onde posso construir galpão industrial na ZUI?',
  'Quais as restrições da APA de Itupararanga?',
  'Qual a declividade máxima para loteamento?',
  'O que mudou na Minuta do Plano Diretor 2026?',
  'Quantos habitantes e domicílios São Roque tem no Censo IBGE 2022?'
];

testQueries.forEach(q => {
  const qNorm = q.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  let bestTopic = null;
  let highestScore = 0;

  for (const t of kb.topicos_ia) {
    let score = 0;
    for (const kw of t.palavras_chave) {
      const kwNorm = kw.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      if (qNorm.includes(kwNorm)) {
        score += 3;
      }
    }
    if (score > highestScore) {
      highestScore = score;
      bestTopic = t;
    }
  }

  console.log(`\n[QUERY] "${q}"`);
  if (bestTopic) {
    console.log(`  -> Match: [${bestTopic.id}] ${bestTopic.titulo} (score: ${highestScore})`);
    console.log(`  -> Resumo: ${bestTopic.resumo.slice(0, 110)}...`);
    console.log(`  -> Camada Sugerida: ${bestTopic.camada_sugerida} | Centro: ${bestTopic.centro_mapa}`);
  } else {
    console.log('  -> Sem match direto de tópico.');
  }
});
