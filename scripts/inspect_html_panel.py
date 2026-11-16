with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('floating-layers-panel')
if idx != -1:
    print('Trecho de floating-layers-panel:')
    print(text[idx:idx+2500])
