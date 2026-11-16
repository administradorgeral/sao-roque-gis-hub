import json

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"

with open(geojson_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for feat in data['features']:
    p = feat['properties']
    cor = p.get('cor_hex', '#FFAA00')
    classe = p.get('classe', '')
    
    alerta = ""
    if "Forte ondulado" in classe:
        alerta = "⚠️ ATENÇÃO: A Lei Federal 6.766/79 (Art. 3º) e a LC 40/2006 (Art. 13) PROÍBEM loteamentos acima de 30% de declividade. Esta classe agrupa 20% a 45%, exigindo laudo topográfico específico para comprovar rampa < 30%."
    elif "Montanhoso" in classe:
        alerta = "🚨 RISCO GEOTÉCNICO: Áreas com rampa > 100% (> 45°) são APPs inalienáveis pelo Código Florestal (Lei 12.651/12, Art. 4º, V)."
    elif "Ondulado" in classe:
        alerta = "ℹ️ CONDIÇÃO VIÁRIA: O Art. 32 da LC 40/2006 estabelece limite máximo de 15% para abertura de vias públicas."
    else:
        alerta = "✅ Área com baixa declividade natural, apta para edificação."

    feat['properties'] = {
        "nome": f"Declividade: {classe}",
        "classe": classe,
        "Classe de Relevo": p.get('relevo', ''),
        "Inclinação Angular Estimada": p.get('angulo_equivalente', ''),
        "Grau de Restrição Construtiva": p.get('grau_restricao', ''),
        "Base Legal Normativa": p.get('base_legal', ''),
        "Diretriz Técnica e Urbanística": p.get('implicacao', ''),
        "Área da Mancha Contígua": f"{p.get('area_ha', 0):.2f} ha ({int(p.get('area_ha', 0)*10000):,} m²)",
        "Alerta de Auditoria Jurídica": alerta,
        "Fonte Primária": "IGC 1:10.000 (Folhas 89 a 98, 1978) / PDA 2019",
        "Responsabilidade Técnica": "Eng. Maurício S. Sartori (CREA 5.060.532.187) / Ana C. Cerminaro (CREA 473.423.455)",
        "cor_hex": cor,
        "cor": cor
    }

with open(geojson_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, separators=(',', ':'))

print(f"Propriedades amigáveis e jurídicas atualizadas em {len(data['features'])} feições!")
