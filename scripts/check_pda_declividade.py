import os

pda_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\legislacao\PDA_2019_Plano_Diretor_Ambiental_Sao_Roque.md"

if os.path.exists(pda_path):
    with open(pda_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"Total de linhas no PDA 2019: {len(lines)}")
    matches = []
    for idx, l in enumerate(lines):
        if any(k in l.lower() for k in ['decliv', 'relevo', '4.3.3', 'scorsatto', 'cerminaro', 'forte ondulado']):
            matches.append((idx + 1, l.strip()))
    print(f"Total de ocorrências: {len(matches)}")
    for m in matches[:25]:
        print(f"L{m[0]}: {m[1][:120]}")
else:
    print("Arquivo PDA não encontrado em:", pda_path)
