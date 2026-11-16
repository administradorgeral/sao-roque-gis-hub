import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

print(f"Total paths: {len(path_objs)}")

# Pegar cores dos primeiros 100 paths
for i in [0, 10, 100, 1000, 10000, 50000, 100000]:
    if i < len(path_objs):
        p = path_objs[i]
        r = ctypes.c_uint()
        g = ctypes.c_uint()
        b = ctypes.c_uint()
        a = ctypes.c_uint()
        res_stroke = pdfium_c.FPDFPath_GetStrokeColor(p.raw, r, g, b, a)
        stroke_rgba = (r.value, g.value, b.value, a.value)
        res_fill = pdfium_c.FPDFPath_GetFillColor(p.raw, r, g, b, a)
        fill_rgba = (r.value, g.value, b.value, a.value)
        num_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
        bounds = p.get_bounds()
        print(f"Path {i}: stroke={stroke_rgba}, fill={fill_rgba}, segs={num_seg}, bounds={bounds}")

doc.close()
