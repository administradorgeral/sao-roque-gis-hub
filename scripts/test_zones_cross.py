import json
from shapely.geometry import shape

with open('data/pmsr_zoneamento_pmd2006.geojson', 'r', encoding='utf-8') as f:
    z06 = json.load(f)
with open('data/pmsr_zoneamento_minuta_pmd2006.geojson', 'r', encoding='utf-8') as f:
    z26 = json.load(f)

geoms_06 = []
for f in z06['features']:
    props = f['properties']
    sigla = props.get('sigla') or props.get('zona') or 'ND'
    geoms_06.append({
        'geom': shape(f['geometry']),
        'sigla': sigla,
        'props': props
    })

print("Testing intersection of 2026 features with 2006 zones...")
for i, f in enumerate(z26['features']):
    props26 = f['properties']
    g26 = shape(f['geometry'])
    nome26 = props26.get('nome')
    sigla26 = props26.get('sigla_zoneamento')
    area_ha = props26.get('area_ha')

    # Find 2006 zones intersecting
    intersections = []
    for g06 in geoms_06:
        if g26.intersects(g06['geom']):
            inter = g26.intersection(g06['geom'])
            if inter.area > 1e-7: # significant
                pct = (inter.area / g26.area) * 100
                intersections.append((g06['sigla'], pct))
    
    inter_str = ", ".join([f"{sig} ({pct:.1f}%)" for sig, pct in intersections])
    print(f"[{i+1}] {nome26} ({area_ha} ha) <- 2006: {inter_str}")
