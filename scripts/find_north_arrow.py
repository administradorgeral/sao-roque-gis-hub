import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]
tp = page.get_textpage()

# Search for "NORTE" or "N"
for search_term in ["NORTE", "N", "NM", "NG"]:
    s = tp.search(search_term)
    matches = []
    while True:
        m = s.get_next()
        if not m:
            break
        c_idx, c_cnt = m
        rects = [tp.get_charbox(c_idx + i) for i in range(c_cnt)]
        min_x = min(r[0] for r in rects)
        max_x = max(r[2] for r in rects)
        min_y = min(r[1] for r in rects)
        max_y = max(r[3] for r in rects)
        matches.append((min_x, min_y, max_x, max_y))
    print(f"Term '{search_term}': {len(matches)} ocorrências. {matches[:3]}")
