import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

# Encontrar o maior path preto ou sem preenchimento na metade esquerda (o neatline)
pw = page.get_width()
ph = page.get_height()
print(f"Página: {pw:.2f} x {ph:.2f}")

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

candidates = []
for p in path_objs:
    b_box = p.get_bounds() # left, bottom, right, top
    w = b_box[2] - b_box[0]
    h = b_box[3] - b_box[1]
    # Se ocupa quase toda a altura e largura da área do mapa
    if w > 1500 and h > 1500:
        pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
        candidates.append((b_box, (r.value, g.value, b.value), w, h))

print(f"Grandes retângulos/molduras encontrados: {len(candidates)}")
for c in candidates:
    print(f"  Bounds: {c[0]}, Stroke: {c[1]}, W={c[2]:.2f}, H={c[3]:.2f}")

# Vamos comparar com a neatline do Mapa 1 e 2:
# neatline_x0_pt = 31.4408
# neatline_y0_pt = 35.9703
# neatline_x1_pt = 1673.0836
# neatline_y1_pt = 1619.6735
print("\nComparação com Neatline padrão de São Roque (1641.64 x 1583.70 pt):")
for b, col, w, h in candidates:
    dx0 = abs(b[0] - 31.4408)
    dy0 = abs(b[1] - 35.9703)
    dx1 = abs(b[2] - 1673.0836)
    dy1 = abs(b[3] - 1619.6735)
    print(f"  Delta com Neatline padrão: dx0={dx0:.4f}, dy0={dy0:.4f}, dx1={dx1:.4f}, dy1={dy1:.4f}")

doc.close()
