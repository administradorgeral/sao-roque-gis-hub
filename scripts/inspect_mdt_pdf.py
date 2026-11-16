import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import os
import re
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"

print(f"=== INSPECIONANDO PDF DO MDT ===")
print(f"Arquivo: {pdf_path}")
print(f"Tamanho: {os.path.getsize(pdf_path) / (1024*1024):.2f} MB")

doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
w, h = page.get_size()
print(f"Dimensões: {w:.2f} x {h:.2f} pt ({w*25.4/72:.1f} x {h*25.4/72:.1f} mm) - Formato A1")

# 1. Metadados do documento
meta_keys = ['Title', 'Author', 'Subject', 'Keywords', 'Creator', 'Producer', 'CreationDate', 'ModDate']
print("\n--- METADADOS DO DOCUMENTO ---")
for k in meta_keys:
    try:
        val = doc.get_metadata_value(k)
        if val:
            print(f"  {k}: {val}")
    except Exception:
        pass

# 2. Contagem e tipos de objetos
objs = list(page.get_objects())
print(f"\nTotal de objetos na página: {len(objs)}")
type_counts = Counter(obj.type for obj in objs)
type_names = {1: 'TEXT', 2: 'PATH', 3: 'IMAGE', 4: 'SHADING', 5: 'FORM'}
for t, c in type_counts.items():
    print(f"  Tipo {t} ({type_names.get(t, 'UNKNOWN')}): {c} objetos")

# 3. Extrair textos e caixas
textpage = page.get_textpage()
num_chars = textpage.count_chars()
chars = []
for i in range(num_chars):
    ch = textpage.get_text_range(i, 1)
    if ch in '\r\n\t':
        continue
    box = textpage.get_charbox(i)
    chars.append({
        'char': ch,
        'left': box[0], 'bottom': box[1], 'right': box[2], 'top': box[3],
        'cx': (box[0] + box[2]) / 2, 'cy': (box[1] + box[3]) / 2
    })

# Linhas de texto na barra lateral (x > 1700)
sidebar_chars = [c for c in chars if c['left'] >= 1700]
sidebar_chars.sort(key=lambda c: (-c['cy'], c['cx']))

lines = []
current_line = []
for c in sidebar_chars:
    if not current_line:
        current_line.append(c)
    else:
        if abs(c['cy'] - current_line[-1]['cy']) < 4.0:
            current_line.append(c)
        else:
            current_line.sort(key=lambda x: x['cx'])
            lines.append("".join([x['char'] for x in current_line]))
            current_line = [c]
if current_line:
    current_line.sort(key=lambda x: x['cx'])
    lines.append("".join([x['char'] for x in current_line]))

print("\n--- TEXTOS DA BARRA LATERAL (LEGENDA E METADADOS TÉCNICOS) ---")
for l in lines:
    if len(l.strip()) > 1:
        print(f"  {l.strip()}")

# 4. Encontrar coordenadas UTM do grid
print("\n--- COORDENADAS UTM DETECTADAS ---")
for target in ['272000', '276000', '280000', '284000', '288000', '292000', '296000']:
    for i in range(len(chars) - len(target) + 1):
        candidate = "".join([chars[i+j]['char'] for j in range(len(target))])
        if candidate == target:
            c_boxes = [chars[i+j] for j in range(len(target))]
            x0 = min(c['left'] for c in c_boxes)
            y0 = min(c['bottom'] for c in c_boxes)
            print(f"  UTM X '{target}' @ x={x0:.1f}, y={y0:.1f}")
            break

# 5. Cores dos caminhos vetoriais
path_objs = [obj for obj in objs if obj.type == 2]
fill_colors = Counter()
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

for i in range(0, len(path_objs), 5):
    p = path_objs[i]
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a)):
        fill_colors[(r.value, g.value, b.value, a.value)] += 1

print("\n--- CORES DE PREENCHIMENTO (FILL) NOS CAMINHOS VETORIAIS ---")
for col, cnt in fill_colors.most_common(15):
    hex_col = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X}"
    print(f"  {hex_col} (RGB {col[0]}, {col[1]}, {col[2]}): {cnt * 5} ocorrências estimadas")

doc.close()
