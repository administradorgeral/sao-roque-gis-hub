import pypdf
import re
import json

reader = pypdf.PdfReader('minuta_pd2026/Plano Diretor - Combined.pdf')

pages_text = []
for i in range(80):
    t = reader.pages[i].extract_text() or ''
    pages_text.append((i + 1, t))

print(f"Lidas 80 páginas de sugestões públicas.")

# Analisar os tópicos e sugestões
# Vamos extrair blocos de sugestões e comentários
full_text = "\n".join([f"=== PÁGINA {p} ===\n{txt}" for p, txt in pages_text])

# Salvar o texto bruto para análise detalhada
with open('data/sugestoes_publicas_raw.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Texto bruto salvo em data/sugestoes_publicas_raw.txt")
