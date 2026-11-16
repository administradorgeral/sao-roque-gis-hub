with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('toggle-minuta-zoneamento')
if idx != -1:
    print('Trecho de minuta-zoneamento:')
    print(text[idx-200:idx+1500])
