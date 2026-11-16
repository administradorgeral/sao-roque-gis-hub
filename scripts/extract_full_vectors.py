import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
from shapely.geometry import Polygon, MultiPolygon
from shapely import transform, make_valid, union_all
import pyproj

print("Iniciando extração e montagem geométrica...")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]
print(f"Lidos {len(path_objs)} paths em {time.time()-t0:.2f}s")

color_map = {
    "#FFFF73": {"classe": "Plano (0 a 3%)", "cor": "#FFFF73", "code": "CL_1_PLANO"},
    "#FFFF00": {"classe": "Suave ondulado (3 a 8%)", "cor": "#FFFF00", "code": "CL_2_SUAVE"},
    "#FFAA00": {"classe": "Ondulado (8 a 20%)", "cor": "#FFAA00", "code": "CL_3_ONDULADO"},
    "#FF5500": {"classe": "Forte ondulado (20 a 45%)", "cor": "#FF5500", "code": "CL_4_FORTE_ONDULADO"},
    "#E60000": {"classe": "Montanhoso (45 a 75%)", "cor": "#E60000", "code": "CL_5_MONTANHOSO"}
}

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
x = ctypes.c_float()
y = ctypes.c_float()

# Fatores da matriz afim para UTM SIRGAS 2000 Fuso 23S
scale_x = 17.636684
scale_y = 17.639795
x0_pt = 31.4408
y0_pt = 35.9703
utm_x0 = 270308.48
utm_y0 = 7382234.44

class_polys_utm = {c: [] for c in color_map}

t1 = time.time()
for p in path_objs:
    b_box = p.get_bounds()
    # Pular elementos fora do mapa (ex: legendas, encartes)
    if b_box[0] < 30 or b_box[2] > 1675 or b_box[1] < 35 or b_box[3] > 1622:
        continue

    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    hex_col = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    
    if hex_col not in color_map:
        continue
        
    n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
    current_ring = []
    rings = []
    
    for s in range(n_seg):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        seg_type = pdfium_c.FPDFPathSegment_GetType(seg)
        is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
        
        # Converter para coordenadas UTM SIRGAS 2000
        utm_x = utm_x0 + (x.value - x0_pt) * scale_x
        utm_y = utm_y0 + (y.value - y0_pt) * scale_y
        
        if seg_type == 2: # MOVETO (novo anel ou novo polígono)
            if len(current_ring) >= 3:
                rings.append(current_ring)
            current_ring = [(utm_x, utm_y)]
        else:
            current_ring.append((utm_x, utm_y))
            if is_close and len(current_ring) >= 3:
                rings.append(current_ring)
                current_ring = []
                
    if len(current_ring) >= 3:
        rings.append(current_ring)
        
    for ring in rings:
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        try:
            poly = Polygon(ring)
            if poly.is_valid and poly.area > 25.0: # filtrar ruídos < 25 m²
                class_polys_utm[hex_col].append(poly)
            elif not poly.is_valid:
                fixed = make_valid(poly)
                if fixed.is_valid and fixed.area > 25.0:
                    class_polys_utm[hex_col].append(fixed)
        except Exception:
            pass

print(f"Extração e conversão UTM concluída em {time.time()-t1:.2f}s:")
for c, polys in class_polys_utm.items():
    print(f"  {color_map[c]['classe']}: {len(polys)} polígonos válidos")

doc.close()
