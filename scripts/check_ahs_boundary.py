import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import geopandas as gpd
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34229_4.2.5.1-1 AHS.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 12.346837, 269458.60
slope_y, intercept_y = 12.345527, 7380944.43

def pt_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
point_x, point_y = ctypes.c_float(), ctypes.c_float()

boundary_lines = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            s_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            w = right.value - left.value
            h = top.value - bottom.value
            
            # Limite do município no mapa tem contorno preto #000000 e cobre grande área
            if s_hex == "#000000" and left.value < 2650:
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                if n_segs > 50:
                    print(f"Objeto de fronteira encontrado: idx={idx}, segs={n_segs}, bounds=[{left.value:.1f}, {bottom.value:.1f}, {right.value:.1f}, {top.value:.1f}], size={w:.1f}x{h:.1f}")
                    coords = []
                    for s_i in range(n_segs):
                        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
                        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
                        coords.append(pt_to_utm(point_x.value, point_y.value))
                    if len(coords) >= 3:
                        poly_b = Polygon(coords)
                        if poly_b.is_valid:
                            area_ha = poly_b.area / 10000.0
                            print(f"  Área do polígono de fronteira: {area_ha:.2f} ha")
                            boundary_lines.append(poly_b)

if not boundary_lines:
    print("Nenhum polígono fechado direto com >50 segs, procurando polilinhas...")
    for idx, p in enumerate(objs):
        if type(p).__name__ == 'PdfObject':
            pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
            if st.value != 0:
                pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
                s_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
                if s_hex == "#000000":
                    pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                    w = right.value - left.value
                    h = top.value - bottom.value
                    if w > 200 or h > 200:
                        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                        print(f"  Linha preta longa: idx={idx}, segs={n_segs}, size={w:.1f}x{h:.1f}, bounds=[{left.value:.1f}, {bottom.value:.1f}, {right.value:.1f}, {top.value:.1f}]")
