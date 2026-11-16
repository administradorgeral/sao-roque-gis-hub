import urllib.request
import json

apiKey = os.environ.get('GEMINI_API_KEY', '')
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent?key={apiKey}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Diga 'Argon operacional' e cite a Lei 40/2006 de São Roque em uma frase."}
            ]
        }
    ]
}

req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=15) as res:
        print("Status:", res.status)
        resp_data = json.loads(res.read().decode("utf-8"))
        candidate = resp_data.get("candidates", [{}])[0]
        text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")
        print("Response:", text)
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
