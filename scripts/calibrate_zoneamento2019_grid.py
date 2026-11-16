import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

print(f"Total objects: {len(objs)}")

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

grid_lines_x = []
grid_lines_y = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            s_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            w = right.value - left.value
            h = top.value - bottom.value
            if s_hex in ["#6E6E6E", "#000000", "#7F7F7F", "#808080"]:
                if w < 2.0 and h > 500:
                    grid_lines_x.append((idx, s_hex, left.value, bottom.value, top.value, h))
                elif h < 2.0 and w > 500:
                    grid_lines_y.append((idx, s_hex, bottom.value, left.value, right.value, w))

print(f"Vertical grid lines found: {len(grid_lines_x)}")
for g in sorted(grid_lines_x, key=lambda x: x[2]):
    print(f"  X={g[2]:.2f} (idx={g[0]}, color={g[1]}, Y: {g[3]:.1f} to {g[4]:.1f})")

print(f"Horizontal grid lines found: {len(grid_lines_y)}")
for g in sorted(grid_lines_y, key=lambda x: x[2]):
    print(f"  Y={g[2]:.2f} (idx={g[0]}, color={g[1]}, X: {g[3]:.1f} to {g[4]:.1f})")
