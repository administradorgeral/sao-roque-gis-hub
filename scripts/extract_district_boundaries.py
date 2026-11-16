import json
import os

base_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub"
src_path = os.path.join(base_dir, "data", "distritos_sao_roque_web.geojson")

with open(src_path, "r", encoding="utf-8") as f:
    data = json.load(f)

distritos_map = {
    "São Roque": "distrito_sede_sao_roque.geojson",
    "Mailasqui": "distrito_maylasky_sao_roque.geojson",
    "São João Novo": "distrito_sao_joao_novo.geojson",
    "Canguera": "distrito_canguera.geojson"
}

print("=== EXTRAINDO CONTORNOS VETORIAIS INDIVIDUAIS DOS 4 DISTRITOS ===")
for feat in data["features"]:
    name = feat["properties"]["distrito"]
    if name in distritos_map:
        out_name = distritos_map[name]
        out_path = os.path.join(base_dir, "data", out_name)
        fc = {
            "type": "FeatureCollection",
            "crs": data.get("crs", {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}),
            "features": [feat]
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(fc, f, ensure_ascii=False, indent=2)
        print(f"Salvo: {out_name} - {feat['properties']['nome']} ({feat['properties']['area_km2']} km²)")

print("=== CONTORNOS EXTRAÍDOS COM SUCESSO ===")
