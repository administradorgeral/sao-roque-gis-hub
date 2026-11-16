import geopandas as gpd
import time
import os
import sys
from shapely import simplify

print("Iniciando exportação web ultra rápida...", flush=True)
t0 = time.time()

gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.gpkg"
gdf = gpd.read_file(gpkg_path)
print(f"[{time.time()-t0:.1f}s] Lidos {len(gdf)} registros do GPKG.", flush=True)

# 1. Manter feições com área >= 0.05 ha (500 m²) para eliminar ruídos de pixel
gdf_filtered = gdf[gdf['area_ha'] >= 0.05].copy()
print(f"[{time.time()-t0:.1f}s] Filtradas {len(gdf_filtered)} feições significativas (>= 500 m²).", flush=True)

# 2. Simplificar geometrias com tolerância de 3m (Douglas-Peucker linear rápido)
t1 = time.time()
gdf_filtered['geometry'] = simplify(gdf_filtered['geometry'].values, tolerance=3.0, preserve_topology=False)
print(f"[{time.time()-t0:.1f}s] Simplificação concluída em {time.time()-t1:.2f}s.", flush=True)

# 3. Reprojetar para WGS84
t2 = time.time()
gdf_wgs84 = gdf_filtered.to_crs("EPSG:4326")
print(f"[{time.time()-t0:.1f}s] Reprojeção WGS84 concluída em {time.time()-t2:.2f}s.", flush=True)

# 4. Adicionar propriedade 'cor' para compatibilidade total com LayerRegistry
gdf_wgs84['cor'] = gdf_wgs84['cor_hex']

# 5. Salvar GeoJSON Web Otimizado
out_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"
t3 = time.time()
gdf_wgs84.to_file(out_web, driver="GeoJSON")
size_mb = os.path.getsize(out_web) / (1024 * 1024)
print(f"[{time.time()-t0:.1f}s] GeoJSON Web salvo com sucesso em {time.time()-t3:.2f}s: {size_mb:.2f} MB ({len(gdf_wgs84)} feições).", flush=True)
