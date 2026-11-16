import json

json_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rol_legislacao_territorial.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

estadual_list = data["leis"].get("estadual", [])

existing_ids = [item.get("id") for item in estadual_list]

new_laws = [
    {
        "id": "LEI_11579_SP",
        "tipo": "Lei Estadual Ordinária",
        "numero": "11.579",
        "ano": 2003,
        "ementa": "Cria a Área de Proteção Ambiental da Represa de Itupararanga (APA Itupararanga), abrangendo a bacia formadora do reservatório e definindo sua poligonal territorial.",
        "link_oficial": "https://www.al.sp.gov.br/norma/39414",
        "ambito_territorial": "Região Sul de São Roque (10.805,84 ha / 35,19% do território municipal)",
        "tag_ambito": "🌊 APA Itupararanga (Lei 11.579/03)",
        "zonas_afetadas": ["POLIGONO_APA", "LIMITE_NORTE_APA", "ZPHID_RUR", "ZPHID_SEN", "ZPBIO", "ZUE-Chacaras em Manancial"]
    },
    {
        "id": "DEC_52879_SP",
        "tipo": "Decreto Estadual",
        "numero": "52.879",
        "ano": 2008,
        "ementa": "Regulamenta a APA da Represa de Itupararanga, cria o Conselho Gestor e aprova as diretrizes normativas para o Plano de Manejo da unidade de conservação.",
        "link_oficial": "https://www.al.sp.gov.br/norma/84687",
        "ambito_territorial": "APA Itupararanga (Território Sul de São Roque)",
        "tag_ambito": "📜 Plano de Manejo APA Itupararanga",
        "zonas_afetadas": ["POLIGONO_APA", "LIMITE_NORTE_APA", "ZPHID_RUR", "ZPHID_SEN"]
    }
]

added = 0
for nl in new_laws:
    if nl["id"] not in existing_ids:
        estadual_list.append(nl)
        added += 1

data["leis"]["estadual"] = estadual_list
data["total_leis_catalogo"] = len(data["leis"].get("municipal", [])) + len(estadual_list) + len(data["leis"].get("federal", []))

# Also add zone params if needed
if "zonas_parametros" in data:
    data["zonas_parametros"]["POLIGONO_APA"] = {
        "sigla": "APA Itupararanga",
        "denominacao": "Área de Proteção Ambiental da Represa de Itupararanga (10.805 ha)",
        "esfera": "Estadual",
        "lei_regente": "Lei Estadual nº 11.579/2003 e Decreto Estadual nº 52.879/2008",
        "diretriz_principal": "Proteção integral de mananciais hídricos que abastecem Sorocaba e região. Parcelamento condicionado a diretrizes estaduais da Fundação Florestal e Lei 9.866/97.",
        "taxa_permeabilidade_min": "0.50 (50% a 70% conforme subzona do Plano de Manejo)",
        "lote_minimo_m2": "1.000m² a 20.000m² dependendo do enquadramento de manancial"
    }
    data["zonas_parametros"]["LIMITE_NORTE_APA"] = {
        "sigla": "Limite Norte APA",
        "denominacao": "Linha Divisória de Águas Setentrional da Bacia de Itupararanga (18,59 km)",
        "esfera": "Estadual",
        "lei_regente": "Lei Estadual nº 11.579/2003 (Art. 2º)",
        "diretriz_principal": "Delimitação física e jurídica que separa a vertente do Rio Tietê (ao norte) da vertente da Represa de Itupararanga (ao sul)."
    }

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {json_path}. Added {added} laws. Total laws now: {data['total_leis_catalogo']}")
