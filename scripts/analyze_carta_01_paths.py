import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

fill_colors = {}
stroke_colors = {}
large_polygons = []

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        w = right.value - left.value
        h = top.value - bottom.value
        
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            fill_colors[c] = fill_colors.get(c, 0) + 1
            if w > 100 or h > 100:
                large_polygons.append((idx, c, left.value, bottom.value, right.value, top.value, w, h))

        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            stroke_colors[c] = stroke_colors.get(c, 0) + 1

print("Top 15 Fill Colors in Carta I:")
for c, cnt in sorted(fill_colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB{c} (#{c[0]:02X}{c[1]:02X}{c[2]:02X}): {cnt} objetos")

print("\nTop 15 Stroke Colors in Carta I:")
for c, cnt in sorted(stroke_colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB{c} (#{c[0]:02X}{c[1]:02X}{c[2]:02X}): {cnt} objetos")

print(f"\nPolígonos com dimensão > 100 pt: {len(large_polygons)}")
for lp in large_polygons[:25]:
    print(f"  Obj {lp[0]}: RGB{lp[1]} (#{lp[1][0]:02X}{lp[1][1]:02X}{lp[1][2]:02X}) bounds: x=[{lp[2]:.1f}, {lp[4]:.1f}], y=[{lp[3]:.1f}, {lp[5]:.1f}] w={lp[6]:.1f}, h={lp[7]:.1f}")
