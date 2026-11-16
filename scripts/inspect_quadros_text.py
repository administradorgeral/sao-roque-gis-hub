import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\04_minuta_lc40_zoneamento_uso_ocupacao.pdf"
doc = pdfium.PdfDocument(pdf_path)

pages_to_check = [34, 35, 36, 37, 45, 47, 48, 50]

for p_num in pages_to_check:
    page = doc[p_num - 1]
    tp = page.get_textpage()
    text = tp.get_text_range(0, tp.count_chars())
    print(f"\n==========================================")
    print(f"PÁGINA {p_num} de 04_minuta_lc40_zoneamento_uso_ocupacao.pdf")
    print(f"==========================================")
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    print("\n".join(lines[:35]))
