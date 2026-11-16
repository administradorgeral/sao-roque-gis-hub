import geopandas as gpd
import time
import os
import sys
import json
from shapely import simplify

print("Otimizando GeoJSON para carregamento instantâneo no navegador...", flush=True)
t0 = time.time()

gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.gpkg"
gdf = gpd.read_file(gpkg_path)

# 1. Feições com área >= 0.1 ha (1.000 m²)
gdf_filtered = gdf[gdf['area_ha'] >= 0.10].copy()
print(f"Feições com área >= 1.000 m²: {len(gdf_filtered)}", flush=True)

# 2. Simplificação com 4 metros (0.08 mm na escala 1:50.000)
gdf_filtered['geometry'] = simplify(gdf_filtered['geometry'].values, tolerance=4.0, preserve_topology=False)

# 3. Reprojeção WGS84
gdf_wgs84 = gdf_filtered.to_crs("EPSG:4326")
gdf_wgs84['cor'] = gdf_wgs84['cor_hex']

out_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"
gdf_wgs84.to_file(out_web, driver="GeoJSON")
size_mb = os.path.getsize(out_web) / (1024 * 1024)
print(f"GeoJSON Web otimizado: {size_mb:.2f} MB ({len(gdf_wgs84)} feições) gerado em {time.time()-t0:.2f}s!", flush=True)
