import json
import os

base_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data"
files = [
    "declividade_sao_roque_web.geojson",
    "hidrografia_sao_roque_web.geojson",
    "vegetacao_arborea_sao_roque_web.geojson",
    "mdt_sao_roque_web.geojson",
    "ahs_sao_roque_web.geojson"
]

for fname in files:
    fpath = os.path.join(base_dir, fname)
    if os.path.exists(fpath):
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                d = json.load(fp)
            feats = d.get("features", [])
            count = len(feats)
            if count > 0:
                first_props = feats[0].get("properties", {})
                print(f"FILE: {fname} (total {count} features)")
                print(f"  KEYS: {list(first_props.keys())}")
                print(f"  SAMPLE: {first_props}\n")
            else:
                print(f"FILE: {fname} (EMPTY)\n")
        except Exception as e:
            print(f"FILE: {fname} ERROR: {e}\n")
