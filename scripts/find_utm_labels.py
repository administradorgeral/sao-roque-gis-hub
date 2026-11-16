import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\75631_4_3_5_1 Geologia.pdf')
page = doc[0]
tp = page.get_textpage()

# Let's search all texts with 6 or 7 digits (UTM coordinates like 276000, 7385000, etc.)
chars = []
for i in range(tp.count_chars()):
    b = tp.get_charbox(i)
    chars.append((b, tp.get_text_range(i, 1)))

# Let's search for numbers
full_text = "".join(c for _, c in chars)
print("Page characters total:", len(full_text))

# Let's inspect text near neatline borders:
# X neatline is around 31.441 to 1674.044, Y neatline around 35.970 to 1620.634
for i in range(tp.count_chars()):
    b = tp.get_charbox(i)
    # check if char starts a word
    if i + 6 < tp.count_chars():
        word = "".join(tp.get_text_range(j, 1) for j in range(i, i+7)).strip()
        if word.isdigit() and len(word) in (6, 7):
            print(f"UTM Label: {word} at ({b[0]:.1f}, {b[1]:.1f})")
