import geopandas as gpd
import time
import os
import json
from shapely import simplify

print("Reduzindo precisão de coordenadas para 5 decimais...", flush=True)
t0 = time.time()

gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.gpkg"
gdf = gpd.read_file(gpkg_path)
gdf_filtered = gdf[gdf['area_ha'] >= 0.12].copy()
print(f"Feições selecionadas: {len(gdf_filtered)}", flush=True)

gdf_filtered['geometry'] = simplify(gdf_filtered['geometry'].values, tolerance=5.0, preserve_topology=False)
gdf_wgs84 = gdf_filtered.to_crs("EPSG:4326")
gdf_wgs84['cor'] = gdf_wgs84['cor_hex']

# Exportar para GeoJSON com precisão de 5 decimais
out_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"

# Formatação direta de GeoJSON em json com 5 decimais
data = json.loads(gdf_wgs84.to_json())

def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in data['features']:
    if 'geometry' in feat and feat['geometry'] and 'coordinates' in feat['geometry']:
        feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])

with open(out_web, 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))

size_mb = os.path.getsize(out_web) / (1024 * 1024)
print(f"GeoJSON Web de Alta Precisão (5 decimais) salvo em {time.time()-t0:.2f}s: {size_mb:.2f} MB!", flush=True)
