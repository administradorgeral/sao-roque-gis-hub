with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('toggle-declividade')
if idx != -1:
    print('Trecho pós toggle-declividade:')
    print(text[idx:idx+1500])
