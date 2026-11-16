import urllib.request
import json

api_key = os.environ.get('GEMINI_API_KEY', '')
model = 'gemini-4-argon'
url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

prompt = """Você é o arquiteto de software e especialista em Inteligência Geoespacial, Auditoria Territorial e Direito Urbanístico sênior do São Roque GIS Hub.

O usuário nos enviou a seguinte reflexão crítica:
\"acho que faltou a inteligência que consiga identificar o perímetro das propostas. identificando erros grosseiros ou preferências escusas e duvidosas ao invés de adotar estratégia mais benéfica. consegue discutir com o argon se é necessário, como fazer isso e se é util?\"

SUA MISSÃO COMO GEMINI-4-ARGON:
Discuta a fundo esta questão de forma estruturada, respondendo:

1. É NECESSÁRIO E É ÚTIL?
   - Faça a defesa técnica e institucional de por que uma auditoria algorítmica de perímetros e propostas é CRUCIAL no controle social, na prevenção à improbidade administrativa (Lei 8.429/92), na garantia da função social da propriedade (Estatuto da Cidade Lei 10.257/01) e no histórico de São Roque (ex: a ADI TJ-SP 2048131-35 que anulou leis urbanísticas por casuísmo sem estudos técnicos).

2. COMO FAZER ISSO SEM SUBJETIVIDADE, JULGAMENTO LEVIANO OU ALUCINAÇÃO?
   - Defina a metodologia e os 5 Indicadores Objetivos e Matemáticos de Anomalia Perimetral / Desvio de Finalidade Urbanística ("Spot Zoning" / Casuísmo):
     * Indicador A: Geometria Anômala e Ruptura de Continuidade (polígonos digitados com "dedos" ou contornos de matrícula sem justificativa de bacia ou via).
     * Indicador B: Incompatibilidade Biofísica e Risco Geotécnico (expansão urbana proposta sobre declividade >= 30%, várzeas ou mananciais da APA sem capacidade de suporte).
     * Indicador C: Discrepância Desproporcional de Parâmetros / Mais-Valia Especulativa (salto de CA/TO ou liberação de uso de alto impacto em gleba isolada cercada por zonas restritivas).
     * Indicador D: Descompasso entre Adensamento e Rede de Infraestrutura (proposta de alta densidade sem rede Sabesp ou acesso viário estruturado).
     * Indicador E: Rastreabilidade Decisória e Déficit de Participação (alteração perimetral que não decorre das oficinas técnicas nem das atas de audiência pública).

3. PROPOSTA DE ARQUITETURA E IMPLEMENTAÇÃO NO SÃO ROQUE GIS HUB:
   - Como implementar o motor de cruzamento espacial no WebGIS (cruzando os GeoJSONs de Zoneamento 2006 vs Minuta 2026, Declividade, APA e Hidrografia).
   - Como o assistente de IA deve reportar isso ao usuário quando:
     a) O pin marker for posicionado sobre uma gleba de perímetro anômalo/suspeito.
     b) O usuário fizer perguntas como "existem perímetros suspeitos?", "onde houve favorecimento?", "quais propostas são incoerentes ou ilegais?".

Forneça um parecer aprofundado, técnico, fundamentado no Direito Urbanístico e na Ciência da Geoinformação.
"""

payload = {
    'contents': [{'parts': [{'text': prompt}]}],
    'generationConfig': {
        'temperature': 0.1,
        'maxOutputTokens': 3500
    }
}

print("Consultando o Gemini 4 Argon sobre auditoria de perímetros e casuísmo urbanístico...")
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        answer = res['candidates'][0]['content']['parts'][0]['text']
        out_file = 'scripts/argon_perimetros_auditoria_discussao.md'
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(answer)
        print(f"Discussão salva com sucesso em {out_file}! Tamanho: {len(answer)} caracteres.")
except Exception as e:
    print("Erro:", e)
