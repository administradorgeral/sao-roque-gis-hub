import json
import geopandas as gpd
from shapely.affinity import translate

print("=== APLICANDO AJUSTE DE>PARA NA CAMADA RBCV (UNESCO) ===")

lat_de, lon_de = -23.66308, -46.94784
lat_para, lon_para = -23.65797, -46.93720

d_lat = lat_para - lat_de  # +0.00511
d_lon = lon_para - lon_de  # +0.01064

print(f"Ponto DE:   Lat {lat_de:.5f}, Lon {lon_de:.5f}")
print(f"Ponto PARA: Lat {lat_para:.5f}, Lon {lon_para:.5f}")
print(f"Vetor de Translação: d_lat = {d_lat:+.5f}, d_lon = {d_lon:+.5f}")

# 1. Atualizar GeoJSON rbcv_cinturao_verde_web.geojson
def shift_geojson(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    def shift_coords(coords):
        if not coords:
            return coords
        if isinstance(coords[0], (int, float)):
            # [lon, lat] or [lon, lat, elev]
            new_c = [round(coords[0] + d_lon, 6), round(coords[1] + d_lat, 6)]
            if len(coords) > 2:
                new_c.extend(coords[2:])
            return new_c
        return [shift_coords(sub) for sub in coords]

    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        gtype = geom.get("type")
        if gtype == "GeometryCollection":
            for sub_g in geom.get("geometries", []):
                sub_g["coordinates"] = shift_coords(sub_g.get("coordinates", []))
        elif "coordinates" in geom:
            geom["coordinates"] = shift_coords(geom["coordinates"])
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"  Atualizado: {file_path}")

geojson_files = [
    "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_web.geojson",
    "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_nucleos_web.geojson",
    "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_limite_web.geojson"
]

for gfile in geojson_files:
    shift_geojson(gfile)

# 2. Atualizar GPKG rbcv_cinturao_verde.gpkg
gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde.gpkg"
try:
    layers = ["rbcv_nucleos", "rbcv_limite"]
    for lyr in layers:
        gdf = gpd.read_file(gpkg_path, layer=lyr)
        gdf["geometry"] = gdf["geometry"].apply(lambda g: translate(g, xoff=d_lon, yoff=d_lat) if g else g)
        gdf.to_file(gpkg_path, layer=lyr, driver="GPKG")
        print(f"  GPKG layer '{lyr}' atualizada.")
except Exception as e:
    print(f"  Nota GPKG: {e}")

# 3. Calcular novos rasterBounds
current_bounds = [[-25.35882, -47.54622], [-22.44569, -45.31257]]
new_bounds = [
    [round(current_bounds[0][0] + d_lat, 5), round(current_bounds[0][1] + d_lon, 5)],
    [round(current_bounds[1][0] + d_lat, 5), round(current_bounds[1][1] + d_lon, 5)]
]
print(f"Novos rasterBounds: {new_bounds}")

# 4. Atualizar js/layers/rbcv_cinturao_verde.js
js_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/layers/rbcv_cinturao_verde.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Substituir rasterBounds e rasterUrl
import re
js_content = re.sub(
    r'rasterBounds:\s*\[\[.*?\],\s*\[.*?\]\]',
    f'rasterBounds: [[{new_bounds[0][0]}, {new_bounds[0][1]}], [{new_bounds[1][0]}, {new_bounds[1][1]}]]',
    js_content
)
js_content = re.sub(
    r'rasterUrl:\s*"data/rbcv_cinturao_verde_regional\.png(\?v=[^"]*)?"',
    'rasterUrl: "data/rbcv_cinturao_verde_regional.png?v=20261115_depara"',
    js_content
)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"  Atualizado: {js_path}")
print("=== SUCESSO NO AJUSTE DE>PARA ===")
