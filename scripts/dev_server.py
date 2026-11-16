import http.server
import socketserver
import json
import urllib.request
import urllib.error
import os
import sys

PORT = 8000
REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_gemini_key():
    return os.environ.get('GEMINI_API_KEY', '')

class SpatialDevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(405)
        self.send_header('Allow', 'POST')
        self.end_headers()

    def do_POST(self):
        if self.path != '/api/argon':
            self.send_error(404)
            return

        origin = self.headers.get('Origin')
        allowed_origins = {f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}'}
        if origin and origin not in allowed_origins:
            self.send_error(403, 'Origem não autorizada')
            return

        try:
            content_len = int(self.headers.get('Content-Length', 0))
        except ValueError:
            self.send_error(400, 'Content-Length inválido')
            return
        if content_len <= 0 or content_len > 256_000:
            self.send_error(413, 'Tamanho da consulta inválido')
            return

        try:
            data = json.loads(self.rfile.read(content_len).decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, 'JSON inválido')
            return

        if not isinstance(data, dict) or not isinstance(data.get('contents'), list) or not data['contents']:
            self.send_error(400, 'Conteúdo Gemini inválido')
            return

        key = get_gemini_key()
        if not key:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "GEMINI_API_KEY não configurada no servidor"}).encode('utf-8'))
            return

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-4-argon:generateContent"
        payload = {
            "contents": data["contents"],
            "generationConfig": data.get("generationConfig", {
                "temperature": 0.45,
                "maxOutputTokens": 3500
            })
        }
        req = urllib.request.Request(
            f'{url}?key={key}',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req, timeout=75) as resp:
                resp_data = resp.read()
                self.send_response(resp.status)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp_data)
        except urllib.error.HTTPError as error:
            self.send_response(error.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error.read())
        except urllib.error.URLError:
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Não foi possível conectar à API Gemini"}).encode('utf-8'))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), SpatialDevHandler) as httpd:
        print(f"SpatialDevServer running on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == '__main__':
    run()
