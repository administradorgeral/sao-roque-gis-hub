import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
tp = doc[0].get_textpage()

tokens = []
i = 0
n = tp.count_chars()
while i < n:
    b = tp.get_charbox(i)
    ch = tp.get_text_range(i, 1)
    if ch.isdigit():
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

print("Numeric border tokens:")
for t in tokens:
    if len(t[2]) >= 5 and (t[1] < 50 or t[1] > 1600 or t[0] < 100 or t[0] > 1650):
        print(f"  ({t[0]}, {t[1]}): '{t[2]}'")
