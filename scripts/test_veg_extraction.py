import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

print("=== TESTE DE EXTRAÇÃO VETORIAL NATIVA DE VEGETAÇÃO ARBÓREA ===")
t0 = time.time()

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/34218_5_3_2_1_1 Vegetação Nativa arbórea.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 12.345755, 269928.85
slope_y, intercept_y = 12.345527, 7380932.58

def pt_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
point_x, point_y = ctypes.c_float(), ctypes.c_float()

polygons_avancado = []
polygons_inicial = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            
            if f_hex in ["#267300", "#55FF00"]:
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                # Excluir a legenda (x > 2650)
                if left.value > 2650:
                    continue
                
                n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
                subpaths = []
                cur_sp = []
                for s_i in range(n_segs):
                    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
                    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
                    s_type = pdfium_c.FPDFPathSegment_GetType(seg)
                    is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
                    
                    ux, uy = pt_to_utm(point_x.value, point_y.value)
                    cur_sp.append((ux, uy))
                    
                    if is_close or s_type == 1:
                        if len(cur_sp) >= 3:
                            subpaths.append(cur_sp)
                        cur_sp = []
                        
                if cur_sp and len(cur_sp) >= 3:
                    subpaths.append(cur_sp)
                    
                if subpaths:
                    try:
                        poly = Polygon(subpaths[0], holes=subpaths[1:] if len(subpaths) > 1 else None)
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        if not poly.is_empty:
                            if f_hex == "#267300":
                                polygons_avancado.append(poly)
                            else:
                                polygons_inicial.append(poly)
                    except Exception as err:
                        pass

print(f"Polígonos extraídos em {time.time()-t0:.2f}s:")
print(f"  Estágio Avançado/Médio (#267300): {len(polygons_avancado)}")
print(f"  Estágio Inicial (#55FF00): {len(polygons_inicial)}")

# Dissolver cada classe
t1 = time.time()
print("\nDissolvendo polígonos nativos...")
union_avancado = unary_union(polygons_avancado)
union_inicial = unary_union(polygons_inicial)
print(f"Dissolve concluído em {time.time()-t1:.2f}s.")

# Carregar limite municipal oficial
mun_gdf = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_poly = mun_gdf.geometry.iloc[0]
mun_area_ha = mun_poly.area / 10000.0
print(f"Área oficial do município: {mun_area_ha:,.2f} ha")

# Clip com o limite municipal
clip_avancado = union_avancado.intersection(mun_poly)
clip_inicial = union_inicial.intersection(mun_poly)

area_av_raw = union_avancado.area / 10000.0
area_av_clip = clip_avancado.area / 10000.0
pct_av = (area_av_clip / mun_area_ha) * 100.0

area_in_raw = union_inicial.area / 10000.0
area_in_clip = clip_inicial.area / 10000.0
pct_in = (area_in_clip / mun_area_ha) * 100.0

total_veg_clip = area_av_clip + area_in_clip
pct_total = (total_veg_clip / mun_area_ha) * 100.0

print("\n=== RESULTADOS DE COBERTURA FLORESTAL ===")
print(f"1. Estágio Avançado e Médio (#267300):")
print(f"   Área bruta: {area_av_raw:,.2f} ha")
print(f"   Área clipada no município: {area_av_clip:,.2f} ha ({pct_av:.2f}% do município)")
print(f"2. Estágio Inicial (#55FF00):")
print(f"   Área bruta: {area_in_raw:,.2f} ha")
print(f"   Área clipada no município: {area_in_clip:,.2f} ha ({pct_in:.2f}% do município)")
print(f"TOTAL VEGETAÇÃO NATIVA ARBÓREA:")
print(f"   Área: {total_veg_clip:,.2f} ha ({pct_total:.2f}% de São Roque)")
