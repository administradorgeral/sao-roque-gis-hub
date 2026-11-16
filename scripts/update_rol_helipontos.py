import json

json_path = "data/rol_legislacao_territorial.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

novas_leis_federal = [
    {
        "id": "PORTARIA_176_DGCEA_2014",
        "tipo": "Portaria DECEA",
        "numero": "Portaria 176/DGCEA",
        "ano": 2014,
        "ementa": "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto Vila Don Patto (SWVD), Estrada do Vinho km 2,5. Impõe servidão administrativa sobre terrenos vizinhos e controle rígido de gabarito nas rampas de aproximação.",
        "link_oficial": "https://sysaga.decea.mil.br/portaria-portal/17990",
        "ambito_territorial": "Estrada do Vinho km 2,5 / Roteiro do Vinho (Canguera)",
        "tag_ambito": "🚁 Heliponto Vila Don Patto (SWVD)",
        "zonas_afetadas": ["PZPH_SWVD", "FATO_SWVD", "ZUE-DT", "ZR"]
    },
    {
        "id": "PORTARIA_394_ICA_2018",
        "tipo": "Portaria DECEA / ICA",
        "numero": "Portaria 394/ICA",
        "ano": 2018,
        "ementa": "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto Taxaquara Golf Club (SIZT), Condomínio Vila Darcy Penteado. Restringe altura de imóveis residenciais, postes e árvores no cone de aproximação.",
        "link_oficial": "https://sysaga.decea.mil.br/portaria-portal/18926",
        "ambito_territorial": "Estrada Darcy Penteado / Bairro Taxaquara",
        "tag_ambito": "🚁 Heliponto Taxaquara (SIZT)",
        "zonas_afetadas": ["PZPH_SIZT", "FATO_SIZT", "ZR"]
    },
    {
        "id": "PORTARIA_1465_SAGA_2023",
        "tipo": "Portaria DECEA / SAGA",
        "numero": "Portaria 1465/SAGA",
        "ano": 2023,
        "ementa": "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto NÓR Hotel & Spa, Estrada do Pessegueiro nº 1.000. Protege o funil de pouso e subida de helicópteros executivos conectando São Paulo ao resort.",
        "link_oficial": "https://sysaga.decea.mil.br/portaria-portal/25568",
        "ambito_territorial": "Estrada do Pessegueiro / Bairro Gabriel Piza",
        "tag_ambito": "🚁 Heliponto NÓR Hotel & Spa",
        "zonas_afetadas": ["PZPH_NOR", "FATO_NOR", "ZR", "ZUE-DT"]
    },
    {
        "id": "PORTARIA_28_ICA_2015",
        "tipo": "Portaria DECEA / ICA",
        "numero": "Portaria 28/ICA",
        "ano": 2015,
        "ementa": "Aprova o PBZPA de Congonhas (SBSP): Superfície Horizontal Externa (SHE) de raio 45 km e proteção de auxílios à navegação aérea (PZANA) da Terminal São Paulo sobre 10.603 ha (34,5%) do leste de São Roque.",
        "link_oficial": "https://sysaga.decea.mil.br/portaria-portal/18751",
        "ambito_territorial": "Setor Leste de São Roque (Serras do Saboó e Cruzeiro / Divisa Cotia)",
        "tag_ambito": "✈️ Congonhas SHE (SBSP 45km / TMA-SP)",
        "zonas_afetadas": ["SHE_SBSP_CONGONHAS", "ZR", "ZUPA"]
    },
    {
        "id": "RBAC_155_ANAC",
        "tipo": "Regulamento ANAC",
        "numero": "RBAC nº 155",
        "ano": 2018,
        "ementa": "Requisitos para Projeto, Operação e Segurança de Helipontos: dimensões mínimas de FATO/TLOF, rampas de aproximação (8% a 12,5%) e faixas de segurança livres de qualquer obstáculo físico.",
        "link_oficial": "https://www.anac.gov.br",
        "ambito_territorial": "Todos os Helipontos Homologados de São Roque",
        "tag_ambito": "🚁 Helipontos (RBAC 155 / ANAC)",
        "zonas_afetadas": ["PZPH_SWVD", "PZPH_SIZT", "PZPH_NOR"]
    }
]

