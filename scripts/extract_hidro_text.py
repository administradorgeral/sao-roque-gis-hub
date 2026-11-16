import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

textpage = page.get_textpage()
n_chars = textpage.count_chars()

print(f"Total de caracteres: {n_chars}")

# Extrair blocos de texto ou palavras com posições
# Vamos agrupar caracteres próximos em palavras/linhas
words = []
curr_word = ""
curr_box = None

for i in range(n_chars):
    char = textpage.get_text_range(i, 1)
    box = textpage.get_charbox(i) # left, bottom, right, top
    if char in (' ', '\n', '\r', '\t'):
        if curr_word:
            words.append((curr_word, curr_box))
            curr_word = ""
            curr_box = None
    else:
        if not curr_word:
            curr_box = list(box)
        else:
            curr_box[0] = min(curr_box[0], box[0])
            curr_box[1] = min(curr_box[1], box[1])
            curr_box[2] = max(curr_box[2], box[2])
            curr_box[3] = max(curr_box[3], box[3])
        curr_word += char

if curr_word:
    words.append((curr_word, curr_box))

print(f"Total de palavras extraídas: {len(words)}")

# Filtrar palavras na barra lateral (X > 1700) para ver o carimbo e a legenda
sidebar_words = [w for w in words if w[1] and w[1][0] > 1700]
# Ordenar por Y decrescente (topo para base)
sidebar_words.sort(key=lambda x: -x[1][3])

print("\n--- TEXTO DA BARRA LATERAL (LEGENDA E CARIMBO TÉCNICO) ---")
curr_y = None
line_buf = []
for w, box in sidebar_words:
    if curr_y is None or abs(box[3] - curr_y) > 4:
        if line_buf:
            print(" ".join(line_buf))
            line_buf = []
        curr_y = box[3]
    line_buf.append(w)
if line_buf:
    print(" ".join(line_buf))

# Filtrar nomes no mapa (X < 1700) para ver os cursos d'água identificados
map_words = [w for w in words if w[1] and w[1][0] <= 1700]
print(f"\nTotal de palavras no interior do mapa: {len(map_words)}")

# Exibir algumas palavras no mapa
print("\n--- AMOSTRA DE NOMES DE RIOS/CÓRREGOS/LUGARES NO MAPA ---")
map_words.sort(key=lambda x: -x[1][3])
sample_lines = []
curr_y = None
line_buf = []
for w, box in map_words:
    if curr_y is None or abs(box[3] - curr_y) > 3:
        if line_buf:
            l_str = " ".join(line_buf)
            if any(term in l_str.lower() for term in ["rio", "córrego", "corrego", "ribeirão", "ribeirao", "lago", "represa", "bacia"]):
                sample_lines.append(l_str)
            line_buf = []
        curr_y = box[3]
    line_buf.append(w)

for l in sample_lines[:25]:
    print(f"  {l}")

doc.close()
