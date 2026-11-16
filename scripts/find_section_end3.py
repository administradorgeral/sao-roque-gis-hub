with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('legend-minuta-zoneamento')
if idx != -1:
    print('Trecho pós legend-minuta-zoneamento:')
    print(text[idx+1000:idx+2500])
