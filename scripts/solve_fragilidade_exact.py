import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
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

target_classes = {
    '#006100': ('muito_fraca', 'Muito Fraca'),
    '#7AAB00': ('fraca', 'Fraca'),
    '#FFFF00': ('media', 'Média'),
    '#FF0000': ('forte', 'Forte'),
    '#A80000': ('muito_forte', 'Muito Forte')
}

polys_by_color = {c: [] for c in target_classes}

for p in objs:
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(red), ctypes.byref(grn), ctypes.byref(blu), ctypes.byref(alf))
                f_hex = f'#{red.value:02X}{grn.value:02X}{blu.value:02X}'
                if f_hex in target_classes:
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
                                polys_by_color[f_hex].append(poly)

dissolved = {}
for c, plist in polys_by_color.items():
    t0 = time.time()
    simplified = [p.simplify(1.0, preserve_topology=True) for p in plist]
    u = unary_union(simplified)
    if not u.is_valid:
        u = make_valid(u)
    dissolved[c] = u
    print(f'{target_classes[c][1]} ({c}): {len(plist)} polys -> dissolved {u.area/10000.0:.2f} ha in {time.time()-t0:.1f}s')

# Now subtract other classes from Yellow (Média)
t_sub = time.time()
other_classes = unary_union([dissolved['#006100'], dissolved['#7AAB00'], dissolved['#FF0000'], dissolved['#A80000']])
cleaned_yellow = dissolved['#FFFF00'].difference(other_classes)
if not cleaned_yellow.is_valid:
    cleaned_yellow = make_valid(cleaned_yellow)
dissolved['#FFFF00'] = cleaned_yellow
print(f'Média after subtracting overlapping classes: {dissolved["#FFFF00"].area/10000.0:.2f} ha (took {time.time()-t_sub:.1f}s)')

total_ha = sum(g.area for g in dissolved.values()) / 10000.0
print(f'\nTOTAL NON-OVERLAPPING TERRITORY: {total_ha:.2f} ha (Official PDA: 30709.52 ha)')
for c, g in dissolved.items():
    ha = g.area / 10000.0
    pct = (ha / total_ha) * 100
    print(f'  {target_classes[c][1]}: {ha:.2f} ha ({pct:.2f}%)')
