import geopandas as gpd
import time
import os
from shapely import simplify

print("Testando consolidação em 5 MultiPolígonos por classe...")
t0 = time.time()
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.gpkg"

# Carregar do GPKG que já tem todas as geometrias prontas
gdf = gpd.read_file(gpkg_path)
print(f"Lidos {len(gdf)} registros em {time.time()-t0:.2f}s")

# Dissolver por classe
t1 = time.time()
dissolved = gdf.dissolve(by="codigo_classe", as_index=False)
print(f"Dissolvido em {len(dissolved)} MultiPolígonos em {time.time()-t1:.2f}s")

# Testar simplificação leve para WebGIS (tolerância de 5m em UTM SIRGAS 2000)
# Na escala 1:50.000, 5 metros = 0.1 milímetro no papel (abaixo da resolução do traçado!)
dissolved["geometry"] = dissolved["geometry"].apply(lambda g: simplify(g, tolerance=5.0, preserve_topology=True))

# Reprojetar para WGS84
dissolved_wgs84 = dissolved.to_crs("EPSG:4326")

out_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"
dissolved_wgs84.to_file(out_web, driver="GeoJSON")
size_kb = os.path.getsize(out_web) / 1024
print(f"GeoJSON Web Otimizado salvo em {time.time()-t0:.2f}s: {size_kb:.1f} KB!")

for idx, row in dissolved.iterrows():
    print(f"  Classe: {row['classe']} | Área: {row.geometry.area / 10000.0:.2f} ha | Vértices: {len(row.geometry.exterior.coords) if row.geometry.geom_type == 'Polygon' else sum(len(p.exterior.coords) for p in row.geometry.geoms)}")
