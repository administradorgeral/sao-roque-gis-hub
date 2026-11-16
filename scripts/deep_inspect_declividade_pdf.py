import pypdfium2 as pdfium
import json
import re

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
width, height = page.get_size()

print(f"Dimensões da página: {width} x {height} pt ({width*25.4/72:.1f} x {height*25.4/72:.1f} mm)")

textpage = page.get_textpage()
text = textpage.get_text_range()
print(f"Total de caracteres de texto: {len(text)}")

# Buscar todos os textos com suas caixas delimitadoras (bounding boxes)
num_chars = textpage.count_chars()
print(f"Total de caracteres individuais: {num_chars}")

# Vamos agrupar textos por proximidade vertical e horizontal
lines = []
current_line = []
for i in range(num_chars):
    char = textpage.get_text_range(i, 1)
    rect = textpage.get_charbox(i) # left, bottom, right, top
    if char == '\r' or char == '\n':
        if current_line:
            txt = "".join([c[0] for c in current_line])
            bbox = (
                min(c[1][0] for c in current_line),
                min(c[1][1] for c in current_line),
                max(c[1][2] for c in current_line),
                max(c[1][3] for c in current_line)
            )
            lines.append((txt, bbox))
            current_line = []
    else:
        current_line.append((char, rect))

if current_line:
    txt = "".join([c[0] for c in current_line])
    bbox = (
        min(c[1][0] for c in current_line),
        min(c[1][1] for c in current_line),
        max(c[1][2] for c in current_line),
        max(c[1][3] for c in current_line)
    )
    lines.append((txt, bbox))

print(f"Total de blocos/linhas de texto reconstruídos: {len(lines)}")

# Filtrar textos que parecem coordenadas UTM (e.g. 272000, 7385000, 276.000, etc.)
utm_coords = []
for txt, bbox in lines:
    clean = txt.strip()
    # Verifica se tem números com 6 ou 7 dígitos ou formato 272.000 / 7.390.000
    m_utm_x = re.match(r"^(\d{2,3}[\.\s]?\d{3})\s*(m\.?E|E)?$", clean)
    m_utm_y = re.match(r"^(\d{1,2}[\.\s]?\d{3}[\.\s]?\d{3})\s*(m\.?N|N)?$", clean)
    digits_only = re.sub(r"\D", "", clean)
    if len(digits_only) in [6, 7] and (digits_only.startswith('2') or digits_only.startswith('7')):
        utm_coords.append((clean, digits_only, bbox))

print("\n--- COORDENADAS UTM DETECTADAS NO TEXTO DO PDF ---")
for c, d, b in utm_coords:
    print(f"Texto: '{c}' (Dígitos: {d}) @ BBox (x0={b[0]:.1f}, y0={b[1]:.1f}, x1={b[2]:.1f}, y1={b[3]:.1f})")

# Textos de Legenda e Metadados
print("\n--- TEXTOS CHAVE IDENTIFICADOS ---")
for txt, bbox in lines:
    t = txt.strip()
    if any(k in t.lower() for k in ['decliv', 'escala', 'sirgas', 'datum', 'fonte', 'elabora', 'respons', 'crea', 'sistema', 'proje']):
        print(f"'{t}' @ {bbox[0]:.1f}, {bbox[1]:.1f}")

doc.close()
