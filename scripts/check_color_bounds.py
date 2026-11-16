import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

color_bounds = {}

for p in page.get_objects():
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c = (r.value, g.value, b.value)
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            
            if c not in color_bounds:
                color_bounds[c] = [left.value, bottom.value, right.value, top.value, 1]
            else:
                cb = color_bounds[c]
                cb[0] = min(cb[0], left.value)
                cb[1] = min(cb[1], bottom.value)
                cb[2] = max(cb[2], right.value)
                cb[3] = max(cb[3], top.value)
                cb[4] += 1

print("Bounds of Fill Colors in Carta I:")
for c, cb in color_bounds.items():
    hex_c = f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}"
    print(f"Color RGB{c} ({hex_c}) -> {cb[4]} objs: x=[{cb[0]:.1f}, {cb[2]:.1f}], y=[{cb[1]:.1f}, {cb[3]:.1f}] w={cb[2]-cb[0]:.1f}, h={cb[3]-cb[1]:.1f}")
