import json

with open('data/setores_censitarios_sao_roque_web.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

for feat in data['features']:
    props = feat['properties']
    cd = props.get('cd_setor', '')
    dist = props.get('distrito', '')
    sit = props.get('situacao', '')
    props['nome'] = f"Setor {cd} ({dist} - {sit})"

with open('data/setores_censitarios_sao_roque_web.geojson', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {len(data['features'])} setores censitários with 'nome'")
