import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

point_x, point_y = ctypes.c_float(), ctypes.c_float()

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        pts = []
        for s_i in range(n_segs):
            seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
            pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
            pts.append((point_x.value, point_y.value))
        
        # Check if points match our ticks
        for x, y in pts:
            if abs(x - 157.9) < 2 and (y < 40 or y > 730):
                print(f"X=-47° Tick pts: {pts}")
                break
            if abs(x - 400.3) < 2 and (y < 40 or y > 730):
                print(f"X=-46° Tick pts: {pts}")
                break
            if abs(y - 606.2) < 2 and (x < 40 or x > 560):
                print(f"Y=-23° Tick pts: {pts}")
                break
            if abs(y - 363.8) < 2 and (x < 40 or x > 560):
                print(f"Y=-24° Tick pts: {pts}")
                break
            if abs(y - 121.4) < 2 and (x < 40 or x > 560):
                print(f"Y=-25° Tick pts: {pts}")
                break
