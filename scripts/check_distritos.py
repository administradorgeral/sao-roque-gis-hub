import json
import shapely.geometry

with open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\distritos_sao_roque_web.geojson", "r", encoding="utf-8") as f:
    d = json.load(f)

for feat in d["features"]:
    geom = shapely.geometry.shape(feat["geometry"])
    print(feat["properties"]["nome"], "-> Bounding Box WGS84:", geom.bounds)
