import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf')
page = doc[0]
tp = page.get_textpage()

# Let's extract all characters with boxes between X: 1100-1650 and Y: 1050-1580
chars = []
for i in range(tp.count_chars()):
    box = tp.get_charbox(i) # (left, bottom, right, top)
    if 1100 <= box[0] <= 1650 and 1050 <= box[1] <= 1580:
        ch = tp.get_text_range(i, 1)
        chars.append((box, ch))

# Group characters into lines by Y
lines = {}
for (l, b, r, t), ch in chars:
    y_bucket = round(b / 8) * 8
    lines.setdefault(y_bucket, []).append((l, ch))

for y in sorted(lines.keys(), reverse=True):
    line_chars = sorted(lines[y], key=lambda x: x[0])
    text = "".join(c for _, c in line_chars).strip()
    if text:
        print(f"Y={y}: {text}")
