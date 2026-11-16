import urllib.request
import json

apiKey = os.environ.get('GEMINI_API_KEY', '')
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent?key={apiKey}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Pesquise na internet: Qual o status atual da revisão do Plano Diretor de São Roque em 2026? Liste as fontes com URLs."}
            ]
        }
    ],
    "tools": [
        {"googleSearch": {}}
    ]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=20) as res:
        print("Status:", res.status)
        resp_data = json.loads(res.read().decode("utf-8"))
        candidate = resp_data.get("candidates", [{}])[0]
        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        grounding = candidate.get("groundingMetadata", {})
        print("Text snippet:", text[:300])
        print("Grounding metadata:", json.dumps(grounding, indent=2, ensure_ascii=False)[:600])
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
