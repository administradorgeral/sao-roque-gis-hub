import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union
import geopandas as gpd

t0 = time.time()
doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa Fragilidade Potencial.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.639957, 273175.28
slope_y, intercept_y = 17.638071, 7380747.19

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

polys_mf = []
for idx in range(3, 11927):
    p = objs[idx]
    pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
    if fm.value != 0:
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        if left.value >= 25 and right.value <= 1675:
            n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
            current_sp = []
            for s in range(n_segs):
                seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
                stype = pdfium_c.FPDFPathSegment_GetType(seg)
                pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
                pt = pdf_to_utm(x.value, y.value)
                if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
                    if len(current_sp) >= 3:
                        poly = Polygon(current_sp)
                        if poly.is_valid and poly.area > 50:
                            polys_mf.append(poly)
                    current_sp = [pt]
                else:
                    current_sp.append(pt)
            if len(current_sp) >= 3:
                poly = Polygon(current_sp)
                if poly.is_valid and poly.area > 50:
                    polys_mf.append(poly)

print(f'Extracted {len(polys_mf)} polygons for Muito Fraca in {time.time()-t0:.2f}s')

t1 = time.time()
# Simplify slightly (e.g. 1.0 m tolerance in UTM) for high-speed robust unary_union
simplified = [p.simplify(1.0, preserve_topology=True) for p in polys_mf]
print(f'Simplified in {time.time()-t1:.2f}s')

t2 = time.time()
u = unary_union(simplified)
print(f'Dissolved in {time.time()-t2:.2f}s | Area = {u.area / 10000.0:.2f} ha')
