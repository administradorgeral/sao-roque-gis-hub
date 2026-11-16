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

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

# Let's check a small spatial window (e.g. 500m x 500m in UTM) to see if polygons of different colors overlap!
# UTM window: 280000 to 282000 E, 7395000 to 7397000 N
x_min, x_max = 280000, 282000
y_min, y_max = 7395000, 7397000

window_polys = {c: [] for c in ['#006100', '#7AAB00', '#FFFF00', '#FF0000', '#A80000']}

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
                if f_hex in window_polys:
                    # check if bounds intersect window
                    u_l, u_b = pdf_to_utm(left.value, bottom.value)
                    u_r, u_t = pdf_to_utm(right.value, top.value)
                    if not (u_r < x_min or u_l > x_max or u_t < y_min or u_b > y_max):
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
                                if not poly.is_empty:
                                    window_polys[f_hex].append(poly)

print('Window polygon counts:')
for c, lst in window_polys.items():
    print(f'{c}: {len(lst)} polys')

# Test overlap between yellow and red in this window
if window_polys['#FFFF00'] and window_polys['#FF0000']:
    u_yellow = unary_union(window_polys['#FFFF00'])
    u_red = unary_union(window_polys['#FF0000'])
    inter = u_yellow.intersection(u_red)
    print(f'Intersection area between Yellow and Red in window: {inter.area:.2f} m2')
    print(f'Yellow area in window: {u_yellow.area:.2f} m2')
    print(f'Red area in window: {u_red.area:.2f} m2')
