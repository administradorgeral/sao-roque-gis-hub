import urllib.request
import json

api_key = os.environ.get('GEMINI_API_KEY', '')
model = 'gemini-flash-latest'
url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

prompt = """Você é a Inteligência Territorial e Jurídica Oficial de São Roque/SP.
Sua postura é estritamente técnica, analítica, crítica e objetiva (sem juízo de valor moral, sem adjetivações vagas, sem alucinação).

Pergunta do usuário: "o que é ruim?" (interpretado tecnicamente como: diagnóstico de vulnerabilidades territoriais, passivos ambientais, gargalos de infraestrutura, riscos físicos/geológicos, restrições urbanísticas e conflitos identificados nas audiências públicas do Plano Diretor).

Responda de forma profunda, técnica e estruturada, abordando:
1. Vulnerabilidades Físico-Ambientais e Áreas de Risco (Declividade crítica >= 30%, inundações na bacia do Ribeirão Aracaí, fragilidade hidrogeológica da APA Itupararanga).
2. Gargalos Estruturais de Mobilidade (SP-270 Raposo Tavares como barreira urbana, estrangulamento na Estrada do Vinho SPV-077, segregação ferroviária em São João Novo).
3. Conflitos de Uso do Solo e Saneamento (Dispersão urbana, núcleos clandestinos sem rede de esgoto da Sabesp, pressão por desdobro de chácaras).
4. Vedações e Proibições Legais Expressas (Art. 3º Lei 6.766/79, APP da Lei 12.651/12, Leis Estaduais 10.100/98 e 9.866/97).
5. Manifestações Críticas da Sociedade Civil nas Audiências Públicas (COMDEMA, moradores de Maylasky, ACIA, etc.).
"""

data = {
    'contents': [{'parts': [{'text': prompt}]}],
    'generationConfig': {
        'temperature': 0.2,
        'maxOutputTokens': 1500
    }
}
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        out_text = res['candidates'][0]['content']['parts'][0]['text']
        with open('scripts/test_gemini_out.txt', 'w', encoding='utf-8') as f:
            f.write(out_text)
        print("Written successfully, length:", len(out_text))
except Exception as e:
    print('Error:', e)
