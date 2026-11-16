import os
import sys
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString
from shapely.ops import unary_union, linemerge, polygonize
from shapely.validation import make_valid
from PIL import Image

print("=== PROCESSAMENTO DA RESERVA DA BIOSFERA DO CINTURÃO VERDE (RBCV 2019) ===")

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# 1. Renderizar imagem regional em alta resolução
print("1. Renderizando raster regional da RBCV...")
scale = 300 / 72
bitmap = page.render(scale=scale)
pil_img = bitmap.to_pil()

# Coordenadas do mapa interno em pt
# X de 31.2 a 564.5 pt
# Y de 32.8 a 740.2 pt (PDF bottom-up)
page_h = 841.4929
x0 = int(31.2 * scale)
x1 = int(564.5 * scale)
y0 = int((page_h - 740.2) * scale)
y1 = int((page_h - 32.8) * scale)

crop_map = pil_img.crop((x0, y0, x1, y1))
raster_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png"
crop_map.save(raster_out, optimize=True)
print(f"  Raster salvo ({crop_map.size[0]}x{crop_map.size[1]} px): {raster_out}")

# 2. Extrair vetores nativos
print("\n2. Extraindo geometrias vetoriais nativas...")
slope_lon = 0.00412524
intercept_lon = -47.610866

slope_lat = 0.00412490
intercept_lat = -25.492884

def pt_to_geo(px, py):
    lon = slope_lon * px + intercept_lon
    lat = slope_lat * py + intercept_lat
    return (lon, lat)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
point_x, point_y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

nucleos_polygons = []
limite_lines = []
urban_polygons = []

objs = list(page.get_objects())

for idx, p in enumerate(objs):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        
        # Ignorar legendas (x > 320 e y < 220)
        if left.value > 320 and top.value < 220:
            continue
            
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        if n_segs < 2:
            continue
            
        # Coletar pontos
        cur_subpaths = []
        cur_pts = []
        for s_i in range(n_segs):
            seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s_i)
            pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(point_x), ctypes.byref(point_y))
            s_type = pdfium_c.FPDFPathSegment_GetType(seg)
            is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
            
            lon, lat = pt_to_geo(point_x.value, point_y.value)
            cur_pts.append((lon, lat))
            
            if is_close or s_type == 1:
                if len(cur_pts) >= 2:
                    cur_subpaths.append(cur_pts)
                cur_pts = []
        if cur_pts and len(cur_pts) >= 2:
            cur_subpaths.append(cur_pts)

        # Tratar Fill
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            
            if f_hex == "#38A800": # Zona Núcleo
                for sp in cur_subpaths:
                    if len(sp) >= 3:
                        try:
                            poly = Polygon(sp)
                            if not poly.is_valid:
                                poly = make_valid(poly)
                            if not poly.is_empty:
                                nucleos_polygons.append(poly)
                        except Exception:
                            pass
            elif f_hex == "#FF0000": # Mancha Urbana
                for sp in cur_subpaths:
                    if len(sp) >= 3:
                        try:
                            poly = Polygon(sp)
                            if not poly.is_valid:
                                poly = make_valid(poly)
                            if not poly.is_empty:
                                urban_polygons.append(poly)
                        except Exception:
                            pass

        # Tratar Stroke (Limite RBCV)
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            s_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            if s_hex == "#000000" and n_segs > 5:
                for sp in cur_subpaths:
                    if len(sp) >= 2:
                        try:
                            line = LineString(sp)
                            if not line.is_empty:
                                limite_lines.append(line)
                        except Exception:
                            pass

print(f"  Zonas-Núcleo (#38A800): {len(nucleos_polygons)} polígonos")
print(f"  Limite RBCV Linhas: {len(limite_lines)} segmentos")
print(f"  Mancha Urbana (#FF0000): {len(urban_polygons)} polígonos")

# 3. Dissolver Zonas-Núcleo
print("\n3. Dissolvendo Zonas-Núcleo...")
union_nucleos = unary_union(nucleos_polygons)
print(f"  Zonas-Núcleo dissolvidas: área aproximada = {union_nucleos.area:.4f} graus²")

# 4. Mesclar Linhas de Limite RBCV
print("4. Mesclando segmentos do Limite RBCV...")
merged_limite = linemerge(limite_lines)

# Salvar GeoJSONs
gdf_nucleos = gpd.GeoDataFrame([
    {
        "id": "rbcv_nucleos",
        "nome": "Zonas-Núcleo da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Proteção Integral Estrita (UNESCO)",
        "classe": "Zona Núcleo",
        "esfera": "Internacional / Federal / Estadual",
        "orgao": "UNESCO / MaB / COBRAMAB / Instituto Florestal / Fundação Florestal",
        "base_legal": "Resolução 28 C/2.4 UNESCO, CF/88 Art. 225, Lei 9.985/00 Art. 41, Dec. 4.340/02, Dec. 12.035/24, Dec. Est. 47.094/02",
        "cor_hex": "#38A800",
        "geometry": union_nucleos
    }
], crs="EPSG:4326")

nucleos_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_nucleos_web.geojson"
gdf_nucleos.to_file(nucleos_out, driver="GeoJSON")
print(f"  GeoJSON Núcleos salvo: {nucleos_out}")

gdf_limite = gpd.GeoDataFrame([
    {
        "id": "rbcv_limite",
        "nome": "Limite Oficial da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Perímetro Internacional Homologado (UNESCO)",
        "classe": "Limite RBCV",
        "esfera": "Internacional / Estadual",
        "orgao": "UNESCO / MaB / Conselho de Gestão da RBCV",
        "base_legal": "Decreto Estadual nº 47.094/2002, Programa MaB UNESCO (1994), LC nº 39/2006",
        "cor_hex": "#000000",
        "geometry": merged_limite
    }
], crs="EPSG:4326")

limite_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_limite_web.geojson"
gdf_limite.to_file(limite_out, driver="GeoJSON")
print(f"  GeoJSON Limite salvo: {limite_out}")

# Salvar também GeoPackage unificado
gpkg_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde.gpkg"
gdf_nucleos.to_file(gpkg_out, layer="zonas_nucleo", driver="GPKG")
gdf_limite.to_file(gpkg_out, layer="limite_rbcv", driver="GPKG")
print(f"  GPKG unificado salvo: {gpkg_out}")

# Bounds geográficos da imagem para Leaflet ImageOverlay:
lat_min = slope_lat * 32.8 + intercept_lat
lat_max = slope_lat * 740.2 + intercept_lat
lon_min = slope_lon * 31.2 + intercept_lon
lon_max = slope_lon * 564.5 + intercept_lon

print("\n=== BOUNDS OFICIAIS PARA LEAFLET IMAGE OVERLAY ===")
print(f"[[{lat_min:.5f}, {lon_min:.5f}], [{lat_max:.5f}, {lon_max:.5f}]]")
