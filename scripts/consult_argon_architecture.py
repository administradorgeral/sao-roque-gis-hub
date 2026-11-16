import urllib.request
import json
import os

api_key = os.environ.get('GEMINI_API_KEY', '')
model = 'gemini-4-argon'
url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

system_prompt = """Você é o arquiteto de software e especialista em IA Geoespacial e Direito Urbanístico sênior.
Estamos aprimorando o sistema 'São Roque GIS Hub' (WebGIS em Leaflet ES6 + banco SQLite sao_roque_geodados.db + 33 camadas geográficas + 13 Cartas do Plano Diretor 2026 + 1.709 artigos jurídicos + vetor de participação popular).

PROBLEMA ATUAL:
O usuário perguntou: "o que é ruim?"
A resposta anterior foi rasa e pré-fabricada (apenas 3 tópicos genéricos sobre declividade, APA e ZUI).
O usuário pontuou com razão: "concorda que essa resposta é limitada e não abrange a profundidade do plano diretor, das legislações e não é exaustivo está autorizado refatorar código. buscar soluções no mcps, instalar ou reconfigurar o meganismo para que a abrangência seja exaustiva e simultaneamente técnica."

SUA MISSÃO COMO GEMINI-4-ARGON:
Apresente uma análise arquitetural detalhada e proposta técnica de código para refatorar o motor de IA territorial (ai-search.js, base de conhecimento e integração direta com a API do Gemini):

1. COMO INTERPRETAR PERGUNTAS CONCEITUAIS E AMPLAS (como 'o que é ruim?', 'quais as fragilidades?', 'o que é proibido?', 'quais são os conflitos fundiários?'):
   - Mapear a pergunta para os eixos de diagnóstico territorial: (a) Riscos e Vulnerabilidades Físico-Ambientais; (b) Gargalos de Mobilidade e Conectividade; (c) Conflitos de Uso do Solo e Saneamento; (d) Ilegalidades e Vedações Normativas Explícitas; (e) Demandas Críticas das Audiências Públicas.

2. ARQUITETURA HÍBRIDA ROBUSTA DE RAG (Retrieval-Augmented Generation):
   - Como construir o prompt de sistema definitivo e a injeção contextual dinâmica (com seleção de pin ativa ou inativa).
   - Como alimentar o modelo com o corpus territorial (33 camadas, 13 cartas, 22 obras prioritárias SRQ-01 a SRQ-22, parâmetros das 28 zonas, participações populares e artigos de lei relevantes).
   - Como garantir que a resposta no WebGIS seja formatada com Markdown rico, badges técnicos, parâmetros exatos e ações no mapa Leaflet.

3. ESTRATÉGIA DE CÓDIGO (JavaScript no WebGIS):
   - Integração direta e segura no navegador chamando a API do Gemini com o modelo 'gemini-4-argon' (com fallback inteligente para o motor semântico local se estiver offline).
   - Como renderizar a resposta com profundidade exaustiva, streaming ou carregamento suave, tabelas comparativas, links para as leis e botões de ação cartográfica.

Forneça orientações precisas, código e estrutura de prompt prontos para implementação.
"""

payload = {
    'contents': [{'parts': [{'text': system_prompt}]}],
    'generationConfig': {
        'temperature': 0.1,
        'maxOutputTokens': 3000
    }
}

print(f"Consultando modelo {model}...")
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        answer = res['candidates'][0]['content']['parts'][0]['text']
        out_file = 'scripts/argon_architecture_recommendation.md'
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(answer)
        print(f"Recomendações salvas em {out_file} ({len(answer)} caracteres).")
except Exception as e:
    print("Erro:", e)
