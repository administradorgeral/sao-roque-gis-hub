import os
import sys
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString
from shapely.ops import unary_union, linemerge
from shapely.validation import make_valid
from PIL import Image

print("=== REPROCESSAMENTO DE PRECISÃO MATEMÁTICA DA RBCV (UNESCO 2019) ===")

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# 1. Calibração baseada estritamente nos Ticks da Grade Cartográfica do PDF
# Tick 47°W (#87/#96): x = 157.92 pt -> Lon = -47.0°
# Tick 46°W (#69/#78): x = 400.33 pt -> Lon = -46.0°
# Delta X = 242.41 pt
slope_lon = 1.0 / 242.41
intercept_lon = -47.0 - (slope_lon * 157.92)

# Tick 25°S (#141/#150): y = 121.41 pt -> Lat = -25.0°
# Tick 24°S (#123/#132): y = 363.84 pt -> Lat = -24.0°
# Tick 23°S (#105/#114): y = 606.27 pt -> Lat = -23.0°
# Delta Y = 242.43 pt
slope_lat = 1.0 / 242.43
intercept_lat = -25.0 - (slope_lat * 121.41)

print(f"Parâmetros Exatos:")
print(f"  slope_lon: {slope_lon:.8f}, intercept_lon: {intercept_lon:.8f}")
print(f"  slope_lat: {slope_lat:.8f}, intercept_lat: {intercept_lat:.8f}")

# 2. Renderizar e Recortar o Raster da Moldura Interna (Neatline)
scale = 300 / 72
bitmap = page.render(scale=scale)
pil_img = bitmap.to_pil()

page_h = 841.49292
x_min, x_max = 31.201, 564.493
y_min, y_max = 33.079, 740.201

x0 = int(round(x_min * scale))
x1 = int(round(x_max * scale))
y0 = int(round((page_h - y_max) * scale))
y1 = int(round((page_h - y_min) * scale))

crop_map = pil_img.crop((x0, y0, x1, y1))
raster_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png"
crop_map.save(raster_out, optimize=True)
print(f"  Raster salvo ({crop_map.size[0]}x{crop_map.size[1]} px): {raster_out}")

# Bounds para o Leaflet:
lat_min = slope_lat * y_min + intercept_lat
lat_max = slope_lat * y_max + intercept_lat
lon_min = slope_lon * x_min + intercept_lon
lon_max = slope_lon * x_max + intercept_lon

leaflet_bounds = [[round(lat_min, 5), round(lon_min, 5)], [round(lat_max, 5), round(lon_max, 5)]]
print(f"  Novos Bounds Leaflet: {leaflet_bounds}")

# 3. Extrair Vetores Nativos do PDF com a Nova Calibração
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

        # Tratar Fill: Zona Núcleo (#38A800)
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            f_hex = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
            
            if f_hex == "#38A800":
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

        # Tratar Stroke: Limite RBCV (#000000)
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
print(f"  Limite RBCV: {len(limite_lines)} segmentos de linha")

union_nucleos = unary_union(nucleos_polygons)
merged_limite = linemerge(limite_lines)

# 4. Gravar GeoJSONs e GeoPackage
gdf_nucleos = gpd.GeoDataFrame([
    {
        "id": "rbcv_nucleos",
        "nome": "Zonas-Núcleo da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Proteção Integral Estrita (UNESCO)",
        "classe": "Zona Núcleo",
        "codigo": "RBCV_NUCLEO",
        "esfera": "Internacional / Federal / Estadual",
        "orgao": "UNESCO / MaB / COBRAMAB / Instituto Florestal / Fundação Florestal",
        "base_legal": "Resolução 28 C/2.4 UNESCO, CF/88 Art. 225, Lei 9.985/00 Art. 41, Dec. 4.340/02, Dec. 12.035/24, Dec. Est. 47.094/02",
        "cor_hex": "#38A800",
        "geometry": union_nucleos
    }
], crs="EPSG:4326")

nucleos_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_nucleos_web.geojson"
gdf_nucleos.to_file(nucleos_out, driver="GeoJSON")

gdf_limite = gpd.GeoDataFrame([
    {
        "id": "rbcv_limite",
        "nome": "Limite Oficial da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Perímetro Internacional Homologado (UNESCO)",
        "classe": "Limite RBCV",
        "codigo": "RBCV_LIMITE",
        "esfera": "Internacional / Estadual",
        "orgao": "UNESCO / MaB / Conselho de Gestão da RBCV",
        "base_legal": "Decreto Estadual nº 47.094/2002, Programa MaB UNESCO (1994), LC nº 39/2006",
        "cor_hex": "#0F172A",
        "geometry": merged_limite
    }
], crs="EPSG:4326")

limite_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_limite_web.geojson"
gdf_limite.to_file(limite_out, driver="GeoJSON")

# GeoJSON Unificado para a camada
gdf_unified = gpd.GeoDataFrame([
    {
        "id": "rbcv_nucleos",
        "nome": "Zonas-Núcleo da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Proteção Integral Estrita (UNESCO)",
        "classe": "Zona Núcleo",
        "codigo": "RBCV_NUCLEO",
        "esfera": "Internacional / Federal / Estadual",
        "orgao": "UNESCO / MaB / COBRAMAB / Instituto Florestal / Fundação Florestal",
        "base_legal": "Resolução 28 C/2.4 UNESCO, CF/88 Art. 225, Lei 9.985/00 Art. 41, Dec. 4.340/02, Dec. 12.035/24, Dec. Est. 47.094/02",
        "cor_hex": "#38A800",
        "geometry": union_nucleos
    },
    {
        "id": "rbcv_limite",
        "nome": "Limite Oficial da Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)",
        "categoria": "Perímetro Internacional Homologado (UNESCO)",
        "classe": "Limite RBCV",
        "codigo": "RBCV_LIMITE",
        "esfera": "Internacional / Estadual",
        "orgao": "UNESCO / MaB / Conselho de Gestão da RBCV",
        "base_legal": "Decreto Estadual nº 47.094/2002, Programa MaB UNESCO (1994), LC nº 39/2006",
        "cor_hex": "#0F172A",
        "geometry": merged_limite
    }
], crs="EPSG:4326")

web_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_web.geojson"
gdf_unified.to_file(web_out, driver="GeoJSON")
print(f"  GeoJSON Unificado salvo: {web_out}")

gpkg_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde.gpkg"
gdf_nucleos.to_file(gpkg_out, layer="zonas_nucleo", driver="GPKG")
gdf_limite.to_file(gpkg_out, layer="limite_rbcv", driver="GPKG")
print(f"  GPKG salvo: {gpkg_out}")

print(f"\nREPROCESSAMENTO CONCLUÍDO COM SUCESSO!")
