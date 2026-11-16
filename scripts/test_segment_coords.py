import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

p = path_objs[1]
n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
print(f"Path 1 tem {n_seg} segmentos:")

x = ctypes.c_float()
y = ctypes.c_float()

points = []
for i in range(min(n_seg, 10)):
    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
    seg_type = pdfium_c.FPDFPathSegment_GetType(seg)
    is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
    points.append((x.value, y.value, seg_type, is_close))
    print(f"  Seg {i}: ({x.value:.2f}, {y.value:.2f}), type={seg_type}, close={is_close}")

doc.close()
