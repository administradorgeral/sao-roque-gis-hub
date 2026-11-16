import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from shapely.geometry import Polygon
from shapely.validation import make_valid
from shapely.ops import unary_union

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa Fragilidade Potencial.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.639957, 273175.28
slope_y, intercept_y = 17.638071, 7380747.19

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

red, grn, blu, alf = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

polys_yellow = []
for p in objs:
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(red), ctypes.byref(grn), ctypes.byref(blu), ctypes.byref(alf))
                if f'#{red.value:02X}{grn.value:02X}{blu.value:02X}' == '#FFFF00':
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
                    for sp in subpaths:
                        if len(sp) >= 3:
                            if sp[0] != sp[-1]:
                                sp.append(sp[0])
                            poly = Polygon(sp)
                            if not poly.is_valid:
                                poly = make_valid(poly)
                            if not poly.is_empty and poly.area > 25:
                                polys_yellow.append(poly)

print(f'Polygons extracted for Yellow: {len(polys_yellow)}')
raw_sum = sum(p.area for p in polys_yellow) / 10000.0
print(f'Raw sum: {raw_sum:.2f} ha')
simplified = [p.simplify(1.0, preserve_topology=True) for p in polys_yellow]
u = unary_union(simplified)
print(f'Dissolved Yellow area: {u.area / 10000.0:.2f} ha')
