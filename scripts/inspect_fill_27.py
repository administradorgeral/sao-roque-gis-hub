import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon
from shapely.validation import make_valid

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

x, y = ctypes.c_float(), ctypes.c_float()
p = objs[27]

n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
current_sp = []
subpaths = []
for s in range(n_segs):
    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
    stype = pdfium_c.FPDFPathSegment_GetType(seg)
    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
    pt = pdf_to_utm(x.value, y.value)
    if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
        if len(current_sp) >= 3:
            subpaths.append(current_sp)
        current_sp = [pt]
    else:
        current_sp.append(pt)
if len(current_sp) >= 3:
    subpaths.append(current_sp)

print(f"Object #27 has {len(subpaths)} subpaths:")
for idx, sp in enumerate(subpaths):
    if sp[0] != sp[-1]:
        sp.append(sp[0])
    poly = Polygon(sp)
    if not poly.is_valid:
        poly = make_valid(poly)
    print(f"  Subpath #{idx}: {len(sp)} pts, area={poly.area/10000.0:.2f} ha, bounds={poly.bounds}")
