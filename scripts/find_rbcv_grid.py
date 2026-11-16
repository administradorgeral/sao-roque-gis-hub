import pypdfium2 as pdfium

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]
tp = page.get_textpage()

terms = ['47°0', '46°0', '23°0', '24°0', '25°0']
for t in terms:
    s = tp.search(t)
    while True:
        m = s.get_next()
        if not m:
            break
        char_idx, char_count = m
        n_rects = tp.count_rects(char_idx, char_count)
        rects = [tp.get_rect(i) for i in range(n_rects)]
        print(f"Term '{t}' at char {char_idx}: {rects}")
