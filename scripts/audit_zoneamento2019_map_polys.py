import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
from collections import Counter
from shapely.geometry import Polygon
from shapely.validation import make_valid

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf')
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

target_colors = {
    '#FF7F7F': 'ZONA PRIORITÁRIA DE GESTÃO AOS PROCESSOS DE URBANIZAÇÃO',
    '#55FF00': 'ZONA PRIORITÁRIA DE PROTEÇÃO À BIODIVERSIDADE',
    '#FFAA00': 'Subzona Especial para Controle de Processos Erosivos',
    '#FFFF00': 'Subzona Especial de Controle Escoamento Superficial Águas Pluviais',
    '#E8BEFF': 'Subzona Desenvolvimento Socioambiental',
    '#CA7AF5': 'Subzona de Desenvolvimento Socioeconômico - Castelo Branco',
    '#0070FF': 'Subzona de Áreas Hidrologicamente Sensíveis',
    '#00A9E6': 'Subzona de Manancial em Áreas Rurais',
    '#97DBF2': 'Subzona de Manancial em Usos Intensivos ou Urbanizados'
}

polys_by_color = {c: [] for c in target_colors}
other_colors = Counter()

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            # exclude legend box (x > 1100 and y > 1050) and locator map (x > 1750)
            if left.value < 1650 and not (left.value > 1100 and bottom.value > 1050):
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f'#{r.value:02X}{g.value:02X}{b.value:02X}'
                if f_hex in target_colors:
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
                            if not poly.is_empty and poly.area > 50:
                                polys_by_color[f_hex].append(poly)
                else:
                    other_colors[f_hex] += 1

print("Polygons by zone color in map:")
for c, plist in polys_by_color.items():
    raw_area = sum(p.area for p in plist) / 10000.0
    print(f"  {c} ({target_colors[c]}): {len(plist)} polys | Raw Area = {raw_area:.2f} ha")

print(f"\nOther colors: {other_colors}")
