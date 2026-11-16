import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
from shapely.geometry import Polygon
from shapely.validation import make_valid

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x = 17.639957
intercept_x = 273175.28
slope_y = 17.638071
intercept_y = 7380747.19

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

target_colors = {
    "#006100": "Muito Fraca",
    "#7AAB00": "Fraca",
    "#FFFF00": "Média",
    "#FF0000": "Forte",
    "#A80000": "Muito Forte"
}

area_sums = {c: 0.0 for c in target_colors}
poly_counts = {c: 0 for c in target_colors}

for i, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
                if f_hex in target_colors:
                    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                    subpaths = []
                    current_sp = []
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
                        if len(sp) < 3:
                            continue
                        if sp[0] != sp[-1]:
                            sp.append(sp[0])
                        poly = Polygon(sp)
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        if not poly.is_empty:
                            area_sums[f_hex] += poly.area
                            poly_counts[f_hex] += 1

doc.close()

total_area_ha = sum(area_sums.values()) / 10000.0
print(f"Total Area: {total_area_ha:.2f} ha\n")
for c, name in target_colors.items():
    area_ha = area_sums[c] / 10000.0
    pct = (area_ha / total_area_ha) * 100 if total_area_ha > 0 else 0
    print(f"{name} ({c}): {area_ha:.2f} ha ({pct:.2f}%) | Polys: {poly_counts[c]}")
