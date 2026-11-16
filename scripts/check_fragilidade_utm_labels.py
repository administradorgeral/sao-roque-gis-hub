import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
tp = page.get_textpage()

# Let's find UTM labels near border:
x_lines = [103.443, 386.890, 670.337, 953.785, 1237.232, 1520.680]
y_lines = [241.163, 524.593, 808.023, 1091.452, 1375.122]

for xl in x_lines:
    txt_top = tp.get_text_bounded(xl - 50, 1610, xl + 50, 1660).strip()
    txt_bot = tp.get_text_bounded(xl - 50, 20, xl + 50, 50).strip()
    print(f"X = {xl:.3f} -> Top: '{txt_top}' | Bot: '{txt_bot}'")

for yl in y_lines:
    txt_left = tp.get_text_bounded(10, yl - 30, 40, yl + 30).strip()
    txt_right = tp.get_text_bounded(1660, yl - 30, 1720, yl + 30).strip()
    print(f"Y = {yl:.3f} -> Left: '{txt_left}' | Right: '{txt_right}'")
