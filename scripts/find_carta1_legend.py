import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
tp = page.get_textpage()
text = tp.get_text_range(0, tp.count_chars())
lines = [l.strip() for l in text.split("\n") if l.strip()]

print(f"Total lines: {len(lines)}")
# Find "LEGENDA" or macrozonas
for i, l in enumerate(lines):
    if any(k in l.upper() for k in ["LEGENDA", "MACROZONA", "CONSOLIDAÇÃO", "URBANIZAÇÃO", "RURAL", "PROTEÇÃO", "MANANCIAL"]):
        print(f"Line {i:3d}: {l}")
