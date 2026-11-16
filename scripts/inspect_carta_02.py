import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_02_zoneamentos_macrozona_urbanizacao_especifica.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
tp = page.get_textpage()
n_chars = tp.count_chars()

words = []
cur_word = ""
cur_box = None
for c_i in range(n_chars):
    box = tp.get_charbox(c_i)
    char = tp.get_text_range(c_i, 1)
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

print(f"Total de palavras extraídas: {len(words)}")
for w, box in words:
    if any(k in w.upper() for k in ["LEGENDA", "MACROZONA", "ESPECÍFICA", "RURAL", "CONSOLIDAÇÃO", "MANANCIAL", "TURÍST", "MOMBAÇA", "DESENVOLVIMENTO", "ESTRATÉGICA", "OCUPAÇÃO", "CHÁCARA", "CONVENÇÕES", "ZONEAMENTO"]):
        print(f"Word '{w}' at x=[{box[0]:.1f}, {box[2]:.1f}], y=[{box[1]:.1f}, {box[3]:.1f}]")
