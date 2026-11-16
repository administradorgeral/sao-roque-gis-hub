import urllib.request
import json

apiKey = os.environ.get('GEMINI_API_KEY', '')
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={apiKey}"

req = urllib.request.Request(url)
try:
    with urllib.request.urlopen(req, timeout=10) as res:
        data = json.loads(res.read().decode("utf-8"))
        models = [m.get("name") for m in data.get("models", [])]
        print(f"Total models available: {len(models)}")
        for m in models:
            if "flash" in m or "pro" in m or "argon" in m or "gemini" in m:
                print(m)
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