existing_ids = [x.get("id") for x in data["leis"].get("federal", [])]
for lf in novas_leis_federal:
    if lf["id"] not in existing_ids:
        data["leis"]["federal"].append(lf)

data["total_leis_catalogo"] = len(data["leis"].get("municipal", [])) + len(data["leis"].get("estadual", [])) + len(data["leis"].get("federal", []))

# Adicionar parâmetros de zonas para os helipontos e Congonhas
if "zonas_parametros" not in data:
    data["zonas_parametros"] = {}

data["zonas_parametros"]["PZPH_SWVD"] = {
    "sigla": "PZPH_SWVD",
    "denominacao": "Plano de Zona de Proteção de Heliponto - Vila Don Patto (SWVD)",
    "esfera": "Federal (DECEA / ANAC)",
    "lei_regente": "Portaria 176/DGCEA/2014, Lei Federal 7.565/86 (CBA) e ICA 11-408",
    "diretriz_principal": "Servidão aeronáutica compulsória com raio de 1.000m e rampas de descida de 8% a 12,5%. Vedada qualquer edificação, antena ou poste que perfure a rampa no Roteiro do Vinho.",
    "taxa_permeabilidade_min": "Conforme zona subjacente",
    "lote_minimo_m2": "Alvará municipal condicionado à certidão prévia no SYSAGA/DECEA"
}

data["zonas_parametros"]["PZPH_SIZT"] = {
    "sigla": "PZPH_SIZT",
    "denominacao": "Plano de Zona de Proteção de Heliponto - Taxaquara Golf Club (SIZT)",
    "esfera": "Federal (DECEA / ANAC)",
    "lei_regente": "Portaria 394/ICA/2018, Lei Federal 7.565/86 (CBA) e ICA 11-408",
    "diretriz_principal": "Proteção do cone de aproximação de helicópteros no Condomínio Vila Darcy Penteado. Demolição sem indenização caso erguido obstáculo não autorizado pelo DECEA.",
    "taxa_permeabilidade_min": "Conforme zona subjacente",
    "lote_minimo_m2": "Gabarito restrito com aprovação do DECEA"
}

data["zonas_parametros"]["PZPH_NOR"] = {
    "sigla": "PZPH_NOR",
    "denominacao": "Plano de Zona de Proteção de Heliponto - NÓR Hotel & Spa",
    "esfera": "Federal (DECEA / ANAC)",
    "lei_regente": "Portaria 1465/SAGA/2023, Lei Federal 7.565/86 (CBA) e ICA 11-408",
    "diretriz_principal": "Zona de proteção com raio de 1.000m na Estrada do Pessegueiro. Rota de conexão executiva com São Paulo. Controle rigoroso de fiação elétrica e torres de rádio.",
    "taxa_permeabilidade_min": "Conforme zona subjacente",
    "lote_minimo_m2": "Processo OPEA compulsório perante o DECEA"
}

data["zonas_parametros"]["SHE_SBSP_CONGONHAS"] = {
    "sigla": "SHE_SBSP_CONGONHAS",
    "denominacao": "Superfície Horizontal Externa de Congonhas (SBSP 45km / TMA-SP)",
    "esfera": "Federal (DECEA / ANAC)",
    "lei_regente": "Portaria 28/ICA/2015, Lei Federal 7.565/86 (CBA Arts. 44-45) e ICA 63-19",
    "diretriz_principal": "Abrange 10.603,80 ha (34,54%) no leste de São Roque. Restringe torres de telecomunicações nos cumes montanhosos (Saboó e Cruzeiro) para proteger feixes de rádio e fixos de rota IFR da Terminal São Paulo.",
    "taxa_permeabilidade_min": "Conforme zona subjacente",
    "lote_minimo_m2": "Instalação de torres e parques eólicos depende de anuência do IV COMAR / DECEA"
}

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Sucesso! rol_legislacao_territorial.json atualizado:")
print(f"  Total de leis no catálogo: {data['total_leis_catalogo']}")
print(f"  Leis federais cadastradas: {len(data['leis']['federal'])}")
