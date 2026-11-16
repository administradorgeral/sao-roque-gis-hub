with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Minuta Prévia (Estudo Técnico PMD 2006)')
if idx != -1:
    print('Trecho pós Minuta Prévia:')
    print(text[idx:idx+1500])
