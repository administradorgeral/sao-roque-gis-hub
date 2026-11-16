import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]
tp = page.get_textpage()

n_chars = tp.count_chars()
chars_pos = []
for c_i in range(n_chars):
    box = tp.get_charbox(c_i)
    char = tp.get_text_range(c_i, 1)
    chars_pos.append((char, box))

words = []
cur_word = ""
cur_box = None
for char, box in chars_pos:
    if char in ["\n", "\r", " "]:
        if cur_word:
            words.append((cur_word, cur_box))
            cur_word = ""
            cur_box = None
    else:
        cur_word += char
        if cur_box is None:
            cur_box = list(box)
        else:
            cur_box[0] = min(cur_box[0], box[0])
            cur_box[1] = min(cur_box[1], box[1])
            cur_box[2] = max(cur_box[2], box[2])
            cur_box[3] = max(cur_box[3], box[3])
if cur_word:
    words.append((cur_word, cur_box))

# Let's inspect words in the bottom right corner (x >= 1800, y <= 500)
tb_words = [w for w in words if w[1][0] >= 1700 and w[1][1] <= 550]
# Group into lines by similar y (within 4 pt)
tb_words.sort(key=lambda w: -w[1][1])

lines = []
curr_line = []
curr_y = None
for w in tb_words:
    wy = (w[1][1] + w[1][3]) / 2
    if curr_y is None or abs(curr_y - wy) < 5:
        curr_line.append(w)
        curr_y = wy
    else:
        curr_line.sort(key=lambda x: x[1][0])
        lines.append(" ".join(x[0] for x in curr_line))
        curr_line = [w]
        curr_y = wy
if curr_line:
    curr_line.sort(key=lambda x: x[1][0])
    lines.append(" ".join(x[0] for x in curr_line))

print("Linhas do Carimbo / Legenda (Canto Inferior Direito):")
for l in lines:
    print("  ", l)
