import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

print(f"Total paths: {len(path_objs)}")

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

# Inspecionar os primeiros 20 paths
for i in range(20):
    p = path_objs[i]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    hex_col = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
    bounds = p.get_bounds()
    print(f"Path {i}: Cor={hex_col}, Segs={n_seg}, BBox W={bounds[2]-bounds[0]:.2f} pt, H={bounds[3]-bounds[1]:.2f} pt")

doc.close()
