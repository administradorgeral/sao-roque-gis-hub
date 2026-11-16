import pypdfium2 as pdfium

for num, name, code in [(5, 'Maylasky', 'maylasky'), (6, 'Sao Joao Novo', 'sao_joao_novo'), (7, 'Canguera', 'canguera')]:
    pdf_path = f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_0{num}_zoneamento_consolidacao_urbana_{code}.pdf"
    doc = pdfium.PdfDocument(pdf_path)
    page = doc[0]
    tp = page.get_textpage()
    text = tp.get_text_range()
    print(f"=== TODOS OS TEXTOS DA CARTA {num} ({name}) ===")
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for l in lines:
        print("  ", l)
