import pypdfium2 as pdfium

def find_label_coords(pdf_path, labels):
    doc = pdfium.PdfDocument(pdf_path)
    page = doc[0]
    tp = page.get_textpage()
    text = tp.get_text_range()
    
    results = {}
    for lbl in labels:
        pos = text.find(lbl)
        if pos != -1:
            # average charbox of the label
            xs, ys = [], []
            for i in range(pos, pos + len(lbl)):
                box = tp.get_charbox(i) # left, bottom, right, top
                xs.extend([box[0], box[2]])
                ys.extend([box[1], box[3]])
            results[lbl] = (sum(xs)/len(xs), sum(ys)/len(ys))
    return results

print("=== CARTA 5 (Maylasky) ===")
res5 = find_label_coords("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_05_zoneamento_consolidacao_urbana_maylasky.pdf", 
    ["MAYLASKY", "SUN VALLEY", "LAS BRISAS", "RECANTO", "CAMARGO", "VERA CRUZ"])
for k, v in res5.items():
    print(f"  {k}: pt=({v[0]:.2f}, {v[1]:.2f})")

print("\n=== CARTA 6 (São João Novo) ===")
res6 = find_label_coords("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_06_zoneamento_consolidacao_urbana_sao_joao_novo.pdf",
    ["SÃO JOÃO NOVO", "BOQUEIRÃO", "MONT SERRAT", "SÃO JULIÃO", "ALPINAS"])
for k, v in res6.items():
    print(f"  {k}: pt=({v[0]:.2f}, {v[1]:.2f})")

print("\n=== CARTA 7 (Canguera) ===")
res7 = find_label_coords("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_07_zoneamento_consolidacao_urbana_canguera.pdf",
    ["CAMPININHA", "SUÍÇA", "PAVÃO", "NOVA CANGUERA", "BELMIRO"])
for k, v in res7.items():
    print(f"  {k}: pt=({v[0]:.2f}, {v[1]:.2f})")
