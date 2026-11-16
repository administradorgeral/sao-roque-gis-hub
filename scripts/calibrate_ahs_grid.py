import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34229_4.2.5.1-1 AHS.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

print(f"Total objects in AHS PDF: {len(objs)}")

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

grid_lines_x = []
grid_lines_y = []
fill_colors = Counter()
stroke_colors = Counter()

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        w = right.value - left.value
        h = top.value - bottom.value

        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            fill_colors[f_hex] += 1

        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            s_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            stroke_colors[s_hex] += 1
            if s_hex in ["#6E6E6E", "#000000", "#7F7F7F", "#808080"]:
                if w < 2.0 and h > 500:
                    grid_lines_x.append((idx, s_hex, left.value, bottom.value, top.value, h))
                elif h < 2.0 and w > 500:
                    grid_lines_y.append((idx, s_hex, bottom.value, left.value, right.value, w))

print(f"\n--- GRID LINES ENCONTRADAS ---")
print(f"Vertical grid lines found: {len(grid_lines_x)}")
for g in sorted(grid_lines_x, key=lambda x: x[2]):
    print(f"  X={g[2]:.2f} (idx={g[0]}, color={g[1]}, Y: {g[3]:.1f} to {g[4]:.1f}, h={g[5]:.1f})")

print(f"Horizontal grid lines found: {len(grid_lines_y)}")
for g in sorted(grid_lines_y, key=lambda x: x[2]):
    print(f"  Y={g[2]:.2f} (idx={g[0]}, color={g[1]}, X: {g[3]:.1f} to {g[4]:.1f}, w={g[5]:.1f})")

print(f"\n--- CORES DE PREENCHIMENTO (FILL) ---")
for c, cnt in fill_colors.most_common(20):
    print(f"  {c}: {cnt}")

print(f"\n--- CORES DE CONTORNO (STROKE) ---")
for c, cnt in stroke_colors.most_common(20):
    print(f"  {c}: {cnt}")

# Textos com coordenadas UTM e legendas
text_page = page.get_textpage()
full_text = text_page.get_text_range()
print(f"\n--- TEXTOS COMPLETOS ---")
for line in full_text.split("\r\n"):
    line_clean = line.strip()
    if line_clean:
        print("  ", line_clean)

