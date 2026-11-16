import geopandas as gpd
import json
import os
import time

print("=== OTIMIZAÇÃO WEB DA CAMADA AHS ===")
t0 = time.time()

gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/ahs_sao_roque.gpkg"
gdf_utm = gpd.read_file(gpkg_path)

print(f"Features: {len(gdf_utm)}")
orig_area = gdf_utm.geometry.area.sum() / 10000.0

# Simplificar em UTM com tolerância de 2.0 metros (0.05 mm na escala do mapa 1:35.000)
print("Simplificando geometria em UTM 23S com tolerância de 2.0 metros...")
gdf_simp = gdf_utm.copy()
gdf_simp['geometry'] = gdf_utm.geometry.simplify(tolerance=2.0, preserve_topology=True)
simp_area = gdf_simp.geometry.area.sum() / 10000.0

diff_ha = abs(orig_area - simp_area)
pct_diff = (diff_ha / orig_area) * 100
print(f"Área original: {orig_area:.2f} ha | Área simplificada: {simp_area:.2f} ha | Diferença: {diff_ha:.2f} ha ({pct_diff:.3f}%)")

# Converter para WGS84
gdf_wgs84 = gdf_simp.to_crs(epsg=4326)

out_geojson = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/ahs_sao_roque_web.geojson"
geojson_dict = json.loads(gdf_wgs84.to_json())

def round_coords(geom):
    if geom['type'] == 'Polygon':
        geom['coordinates'] = [[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in geom['coordinates']]
    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [[[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in poly] for poly in geom['coordinates']]

for f in geojson_dict['features']:
    round_coords(f['geometry'])

with open(out_geojson, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False)

sz_mb = os.path.getsize(out_geojson) / (1024 * 1024)
print(f"Tamanho final do GeoJSON Web Otimizado: {sz_mb:.2f} MB em {time.time()-t0:.2f}s")
