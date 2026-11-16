import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()

fill_colors = {}
stroke_colors = {}

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            fill_colors[c] = fill_colors.get(c, 0) + 1
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            stroke_colors[c] = stroke_colors.get(c, 0) + 1

print("Fill colors count:")
for c, cnt in sorted(fill_colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB{c}: #{c[0]:02X}{c[1]:02X}{c[2]:02X} -> {cnt} objects")

print("\nStroke colors count:")
for c, cnt in sorted(stroke_colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB{c}: #{c[0]:02X}{c[1]:02X}{c[2]:02X} -> {cnt} objects")
