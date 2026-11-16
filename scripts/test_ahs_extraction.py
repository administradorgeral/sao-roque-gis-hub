import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid

print("=== TESTE DE EXTRAÇÃO VETORIAL NATIVA DAS AHS ===")
t0 = time.time()

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

polygons = []
legend_swatches = []

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            if f_hex == "#A80084":
                pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
                # Excluir a amostra da legenda (x > 2650)
                if left.value > 2650:
                    legend_swatches.append(idx)
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
                        if len(subpaths) == 1:
                            poly = Polygon(subpaths[0])
                        else:
                            poly = Polygon(subpaths[0], subpaths[1:])
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        if not poly.is_empty:
                            polygons.append(poly)
                    except Exception as e:
                        pass

print(f"Polígonos AHS extraídos: {len(polygons)}")
print(f"Amostras de legenda ignoradas: {legend_swatches}")

t1 = time.time()
print(f"Tempo de extração dos caminhos: {t1 - t0:.2f}s")

# Unir/dissolver polígonos
print("Executando unary_union das feições de AHS...")
dissolved_ahs = unary_union(polygons)
t2 = time.time()
print(f"Tempo de dissolução: {t2 - t1:.2f}s")

area_m2 = dissolved_ahs.area
area_ha = round(area_m2 / 10000.0, 2)
area_km2 = round(area_ha / 100.0, 2)
print(f"Área Total Dissolvida de AHS: {area_ha} ha ({area_km2} km²)")

# Carregar contorno municipal para auditoria de enquadramento
gdf_mun = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_poly = gdf_mun.geometry.iloc[0]
mun_ha = round(mun_poly.area / 10000.0, 2)
pct_mun = round((area_ha / mun_ha) * 100, 2)
print(f"Porcentagem do Município ({mun_ha} ha): {pct_mun}% de AHS")

# Verificar se AHS ultrapassa contorno municipal
inter_geom = dissolved_ahs.intersection(mun_poly)
inter_ha = round(inter_geom.area / 10000.0, 2)
print(f"Área de AHS estritamente interna ao município: {inter_ha} ha ({round(inter_ha/area_ha*100, 2)}% de concordância)")
