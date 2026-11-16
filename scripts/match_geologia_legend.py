import pypdfium2 as pdfium
doc = pdfium.PdfDocument(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf')
page = doc[0]
tp = page.get_textpage()
# Print all text in the legend box ordered by Y descending
n = tp.count_rects(1100, 1050, 1650, 1580)
print('Legend box text:')
t = tp.get_text_bounded(1100, 1050, 1650, 1580)
for line in t.splitlines():
    if line.strip():
        print(line.strip())
