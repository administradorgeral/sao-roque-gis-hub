import json

json_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rol_legislacao_territorial.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

novas_leis_federal = [
    {
        "id": "LEI_FED_7565",
        "tipo": "Lei Federal Ordinária",
        "numero": "7.565",
        "ano": 1986,
        "ementa": "Código Brasileiro de Aeronáutica (CBA) - Arts. 43 a 47: Servidões Aeronáuticas, Zonas de Proteção (PBZPA/PBZR), vinculação obrigatória do Plano Diretor e demolição sumária de obstáculos aéreos sem indenização.",
        "link_oficial": "https://www.planalto.gov.br/ccivil_03/leis/l7565.htm",
        "ambito_territorial": "Entorno do Aeroporto Catarina / ZUCAer / Eixo Castello Branco",
        "tag_ambito": "✈️ Servidão Aeronáutica (CBA - Lei 7.565/86)",
        "zonas_afetadas": ["ZUCAer", "ZDES_CB", "PBZPA_CONE_SLO", "ASA_20KM_SAO_ROQUE"]
    },
    {
        "id": "LEI_FED_12725",
        "tipo": "Lei Federal Ordinária",
        "numero": "12.725",
        "ano": 2012,
        "ementa": "Dispõe sobre o gerenciamento do risco da fauna nas vizinhanças de aeródromos (perigo aviário): cria a ASA de raio 20 km e veda lixões, abatedouros e atrativos de aves.",
        "link_oficial": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12725.htm",
        "ambito_territorial": "Área de Segurança Aeroportuária (21.648 ha / 70,5% de São Roque)",
        "tag_ambito": "🦅 Área de Segurança Aeroportuária (ASA 20 km)",
        "zonas_afetadas": ["ASA_20KM_SAO_ROQUE", "ZUCAer", "TERRITORIO_MUNICIPAL"]
    },
    {
        "id": "ICA_11_408",
        "tipo": "Instrução Militar / DECEA",
        "numero": "ICA 11-408",
        "ano": 2020,
        "ementa": "Regulamenta os Planos Básicos de Zona de Proteção de Aeródromos (PBZPA), Superfícies Limitadoras de Obstáculos (SLO) e Anuência Prévia SYSAGA/OPEA para gabaritos e construções no cone de aproximação.",
        "link_oficial": "https://publicacoes.decea.mil.br",
        "ambito_territorial": "Cone de Aproximação da Pista 13/31 (Aeroporto Catarina)",
        "tag_ambito": "📐 Controle de Gabarito (DECEA / SLO)",
        "zonas_afetadas": ["PBZPA_CONE_SLO", "ZUCAer"]
    },
    {
        "id": "RBAC_161",
        "tipo": "Regulamento ANAC",
        "numero": "RBAC nº 161",
        "ano": 2021,
        "ementa": "Planos de Zoneamento de Ruído (PZR): veda habitações, escolas e hospitais sob as curvas de ruído aeronáutico DNL 65 e 75, direcionando o uso do solo para logística e indústria.",
        "link_oficial": "https://www.anac.gov.br",
        "ambito_territorial": "Corredor Acústico Aeroporto Catarina (km 60-64 Castello Branco)",
        "tag_ambito": "🔇 Zoneamento de Ruído Aeronáutico (PZR)",
        "zonas_afetadas": ["PBZPA_CONE_SLO", "ZUCAer", "ZDES_CB"]
    }
]

existing_fed_ids = [x.get("id") for x in data["leis"].get("federal", [])]
for lf in novas_leis_federal:
    if lf["id"] not in existing_fed_ids:
        data["leis"]["federal"].append(lf)

data["total_leis_catalogo"] = len(data["leis"].get("municipal", [])) + len(data["leis"].get("estadual", [])) + len(data["leis"].get("federal", []))

if "zonas_parametros" in data:
    data["zonas_parametros"]["ZUCAer"] = {
        "sigla": "ZUCAer",
        "denominacao": "Zona de Uso Controlado Aeroportuário (Polo Catarina)",
        "esfera": "Municipal / Federal",
        "lei_regente": "LC Municipal nº 40/2006, LC nº 65/2012, Lei Federal nº 7.565/1986 e ICA 11-408",
        "diretriz_principal": "Uso compatível com infraestrutura aeroportuária executiva internacional. Loteamentos residenciais e escolas vedados sob o cone de ruído (RBAC 161). Gabarito máximo de 100m submetido a aprovação prévia do DECEA (SYSAGA/OPEA).",
        "taxa_permeabilidade_min": "0.30 (30%)",
        "lote_minimo_m2": "1.000m² a 5.000m² para polos industriais e logísticos"
    }
    data["zonas_parametros"]["PBZPA_CONE_SLO"] = {
        "sigla": "PBZPA / SLO",
        "denominacao": "Cone de Proteção e Ruído das Pistas 13/31 (SBJH)",
        "esfera": "Federal (DECEA / COMAER / ANAC)",
        "lei_regente": "Lei Federal nº 7.565/1986 (Arts. 43 a 46), ICA 11-408 e RBAC 161",
        "diretriz_principal": "Servidão administrativa aeronáutica. Qualquer edificação, antena ou poste que ultrapasse as superfícies limitadoras de obstáculos é passível de embargo e demolição sumária sem indenização."
    }
    data["zonas_parametros"]["ASA_20KM_SAO_ROQUE"] = {
        "sigla": "ASA (20 km)",
        "denominacao": "Área de Segurança Aeroportuária - Raio 20 km (21.648 ha)",
        "esfera": "Federal (Presidência da República / ANAC)",
        "lei_regente": "Lei Federal nº 12.725/2012 e RBAC 153 (ANAC)",
        "diretriz_principal": "Gerenciamento de risco aviário (bird strike). Proibição expressa de lixões, aterros a céu aberto, abatedouros e atividades atrativas de aves num raio de 20 km da pista do aeroporto."
    }

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Catálogo {json_path} atualizado. Total de leis no catálogo: {data['total_leis_catalogo']}")
