import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\Plano Diretor - Combined.pdf"
doc = pdfium.PdfDocument(pdf_path)

sections = [
    ("Seção 1: Diagnóstico / Relatório Técnico?", 1, 74),
    ("Seção 2: Cartas Temáticas e Mapas de Zoneamento (CAD / GIS)", 75, 87),
    ("Seção 3: Minuta Texto Corrido LC 39/06 (Plano Diretor Estratégico)", 88, 152),
    ("Seção 4: Minuta Texto Corrido LC 40/06 (Zoneamento, Uso e Ocupação)", 153, 214),
    ("Seção 5: Projeto de Lei Formatado Revisão LC 40/06", 215, 270),
    ("Seção 6: Projeto de Lei Formatado Revisão LC 39/06", 271, 318)
]

for name, p_start, p_end in sections:
    print(f"\n==========================================")
    print(f"{name} (Páginas {p_start} a {p_end})")
    print(f"==========================================")
    p = doc[p_start - 1]
    tp = p.get_textpage()
    text = tp.get_text_range(0, 800)
    print(f"Primeiros caracteres da página {p_start}:")
    print(text.strip()[:400])
    
    # Check if page has images or paths (like maps)
    p_obj_types = {}
    for obj in p.get_objects():
        p_obj_types[obj.type] = p_obj_types.get(obj.type, 0) + 1
    print(f"Objetos na página {p_start}: {p_obj_types}")
