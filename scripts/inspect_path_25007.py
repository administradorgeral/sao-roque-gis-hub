import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]

objs = list(page.get_objects())
p = objs[25007]
point_x, point_y = ctypes.c_float(), ctypes.c_float()
n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
pts = []
for s_i in range(n_segs):
    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
    pts.append((point_x.value, point_y.value))

xs = [pt[0] for pt in pts]
ys = [pt[1] for pt in pts]

print(f"Path 25007: {len(pts)} pontos.")
print(f"  X range: {min(xs):.1f} to {max(xs):.1f} (width: {max(xs)-min(xs):.1f})")
print(f"  Y range: {min(ys):.1f} to {max(ys):.1f} (height: {max(ys)-min(ys):.1f})")
