import json

json_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rol_legislacao_territorial.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Novas leis a adicionar no catálogo frontend
novas_leis_estadual = [
    {
        "id": "CE_SP_ART146",
        "tipo": "Constituição Estadual",
        "numero": "Artigo 146",
        "ano": 1989,
        "ementa": "Institui o Fundo de Melhoria das Estâncias (DADETUR/FUMEST), assegurando dotação anual a fundo perdido para obras de infraestrutura turística nas Estâncias Paulistas.",
        "link_oficial": "https://www.al.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "🏛️ Fundo das Estâncias (DADETUR)",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL", "ZUE-DT", "ZR"]
    },
    {
        "id": "LEI_EST_6899",
        "tipo": "Lei Estadual Ordinária",
        "numero": "6.899",
        "ano": 1990,
        "ementa": "Transforma em Estância Turística o Município de São Roque, outorgando prerrogativas, repasses e regime jurídico especial.",
        "link_oficial": "https://www.al.sp.gov.br/norma/39414",
        "ambito_territorial": "Território Municipal Integral (30.701,47 ha)",
        "tag_ambito": "⭐ Criação da Estância Turística",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL"]
    },
    {
        "id": "LCE_1261",
        "tipo": "Lei Complementar Estadual",
        "numero": "1.261",
        "ano": 2015,
        "ementa": "Estabelece condições e requisitos para as Estâncias Paulistas: exigência de Plano Diretor de Turismo (PDTur) revisado a cada 3 anos, COMTUR deliberativo ativo e ranqueamento trienal da ALESP.",
        "link_oficial": "https://www.al.sp.gov.br/norma/174987",
        "ambito_territorial": "Território Municipal Integral (30.701,47 ha)",
        "tag_ambito": "📜 Lei-Matriz das Estâncias (LCE 1.261/15)",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL", "ZUE-DT", "ZUE-CM"]
    },
    {
        "id": "DEC_EST_65415",
        "tipo": "Decreto Estadual",
        "numero": "65.415",
        "ano": 2020,
        "ementa": "Regulamenta as transferências e convênios do DADETUR com as Estâncias Turísticas, exigindo aprovação prévia do COMTUR e projeto executivo.",
        "link_oficial": "https://www.al.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "💼 Convênios DADETUR",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL"]
    }
]

novas_leis_municipal = [
    {
        "id": "LEI_ORG_1801",
        "tipo": "Lei Orgânica Municipal",
        "numero": "1.801",
        "ano": 1990,
        "ementa": "Lei Orgânica do Município da Estância Turística de São Roque: institui a autonomia local, o título jurídico de Estância e a compatibilização orçamentária do turismo.",
        "link_oficial": "https://camarasaoroque.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (30.701,47 ha)",
        "tag_ambito": "🏛️ Lei Orgânica Municipal",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL"]
    },
    {
        "id": "LC_MUN_94",
        "tipo": "Lei Complementar Municipal",
        "numero": "94",
        "ano": 2018,
        "ementa": "Institui o Plano Diretor de Desenvolvimento Turístico da Estância Turística de São Roque (PDTur decênio 2018-2028), em cumprimento à LCE nº 1.261/2015.",
        "link_oficial": "https://camarasaoroque.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "🗺️ PDTur Decenal (LC 94/18)",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL", "ZUE-DT"]
    },
    {
        "id": "LC_MUN_140",
        "tipo": "Lei Complementar Municipal",
        "numero": "140",
        "ano": 2025,
        "ementa": "Revisão e Atualização Trienal do Plano Diretor de Desenvolvimento Turístico de São Roque (PDTur), fixando metas trienais, rotas e projetos de infraestrutura DADETUR 2025-2028.",
        "link_oficial": "https://camarasaoroque.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "🌟 PDTur Atualizado (LC 140/25)",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL", "ZUE-DT", "ZR", "POLIGONO_APA"]
    },
    {
        "id": "LEI_MUN_2871",
        "tipo": "Lei Ordinária Municipal",
        "numero": "2.871",
        "ano": 2004,
        "ementa": "Reestrutura o Conselho Municipal de Turismo (COMTUR), conferindo caráter consultivo e deliberativo para aprovação obrigatória de convênios DADETUR.",
        "link_oficial": "https://camarasaoroque.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "👥 COMTUR Deliberativo",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL"]
    },
    {
        "id": "LEI_MUN_4872",
        "tipo": "Lei Ordinária Municipal",
        "numero": "4.872",
        "ano": 2018,
        "ementa": "Dispõe sobre a obrigatoriedade da presença de Guia de Turismo Regional Cadastur acompanhando grupos e excursões que visitam os atrativos de São Roque.",
        "link_oficial": "https://camarasaoroque.sp.gov.br",
        "ambito_territorial": "Território Municipal Integral (São Roque)",
        "tag_ambito": "🛡️ Poder de Polícia Turística (Guias Cadastur)",
        "zonas_afetadas": ["TERRITORIO_MUNICIPAL", "ZUE-DT"]
    }
]

existing_ids_est = [x.get("id") for x in data["leis"].get("estadual", [])]
for l in novas_leis_estadual:
    if l["id"] not in existing_ids_est:
        data["leis"]["estadual"].append(l)

existing_ids_mun = [x.get("id") for x in data["leis"].get("municipal", [])]
for l in novas_leis_municipal:
    if l["id"] not in existing_ids_mun:
        data["leis"]["municipal"].append(l)

data["total_leis_catalogo"] = len(data["leis"].get("municipal", [])) + len(data["leis"].get("estadual", [])) + len(data["leis"].get("federal", []))

if "zonas_parametros" in data:
    data["zonas_parametros"]["TERRITORIO_MUNICIPAL"] = {
        "sigla": "São Roque (Estância)",
        "denominacao": "Município da Estância Turística de São Roque (30.701,47 ha)",
        "esfera": "Municipal / Estadual",
        "lei_regente": "Lei Orgânica Municipal nº 1.801/90, Lei Estadual nº 6.899/90 e LCE nº 1.261/15",
        "diretriz_principal": "Regime jurídico-administrativo diferenciado de Estância Turística. Obrigação de PDTur revisado a cada 3 anos (LC 140/25), COMTUR deliberativo (Lei 2.871/04), recursos DADETUR/FUMEST carimbados para investimentos de capital e proteção da vocação enoturística e cênica.",
        "taxa_permeabilidade_min": "Variável por zona (mínimo de 15% nas zonas urbanas e até 70% nas áreas de manancial e proteção ambiental)",
        "lote_minimo_m2": "Conforme LC 40/06 (150m² a 1.000m² em zona urbana; 1.000m² a 20.000m² em manancial/ZUE; 20.000m² módulo fiscal rural)"
    }

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Catálogo {json_path} atualizado com sucesso. Total de leis: {data['total_leis_catalogo']}")
