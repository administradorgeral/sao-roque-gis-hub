import pypdfium2 as pdfium
import ctypes
import pypdfium2.raw as pdfium_c

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
point_x, point_y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

ticks = []

for i, p in enumerate(objs):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        if n_segs == 2:
            seg0 = pdfium_c.FPDFPath_GetPathSegment(p.raw, 0)
            seg1 = pdfium_c.FPDFPath_GetPathSegment(p.raw, 1)
            x0, y0 = ctypes.c_float(), ctypes.c_float()
            x1, y1 = ctypes.c_float(), ctypes.c_float()
            pdfium_c.FPDFPathSegment_GetPoint(seg0, ctypes.byref(x0), ctypes.byref(y0))
            pdfium_c.FPDFPathSegment_GetPoint(seg1, ctypes.byref(x1), ctypes.byref(y1))
            
            dx = abs(x1.value - x0.value)
            dy = abs(y1.value - y0.value)
            length = (dx**2 + dy**2)**0.5
            if 1.0 < length < 10.0:
                ticks.append((i, x0.value, y0.value, x1.value, y1.value, length))

print(f"Found {len(ticks)} tick line segments:")
for t in ticks:
    print(f"  #{t[0]}: ({t[1]:.2f}, {t[2]:.2f}) -> ({t[3]:.2f}, {t[4]:.2f}), len={t[5]:.2f}")
