import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
doc = pdfium.PdfDocument(pdf_path)

for p_idx in range(74, 87):
    p = doc[p_idx]
    tp = p.get_textpage()
    text = tp.get_text_range(0, 3000)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    # Find relevant lines near title
    assunto = ""
    for i, l in enumerate(lines):
        if "REVISÃO DO PLANO DIRETOR" in l:
            assunto = " | ".join(lines[max(0, i-4):min(len(lines), i+6)])
            break
        elif "MACROZONEAMENTO" in l or "ZONEAMENTO" in l or "CORREDORES" in l or "INTERESSE" in l:
            assunto = " | ".join(lines[max(0, i-2):min(len(lines), i+4)])
            break
    print(f"Pág. {p_idx+1:2d} ({p.get_size()}): {assunto[:130]}")
