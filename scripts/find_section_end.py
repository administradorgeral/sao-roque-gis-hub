with open(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Industrial</span>')
if idx != -1:
    print('Trecho pós Industrial:')
    print(text[idx:idx+1000])
