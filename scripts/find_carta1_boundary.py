import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]

point_x, point_y = ctypes.c_float(), ctypes.c_float()
fm, st = ctypes.c_int(), ctypes.c_int()
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

paths = []

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        if n_segs > 50:  # long paths
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c_stroke = (r.value, g.value, b.value)
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            c_fill = (r.value, g.value, b.value)
            paths.append((idx, n_segs, c_stroke, c_fill))

paths.sort(key=lambda x: x[1], reverse=True)
print(f"Top 15 longest paths in Carta I:")
for p in paths[:15]:
    print(f"  Path {p[0]}: {p[1]} segmentos, stroke={p[2]}, fill={p[3]}")
