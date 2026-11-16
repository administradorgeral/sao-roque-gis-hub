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

print("=== REPROCESSAMENTO CALIBRADO DA RBCV (UNESCO 2019) COM GCPs EMPÍRICOS ===")

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# 1. Calibração empírica por Mínimos Quadrados com 10 Pontos de Controle Terrestre (GCPs):
# São Roque, Cotia, Vargem Grande, Itapevi, Jandira, Barueri, Osasco, São Paulo Sé, Guarulhos e Ilha Porchat
# No sistema de pixels da imagem regional (2222 x 2946 px):
# Lon = 0.00100524 * px - 47.54621820
# Lat = -0.00098884 * py - 22.44568650
opt_bounds = [[-25.35882, -47.54622], [-22.44569, -45.31257]]
print(f"Novos Bounds Calibrados para Leaflet ImageOverlay: {opt_bounds}")

# 2. Renderizar e Salvar Raster Regional em 300 DPI
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

# 3. Conversão de Coordenadas do PDF (pt) para WGS84
def pt_to_geo(px, py):
    pixel_x = (px - x_min) * scale
    pixel_y = (y_max - py) * scale
    lon = 0.00100524 * pixel_x - 47.54621820
    lat = -0.00098884 * pixel_y - 22.44568650
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

print(f"  Zonas-Núcleo extraídas: {len(nucleos_polygons)} polígonos")
print(f"  Limite RBCV: {len(limite_lines)} segmentos de linha")

union_nucleos = unary_union(nucleos_polygons)
merged_limite = linemerge(limite_lines)

# 4. Gravar GeoJSONs
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

gpkg_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde.gpkg"
gdf_nucleos.to_file(gpkg_out, layer="zonas_nucleo", driver="GPKG")
gdf_limite.to_file(gpkg_out, layer="limite_rbcv", driver="GPKG")

print("REPROCESSAMENTO CALIBRADO CONCLUÍDO COM SUCESSO!")
