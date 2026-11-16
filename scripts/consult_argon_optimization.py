import urllib.request
import json

api_key = os.environ.get('GEMINI_API_KEY', '')
model = 'gemini-4-argon'
url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

consultation_prompt = """Você é o arquiteto de software e especialista em Inteligência Geoespacial e LLMs de alta performance.
Estamos refatorando o motor de IA Territorial do São Roque GIS Hub.

O usuário deu a seguinte orientação:
"Em parceria com o argon. pense na refatoração do código para que ele tenha o máximo de informação embasada com o mínimo de carga. e que a resposta não fique cortada. Estamos um pouco sem tempo então use os mcps junto com ele para encontrar a melhor solução em inteligência avançada e resposta embasada. permitido instalar complementos e configurar.."

DESAFIOS TÉCNICOS A RESOLVER:
1. MÁXIMO DE EMBASAMENTO COM MÍNIMO DE CARGA (High-Density Context Engineering):
   - Como comprimir e destilar as 33 camadas, 13 Cartas, 28 zonas, 22 obras (SRQ-01..22), normas (Lei 6.766, 12.651, APA, LC 40/06, Minuta 2026) e audiências públicas em um payload semântico ultra-denso (~1.000 tokens de contexto) que permita ao Gemini 4 Argon responder em altíssima velocidade (< 5 segundos) sem perder 1% da precisão jurídica e territorial.
2. RESPOSTA 100% COMPLETA E NUNCA CORTADA (Zero Truncation Guarantee):
   - Como calibrar maxOutputTokens, prompt framing e CSS/UI para que a resposta nunca seja cortada no meio de uma frase, tabela ou seção.
   - Como garantir que o modelo conclua formalmente todas as seções (os 5 Eixos) de forma fluida e termine com um parecer executivo conclusivo.
3. MELHORIA NO CÓDIGO JS / UI (ai-search.js e CSS):
   - Ajustes pontuais no ai-search.js e CSS para renderizar tabelas responsivas, expandir largura do card (ex: 850px no desktop), rolagem suave sem corte, e binding reativo de botões Leaflet ([[ACTION:LAYER:...]], [[ACTION:FLYTO:...]], [[ACTION:OBRA:...]]).

Forneça a especificação técnica exata, o prompt de alta densidade semântica e os trechos de código refinados para implementação imediata.
"""

payload = {
    'contents': [{'parts': [{'text': consultation_prompt}]}],
    'generationConfig': {
        'temperature': 0.1,
        'maxOutputTokens': 2500
    }
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        answer = res['candidates'][0]['content']['parts'][0]['text']
        with open('scripts/argon_optimization_plan.md', 'w', encoding='utf-8') as f:
            f.write(answer)
        print("Plano de Otimização gerado com sucesso pelo Gemini 4 Argon! Tamanho:", len(answer))
except Exception as e:
    print("Erro:", e)
