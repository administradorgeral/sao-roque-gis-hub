/**
 * Script para carregar variáveis de ambiente do .env
 * e configurar o localStorage para o gemini-4-argon
 * 
 * Uso:
 *   - Crie um arquivo .env com base no .env.example
 *   - Execute: node scripts/load-env.js
 *   - Ou inclua este script no seu HTML antes do app.js
 */

// Função para parsear arquivo .env
function parseEnvFile(content) {
  const lines = content.split('\n');
  const env = {};
  
  for (const line of lines) {
    // Ignora linhas vazias e comentários
    if (!line.trim() || line.trim().startsWith('#')) continue;
    
    const [key, ...valueParts] = line.split('=');
    const keyTrimmed = key?.trim();
    const value = valueParts.join('=').trim();
    
    if (keyTrimmed && value) {
      // Remove aspas se existirem
      env[keyTrimmed] = value.replace(/^['"]|['"]$/g, '');
    }
  }
  
  return env;
}

// Carregar do arquivo .env
try {
  const fs = require('fs');
  const path = require('path');
  const envPath = path.join(process.cwd(), '.env');
  
  if (fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf8');
    const env = parseEnvFile(envContent);
    
    if (env.GEMINI_API_KEY) {
      console.log('✓ API key carregada do .env');
      console.log('  Para usar no browser, execute:');
      console.log(`  localStorage.setItem('SR_GEMINI_API_KEY', '${env.GEMINI_API_KEY.substring(0, 10)}...')`);
    } else {
      console.log('✗ GEMINI_API_KEY não encontrado no .env');
    }
  } else {
    console.log('✗ Arquivo .env não encontrado');
    console.log('  Copie .env.example para .env e preencha com sua API key');
  }
} catch (e) {
  // No browser
  console.log('Carregando configuração do .env para o browser...');
  
  // Tentar carregar via fetch (para desenvolvimento local)
  if (typeof fetch !== 'undefined') {
    fetch('.env')
      .then(resp => resp.text())
      .then(content => {
        const env = parseEnvFile(content);
        if (env.GEMINI_API_KEY) {
          localStorage.setItem('SR_GEMINI_API_KEY', env.GEMINI_API_KEY);
          console.log('✓ API key carregada do .env para localStorage');
        }
      })
      .catch(() => {
        console.log('✗ Não foi possível carregar .env via fetch');
      });
  }
}

// Exportar função para uso programático
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { parseEnvFile };
}
