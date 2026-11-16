import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/1835_4_3_6_1 Pedológico.pdf')
tp = doc[0].get_textpage()

# Search text near Y < 50 or Y > 1600 (top and bottom border)
print("=== LABELS NEAR TOP/BOTTOM (X Coordinates) ===")
for i in range(tp.count_chars()):
    b = tp.get_charbox(i)
    if b[1] < 50 or b[1] > 1600:
        ch = tp.get_text_range(i, 6) # read small token
        # check if it looks like a number
        if any(c.isdigit() for c in ch):
            pass

# Let's collect all text tokens with their positions
tokens = []
i = 0
n = tp.count_chars()
while i < n:
    b = tp.get_charbox(i)
    ch = tp.get_text_range(i, 1)
    if ch.isdigit():
        # read full number
        start_x = b[0]
        start_y = b[1]
        num_str = ch
        j = i + 1
        while j < n:
            b2 = tp.get_charbox(j)
            ch2 = tp.get_text_range(j, 1)
            if ch2.isdigit() or ch2 in '., ':
                num_str += ch2
                j += 1
            else:
                break
        tokens.append((round(start_x, 1), round(start_y, 1), num_str.strip()))
        i = j
    else:
        i += 1

print(f"Found {len(tokens)} numeric tokens:")
for t in tokens:
    if len(t[2]) >= 4 and any(c.isdigit() for c in t[2]):
        print(f"  ({t[0]}, {t[1]}): '{t[2]}'")
