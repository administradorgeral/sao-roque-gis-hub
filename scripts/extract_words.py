import pypdfium2 as pdfium
import re

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()

num_chars = textpage.count_chars()
chars_info = []
for i in range(num_chars):
    ch = textpage.get_text_range(i, 1)
    box = textpage.get_charbox(i)
    chars_info.append((ch, box))

# Vamos procurar sequências de dígitos
full_str = "".join([c[0] for c in chars_info])
print("Amostra do texto completo:")
print(full_str[:500])

# Vamos buscar blocos na parte inferior (y < 200) e superior (y > 1550)
bottom_texts = []
top_texts = []
sidebar_texts = []

# Agrupando palavras por proximidade
words = []
cur_word = ""
cur_box = None

for ch, box in chars_info:
    if ch in ' \t\r\n':
        if cur_word:
            words.append((cur_word, cur_box))
            cur_word = ""
            cur_box = None
    else:
        if not cur_word:
            cur_word = ch
            cur_box = list(box)
        else:
            cur_word += ch
            cur_box[0] = min(cur_box[0], box[0])
            cur_box[1] = min(cur_box[1], box[1])
            cur_box[2] = max(cur_box[2], box[2])
            cur_box[3] = max(cur_box[3], box[3])

if cur_word:
    words.append((cur_word, cur_box))

print(f"\nTotal de palavras identificadas: {len(words)}")

print("\n--- PALAVRAS COM NÚMEROS DE 6 DÍGITOS OU '27'/'28'/'29' ---")
for w, b in words:
    if any(k in w for k in ['272', '276', '280', '284', '288', '292', '296', '1:']):
        print(f"'{w}' @ {b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}")

print("\n--- TEXTOS DA LEGENDA E NOTAS TÉCNICAS (x > 1700) ---")
for w, b in words:
    if b[0] > 1700 and any(k in w.lower() for k in ['decliv', 'escala', 'fonte', 'sirgas', 'ondulado', 'plano', 'montanhoso', 'igc', 'curva', 'morf']):
        print(f"'{w}' @ {b[0]:.1f}, {b[1]:.1f}")

doc.close()
