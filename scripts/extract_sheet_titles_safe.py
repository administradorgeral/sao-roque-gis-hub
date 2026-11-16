import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
doc = pdfium.PdfDocument(pdf_path)

for p_idx in range(74, 87):
    p = doc[p_idx]
    tp = p.get_textpage()
    n_chars = tp.count_chars()
    text = tp.get_text_range(0, n_chars) if n_chars > 0 else ""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    # Scan for sheet titles, carta, folha
    found = []
    for l in lines:
        for kw in ["MACROZONEAMENTO", "ZONEAMENTO", "CORREDOR", "ESPECIAL INTERESSE", "SISTEMA VIÁRIO", "PERÍMETRO", "CARTA", "FOLHA"]:
            if kw in l.upper() and len(l) < 80:
                found.append(l)
                break
    print(f"Pág. {p_idx+1:2d} (chars={n_chars}): {found[:4]}")
