import urllib.request
import urllib.parse
import re

url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('Sao Roque plano diretor')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=10) as r:
    data = r.read().decode('utf-8', errors='ignore')

print("Data length:", len(data))
print("Sample lines:")
for line in data.splitlines()[:60]:
    if 'result' in line.lower() or 'href' in line.lower() or 'class' in line.lower():
        print(line[:120])
