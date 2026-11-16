import json
from shapely.geometry import shape

with open('data/pmsr_zoneamento_pmd2006.geojson', 'r', encoding='utf-8') as f:
    z06 = json.load(f)
with open('data/pmsr_zoneamento_minuta_pmd2006.geojson', 'r', encoding='utf-8') as f:
    z26 = json.load(f)

print("2006 features count:", len(z06['features']))
print("2026 features count:", len(z26['features']))

for i, f in enumerate(z26['features']):
    props = f['properties']
    geom = shape(f['geometry'])
    bounds = geom.bounds
    print(f"[{i+1}] FID: {props.get('fid')} | Nome: {props.get('nome')} | Sigla: {props.get('sigla_zoneamento')} | Area_ha: {props.get('area_ha')} | Bounds: {bounds}")
