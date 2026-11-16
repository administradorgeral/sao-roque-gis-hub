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

target_classes = {
    '#006100': ('muito_fraca', 'Muito Fraca'),
    '#7AAB00': ('fraca', 'Fraca'),
    '#FFFF00': ('media', 'Média'),
    '#FF0000': ('forte', 'Forte'),
    '#A80000': ('muito_forte', 'Muito Forte')
}

polys_by_color = {c: [] for c in target_classes}

print('Extracting vector objects...')
for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
                if f_hex in target_classes:
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
                                if poly.is_valid and poly.area > 25:
                                    polys_by_color[f_hex].append(poly)
                            current_sp = [pt]
                        else:
                            current_sp.append(pt)
                    if len(current_sp) >= 3:
                        poly = Polygon(current_sp)
                        if poly.is_valid and poly.area > 25:
                            polys_by_color[f_hex].append(poly)

print(f'Extraction completed in {time.time()-t0:.2f}s')
for c, plist in polys_by_color.items():
    print(f'  {target_classes[c][1]} ({c}): {len(plist)} polygons')

# Dissolve each
dissolved = {}
for c, plist in polys_by_color.items():
    t_start = time.time()
    # 1.2m simplification for clean topology and fast union
    simplified = [p.simplify(1.2, preserve_topology=True) for p in plist]
    u = unary_union(simplified)
    if not u.is_valid:
        u = make_valid(u)
    dissolved[c] = u
    print(f'Dissolved {target_classes[c][1]} in {time.time()-t_start:.2f}s | Area = {u.area/10000.0:.2f} ha')

# Clean Média by subtracting overlapping other classes
print('Subtracting other classes from Média...')
t_sub = time.time()
non_media = unary_union([dissolved['#006100'], dissolved['#7AAB00'], dissolved['#FF0000'], dissolved['#A80000']])
dissolved['#FFFF00'] = dissolved['#FFFF00'].difference(non_media)
if not dissolved['#FFFF00'].is_valid:
    dissolved['#FFFF00'] = make_valid(dissolved['#FFFF00'])
final_media_area = dissolved['#FFFF00'].area / 10000.0
print(f'Média cleaned in {time.time()-t_sub:.2f}s | Final Area = {final_media_area:.2f} ha')

total_area = sum(u.area for u in dissolved.values()) / 10000.0
print(f'\nTOTAL DISSOLVED AREA: {total_area:.2f} ha (PDA reference: 30709.52 ha)')
for c, u in dissolved.items():
    area_ha = u.area / 10000.0
    pct = (area_ha / total_area) * 100 if total_area > 0 else 0
    print(f'{target_classes[c][1]}: {area_ha:.2f} ha ({pct:.2f}%)')
