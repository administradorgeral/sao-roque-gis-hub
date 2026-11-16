import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf")
t = doc[0].get_textpage()
txt = t.get_text_range()

for search in ['Tratamento', 'Capta', 'bombeamento', 'Potável', 'Reservatório']:
    idx = 0
    while True:
        pos = txt.find(search, idx)
        if pos == -1: break
        start = max(0, pos - 20)
        end = min(len(txt), pos + 40)
        print(f"Match '{search}' at {pos}: '{txt[start:end].replace(chr(10), ' ')}'")
        idx = pos + len(search)

doc.close()
