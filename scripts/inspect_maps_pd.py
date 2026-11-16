import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
doc = pdfium.PdfDocument(pdf_path)

print("--- 13 Cartas e Mapas (Páginas 75 a 87) ---")
for p_idx in range(74, 87):
    p = doc[p_idx]
    tp = p.get_textpage()
    text = tp.get_text_range(0, 1500)
    
    # Extract Title / Assunto / Carta / Folha
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    title_line = ""
    for idx, l in enumerate(lines):
        if "TÍTULO" in l or "ASSUNTO" in l or "CARTA" in l:
            title_line += " | " + " ".join(lines[idx:idx+4])
    print(f"Pág. {p_idx + 1}: {title_line[:120] if title_line else lines[:5]}")
