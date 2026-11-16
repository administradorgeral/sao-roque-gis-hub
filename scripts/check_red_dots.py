import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

red_dots = []

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            if (r.value, g.value, b.value) == (255, 0, 0):
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                cx = (left.value + right.value) / 2
                cy = (bottom.value + top.value) / 2
                red_dots.append((cx, cy))

print(f"Total red dots found: {len(red_dots)}")
# Sort by x
red_dots.sort(key=lambda pt: pt[0])
print(f"Westernmost red dots (min x): {red_dots[:10]}")
