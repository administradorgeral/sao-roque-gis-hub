import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]
tp = page.get_textpage()
text = tp.get_text_range(0, tp.count_chars())

print(f"Comprimento do texto: {len(text)}")
# Print every line in the text
lines = [l.strip() for l in text.split("\n") if l.strip()]
print(f"Total de linhas de texto: {len(lines)}")

# Let's inspect all lines that are NOT street or neighborhood names:
for idx, l in enumerate(lines):
    if any(k in l.upper() for k in ["ZONA", "URBANA", "RURAL", "LEGENDA", "ESPECÍFICA", "LIMITE", "ÁREA", "CONSOLIDAÇÃO"]):
        print(f"Line {idx}: {l}")
