import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
tp = page.get_textpage()

chars = []
for i in range(tp.count_chars()):
    b = tp.get_charbox(i)
    if 1050 <= b[0] <= 1700 and 1250 <= b[1] <= 1650:
        chars.append((b, tp.get_text_range(i, 1)))

lines = {}
for (l, b, r, t), ch in chars:
    y_bucket = round(b / 8) * 8
    lines.setdefault(y_bucket, []).append((l, ch))

for y in sorted(lines.keys(), reverse=True):
    line_chars = sorted(lines[y], key=lambda x: x[0])
    text = "".join(c for _, c in line_chars).strip()
    if text:
        print(f"Y={y}: {text}")
