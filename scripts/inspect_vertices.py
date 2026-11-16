import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

x = ctypes.c_float()
y = ctypes.c_float()

# Inspecionar caminhos 100, 200, 300
for idx in [100, 500, 1000]:
    p = path_objs[idx]
    n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
    pts = []
    for s in range(n_seg):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        pts.append((x.value, y.value))
    print(f"\nPath {idx} (segs={n_seg}):")
    for pt in pts[:10]:
        print(f"  ({pt[0]:.2f}, {pt[1]:.2f})")

doc.close()
