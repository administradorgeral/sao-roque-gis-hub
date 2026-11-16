import urllib.request
import json

api_key = os.environ.get('GEMINI_API_KEY', '')
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent?key={api_key}"

prompt = """Você é um especialista em Direito Urbanístico e Perícia Territorial ajudando um CIDADÃO LEIGO que vai discursar AGORA na Audiência Pública de Uso e Parcelamento do Solo de São Roque/SP (Revisão do Plano Diretor 2026).
Objetivo: Preparar uma fala oral (roteiro de discurso de 3 a 5 minutos), simples, mas com termos técnicos de peso, sem se complicar, com máxima firmeza e ZERO alucinação.

Dados concretos auditados de São Roque:
1. Locais e Casos Reais:
- FID 21 (ZUE Interesse Turístico, ~148 ha): Gleba que era 98% Rural e virou urbana/turística com salto de CA de 0.2 para 1.2 (6x de potencial construtivo) sem EIV.
- FID 30 (Zona Urbana Industrial, ~66 ha): Área de chácaras e turismo (antiga ZUE-DT) convertida em Zona Industrial pesada sem zona de amortecimento, ao lado de moradias.
- FID 1 (ZUE Chácaras Manancial, ~4.919 ha na APA Itupararanga): Traçado convoluto/tentacular com apêndices contornando matrículas privadas específicas na bacia de mananciais.
- Maylasky, Caetê e Monte Verde: Moradores pediram desdobro familiar de chácaras para herança e enfrentam barreiras e exigências severas, enquanto grandes glebas rurais foram convertidas em urbanas de forma privilegiada.
- Precedente TJ-SP: ADI nº 2048131 do Tribunal de Justiça de SP, que já anulou alteração de zoneamento em São Roque por falta de estudo técnico e desvio de finalidade.

2. Esvaziamento da Participação Social:
- Explicar como a participação do povo foi esvaziada (o povo pede serviços, saneamento e desdobro familiar; na surdina entram alterações de gabinetes sem ata ou solicitação comunitária).
- Ausência de mapas vetoriais abertos e estudos de capacidade viária/hídrica disponibilizados antes das audiências.

Estruture a fala em tópicos orais claros:
- Abertura com autoridade e respeito (para a mesa, vereadores e munícipes);
- 3 Denúncias Técnicas Objetivas com os locais exatos;
- A questão do "Dois pesos e duas medidas" (o cidadão comum vs grandes glebas);
- O esvaziamento da participação popular e o risco jurídico (alerta de anulação pelo TJ-SP);
- Conclusão com 3 pedidos formais para constar em ata.
"""

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2500}
}

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(res["candidates"][0]["content"]["parts"][0]["text"])
except Exception as e:
    print("ERRO:", e)
