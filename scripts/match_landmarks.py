import json
import shapely.geometry

# Search in logradouros
with open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\logradouros_sao_roque_web.geojson", "r", encoding="utf-8") as f:
    d = json.load(f)

targets = ["SUN VALLEY", "LAS BRISAS", "VERA CRUZ", "BOQUEIRÃO", "MONT SERRAT", "CAMPININHA", "SUÍÇA", "PAVÃO"]

found = {}
for feat in d["features"]:
    nome = (feat["properties"].get("nome") or "").upper()
    for t in targets:
        if t in nome and t not in found:
            geom = shapely.geometry.shape(feat["geometry"])
            found[t] = (geom.centroid.x, geom.centroid.y)

for k, v in found.items():
    print(f"Landmark {k}: Lon={v[0]:.5f}, Lat={v[1]:.5f}")
