import pypdfium2 as pdfium

doc3 = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_03_zoneamentos_macrozona_consolidacao_urbana.pdf")
page3 = doc3[0]
tp3 = page3.get_textpage()
text3 = tp3.get_text_range()

targets = ["CAMPININHA", "PAVÃO", "SUN VALLEY", "LAS BRISAS", "BOQUEIRÃO", "MONT SERRAT", "VERA CRUZ", "CAMARGO", "SÃO JULIÃO"]

print("=== SEARCHING TARGETS IN CARTA 3 ===")
for t in targets:
    pos = text3.find(t)
    if pos != -1:
        xs, ys = [], []
        for i in range(pos, pos + len(t)):
            box = tp3.get_charbox(i)
            xs.extend([box[0], box[2]])
            ys.extend([box[1], box[3]])
        cx, cy = sum(xs)/len(xs), sum(ys)/len(ys)
        print(f"  {t} in Carta 3: pt=({cx:.2f}, {cy:.2f})")
    else:
        print(f"  {t} NOT found in Carta 3")
