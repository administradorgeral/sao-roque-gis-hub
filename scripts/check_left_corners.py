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

# Look at top-left: x < 700, y > 1100
tl_words = [w for w in words if w[1][0] < 700 and w[1][1] > 1100]
tl_words.sort(key=lambda w: (-w[1][1], w[1][0]))
print("Palavras no Canto Superior Esquerdo (Top-Left):")
print(" ".join(w[0] for w in tl_words[:80]))

# Look at bottom-left: x < 700, y < 600
bl_words = [w for w in words if w[1][0] < 700 and w[1][1] < 600]
bl_words.sort(key=lambda w: (-w[1][1], w[1][0]))
print("\nPalavras no Canto Inferior Esquerdo (Bottom-Left):")
print(" ".join(w[0] for w in bl_words[:80]))
