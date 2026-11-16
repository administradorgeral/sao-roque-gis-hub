import json

with open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_nucleos_web.geojson", encoding="utf-8") as f:
    nucleos = json.load(f)

print(f"Total nucleo features: {len(nucleos['features'])}")

jaragua_features = []
cantareira_features = []

for feat in nucleos['features']:
    poly = feat['geometry']['coordinates']
    # flatten coordinates
    if feat['geometry']['type'] == 'MultiPolygon':
        pts = [p for part in poly for ring in part for p in ring]
    else:
        pts = [p for ring in poly for p in ring]
    
    avg_lon = sum(p[0] for p in pts) / len(pts)
    avg_lat = sum(p[1] for p in pts) / len(pts)
    
    # Jaraguá is around Lon -46.76, Lat -23.46
    if abs(avg_lon - (-46.76)) < 0.08 and abs(avg_lat - (-23.46)) < 0.08:
        print(f"Jaraguá polygon found: centroid=({avg_lon:.5f}, {avg_lat:.5f}), pts={len(pts)}")
    
    # Cantareira is around Lon -46.60, Lat -23.42
    if -46.70 <= avg_lon <= -46.50 and -23.48 <= avg_lat <= -23.35:
        print(f"Cantareira polygon found: centroid=({avg_lon:.5f}, {avg_lat:.5f}), pts={len(pts)}")
