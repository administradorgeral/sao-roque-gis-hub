import urllib.request
import json

apiKey = os.environ.get('GEMINI_API_KEY', '')
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={apiKey}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Qual a situação atual da revisão do Plano Diretor de São Roque em 2026? Cite fontes e URLs se disponíveis."}
            ]
        }
    ],
    "tools": [
        {"googleSearch": {}}
    ]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=15) as res:
        print("Status:", res.status)
        resp_data = json.loads(res.read().decode("utf-8"))
        candidate = resp_data.get("candidates", [{}])[0]
        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        grounding = candidate.get("groundingMetadata", {})
        print("Text snippet:", text[:300])
        print("Grounding metadata keys:", list(grounding.keys()))
        queries = grounding.get("webSearchQueries", [])
        print("Search queries executed:", queries)
        sources = grounding.get("groundingChunks", [])
        print("Sources count:", len(sources))
        for s in sources[:3]:
            web = s.get("web", {})
            print(f"- {web.get('title')}: {web.get('uri')}")
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
