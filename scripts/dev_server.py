import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import sys

PORT = 8000
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENV_FILE = r'C:\Users\admin\.gemini\antigravity\scratch\central-inteligencia-sao-roque\.env'

def get_gemini_key():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip()
    return os.environ.get('GEMINI_API_KEY', '')

class SpatialDevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/config') or self.path.startswith('/api/key'):
            key = get_gemini_key()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            resp = {
                "status": "ok",
                "apiKey": key,
                "model": "gemini-4-argon",
                "hasKey": bool(key)
            }
            self.wfile.write(json.dumps(resp).encode('utf-8'))
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/argon'):
            content_len = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_len).decode('utf-8')
            try:
                data = json.loads(body)
            except Exception:
                data = {}

            key = get_gemini_key()
            if not key:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "GEMINI_API_KEY não configurada no servidor"}).encode('utf-8'))
                return

            model = data.get('model', 'gemini-4-argon')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

            payload = {
                "contents": data.get("contents", []),
                "generationConfig": data.get("generationConfig", {
                    "temperature": 0.15,
                    "maxOutputTokens": 3500
                })
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_data = resp.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(resp_data)
            except urllib.error.HTTPError as e:
                err_body = e.read()
                self.send_response(e.code)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(err_body)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SpatialDevHandler) as httpd:
        print(f"SpatialDevServer running on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
