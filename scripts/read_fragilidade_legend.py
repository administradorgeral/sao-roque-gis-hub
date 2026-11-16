import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
tp = page.get_textpage()

# Let's search text between X: 1100 to 2400 and Y: 800 to 1650 (sidebar and legend area)
chars = []
for i in range(tp.count_chars()):
    box = tp.get_charbox(i)
    if box[0] >= 1100:
        chars.append((box, tp.get_text_range(i, 1)))

lines = {}
for (l, b, r, t), ch in chars:
    y_bucket = round(b / 8) * 8
    lines.setdefault(y_bucket, []).append((l, ch))

for y in sorted(lines.keys(), reverse=True):
    line_chars = sorted(lines[y], key=lambda x: x[0])
    text = "".join(c for _, c in line_chars).strip()
    if text:
        print(f"Y={y}: {text}")
