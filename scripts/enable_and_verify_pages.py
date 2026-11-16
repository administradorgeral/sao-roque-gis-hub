import urllib.request
import json
import time
import os

ENV_FILE = r'C:\Users\admin\.gemini\antigravity\scratch\central-inteligencia-sao-roque\.env'

def get_token():
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip()
    raise RuntimeError("GITHUB_TOKEN not found in .env")

def enable_pages():
    token = get_token()
    repo = "administradorgeral/sao-roque-gis-hub"
    url = f"https://api.github.com/repos/{repo}/pages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Antigravity-Agent"
    }

    # First check if pages is already enabled
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"Pages already enabled: {data.get('html_url')}")
            return data.get('html_url')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Pages not yet enabled, creating Pages site...")
        else:
            print(f"Check Pages error {e.code}: {e.read().decode()}")

    # Enable pages
    payload = json.dumps({
        "source": {
            "branch": "main",
            "path": "/"
        }
    }).encode('utf-8')

    post_req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(post_req) as resp:
            data = json.loads(resp.read().decode())
            print(f"GitHub Pages successfully enabled: {data.get('html_url')}")
            return data.get('html_url')
    except urllib.error.HTTPError as e:
        print(f"Enable Pages response ({e.code}): {e.read().decode()}")
        return None

def verify_online():
    page_url = "https://administradorgeral.github.io/sao-roque-gis-hub/"
    print(f"Verifying online accessibility: {page_url}")
    for attempt in range(1, 15):
        try:
            req = urllib.request.Request(page_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                content = resp.read(500).decode('utf-8', errors='ignore')
                print(f"Attempt {attempt}: HTTP {status}! Page content starts with:\n{content[:200]}")
                if status == 200:
                    print(f"\n[SUCESSO] GitHub Pages está 100% ONLINE e acessível em: {page_url}")
                    return True
        except urllib.error.HTTPError as e:
            print(f"Attempt {attempt}: HTTP {e.code} (GitHub Pages is building...) Waiting 10s...")
            time.sleep(10)
        except Exception as ex:
            print(f"Attempt {attempt}: Error: {ex}. Waiting 10s...")
            time.sleep(10)
    return False

if __name__ == '__main__':
    enable_pages()
    verify_online()
