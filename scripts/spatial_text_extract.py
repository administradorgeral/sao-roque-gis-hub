import pypdfium2 as pdfium

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()
num_chars = textpage.count_chars()

chars = []
for i in range(num_chars):
    ch = textpage.get_text_range(i, 1)
    if ch in '\r\n\t':
        continue
    box = textpage.get_charbox(i)
    # box: (left, bottom, right, top)
    chars.append({
        'char': ch,
        'left': box[0],
        'bottom': box[1],
        'right': box[2],
        'top': box[3],
        'cx': (box[0] + box[2]) / 2,
        'cy': (box[1] + box[3]) / 2,
    })

print(f"Total de caracteres válidos: {len(chars)}")

# Vamos agrupar horizontalmente ou verticalmente por proximidade espacial (threshold de distância)
# Primeiro vamos procurar onde estão os dígitos 272000, 276000, etc.
for target in ['272000', '276000', '280000', '284000', '288000', '292000', '296000']:
    # Encontrar sequências dos dígitos
    for i in range(len(chars) - len(target) + 1):
        candidate = "".join([chars[i+j]['char'] for j in range(len(target))])
        if candidate == target:
            c_boxes = [chars[i+j] for j in range(len(target))]
            x0 = min(c['left'] for c in c_boxes)
            y0 = min(c['bottom'] for c in c_boxes)
            x1 = max(c['right'] for c in c_boxes)
            y1 = max(c['top'] for c in c_boxes)
            print(f"Encontrado UTM X '{target}' @ x=[{x0:.1f}, {x1:.1f}], y=[{y0:.1f}, {y1:.1f}]")

# Vamos encontrar todas as palavras na barra lateral direita (x > 1700)
# Agrupando por linhas com cy similar (diferença < 4 pt)
sidebar_chars = [c for c in chars if c['left'] >= 1700]
# Ordenar por cy decrescente (do topo para baixo), depois cx crescente
sidebar_chars.sort(key=lambda c: (-c['cy'], c['cx']))

lines = []
current_line = []
for c in sidebar_chars:
    if not current_line:
        current_line.append(c)
    else:
        # Verifica se está na mesma linha
        if abs(c['cy'] - current_line[-1]['cy']) < 4.0:
            current_line.append(c)
        else:
            current_line.sort(key=lambda x: x['cx'])
            lines.append("".join([x['char'] for x in current_line]))
            current_line = [c]

if current_line:
    current_line.sort(key=lambda x: x['cx'])
    lines.append("".join([x['char'] for x in current_line]))

print("\n--- TEXTOS COMPLETOS DA BARRA LATERAL (LEGENDA, METADADOS, AUTORES) ---")
for l in lines:
    if len(l.strip()) > 1:
        print(l.strip())

doc.close()
