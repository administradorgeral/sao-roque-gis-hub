with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('1. Esfera Municipal (São Roque)')
if idx != -1:
    print('Trecho de 1. Esfera Municipal:')
    print(text[idx:idx+3000])
