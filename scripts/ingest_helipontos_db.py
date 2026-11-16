import sqlite3

db_path = "dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Normas Jurídicas Aeronáuticas
normas = [
    (
        "portaria_176_dgcea_2014",
        "Federal",
        "Portaria",
        "176",
        2014,
        "Comando da Aeronáutica / DGCEA",
        "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto Vila Don Patto (SWVD) no município de São Roque (SP).",
        "Vigente",
        "https://sysaga.decea.mil.br/portaria-portal/17990",
        "PZPH_SWVD_Portaria_176_DGCEA.pdf",
        "Institui as superfícies limitadoras de obstáculos e rampas de aproximação/subida (inclinações de 8% a 12,5%) para o heliponto privado homologado SWVD, no km 2,5 da Estrada do Vinho. Impõe servidão administrativa sobre terrenos lindeiros, subordinando alvarás municipais à aprovação no SYSAGA/DECEA.",
        "zona_protecao_aeroportuaria_catarina"
    ),
    (
        "portaria_394_ica_2018",
        "Federal",
        "Portaria",
        "394",
        2018,
        "Comando da Aeronáutica / Instituto de Cartografia Aeronáutica (ICA)",
        "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto Taxaquara Golf Club (SIZT) no município de São Roque (SP).",
        "Vigente",
        "https://sysaga.decea.mil.br/portaria-portal/18926",
        "PZPH_SIZT_Portaria_394_ICA.pdf",
        "Institui superfícies de aproximação, subida e transição para o heliponto privado homologado SIZT no Condomínio Residencial Vila Darcy Penteado. Impõe limite de altura para edificações residenciais, postes de iluminação e vegetação arbórea no entorno.",
        "zona_protecao_aeroportuaria_catarina"
    ),
    (
        "portaria_1465_saga_2023",
        "Federal",
        "Portaria",
        "1465",
        2023,
        "Comando da Aeronáutica / SAGA",
        "Aprova o Plano de Zona de Proteção de Heliponto (PZPH) do Heliponto NÓR Hotel & Spa no município de São Roque (SP).",
        "Vigente",
        "https://sysaga.decea.mil.br/portaria-portal/25568",
        "PZPH_NOR_Portaria_1465_SAGA.pdf",
        "Homologa a zona de proteção do heliponto do empreendimento hoteleiro de luxo NÓR Hotel & Spa, na Estrada do Pessegueiro (Gabriel Piza), resguardando funis de aproximação e decolagem de helicópteros executivos vindos da Capital e de outras regiões.",
        "zona_protecao_aeroportuaria_catarina"
    ),
    (
        "portaria_28_ica_2015",
        "Federal",
        "Portaria",
        "28",
        2015,
        "Comando da Aeronáutica / Instituto de Cartografia Aeronáutica (ICA)",
        "Aprova o Plano Básico de Zona de Proteção de Aeródromo (PBZPA) do Aeroporto de São Paulo/Congonhas - Deputado Freitas Nobre (SBSP).",
        "Vigente",
        "https://sysaga.decea.mil.br/portaria-portal/18751",
        "PBZPA_SBSP_Portaria_28_ICA.pdf",
        "Institui a Superfície Horizontal Externa (SHE) com raio de 45 km a partir do centro da pista de Congonhas, abrangendo 10.603,80 ha (34,54%) do leste de São Roque. Restringe torres de telecomunicações e linhas de transmissão no Morro do Saboó e cumes da serra para garantir auxílios à navegação aérea (PZANA) e trajetórias IFR da TMA São Paulo.",
        "zona_protecao_aeroportuaria_catarina"
    ),
    (
        "rbac_155_anac",
        "Federal",
        "Resolução / Regulamento",
        "155",
        2018,
        "Agência Nacional de Aviação Civil (ANAC)",
        "Regulamento Brasileiro da Aviação Civil - RBAC nº 155: Helipontos - Requisitos para Projeto, Operação e Segurança.",
        "Vigente",
        "https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbact/rbac-155",
        "RBAC_155_ANAC.pdf",
        "Estabelece os parâmetros técnicos de projeto físico e operacional de helipontos em solo e elevados: dimensões mínimas de FATO (Área de Toque), TLOF, faixas de segurança, inclinações máximas de rampas de aproximação (8% a 12,5%) e requisitos de balizamento noturno.",
        "zona_protecao_aeroportuaria_catarina"
    )
]

for n in normas:
    cur.execute("""
        INSERT OR REPLACE INTO normas_juridicas (
            id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, arquivo_integra, texto_integral, camadas_competencia
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, n)

# 2. Classes de Proteção
classes = [
    (
        "zona_protecao_aeroportuaria_catarina",
        "HELIPONTO_FATO",
        "Área de Pouso de Helicópteros (FATO/TLOF)",
        "Vila Don Patto (SWVD), Taxaquara (SIZT) e NÓR Hotel",
        "#DC2626",
        "rgb(220,38,38)",
        "RBAC 155 ANAC / ICA 11-408 DECEA",
        "Piso e faixa central de toque e decolagem de helicópteros privados homologados. Área de segurança absoluta totalmente livre de obstáculos."
    ),
    (
        "zona_protecao_aeroportuaria_catarina",
        "HELIPONTO_PZPH",
        "Rampa de Aproximação de Helipontos (PZPH - 1.000m)",
        "Funil de Aproximação e Subida (8% a 12,5% de inclinação)",
        "#F43F5E",
        "rgb(244,63,94)",
        "ICA 11-408 DECEA / CBA Arts. 43-46",
        "Servidão administrativa aeronáutica sobre imóveis vizinhos. Restrição de gabarito para galpões, telhados, postes de luz, árvores de grande porte e torres."
    ),
    (
        "zona_protecao_aeroportuaria_catarina",
        "CONGONHAS_SHE_TMA",
        "Superfície Horizontal Externa de Congonhas (SBSP 45km / TMA-SP)",
        "10.603,80 ha (34,54% do território leste de São Roque)",
        "#8B5CF6",
        "rgb(139,92,246)",
        "Portaria 28/ICA/2015 / CBA Art. 44 / PZANA",
        "Área de manobra externa de aeronaves comerciais e feixes de rádio/radar da Terminal São Paulo. Restrição de altura e sinalização obrigatória para torres e estruturas nas serras."
    )
]

for c in classes:
    cur.execute("""
        INSERT OR REPLACE INTO classes_camada_territorial (
            camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb,
            metodologia_referencia, implicacao_pratica
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 3. Cruzamentos Legais
cruzamentos = [
    ("zona_protecao_aeroportuaria_catarina", "HELIPONTO_PZPH", "Federal", "Portaria", "176", 2014, "Arts. 1º a 4º", "Impeditiva", "Proibição de qualquer obra, galpão, antena ou fiação que ultrapasse as superfícies limitadoras do Heliponto Vila Don Patto.", "Prefeitura é obrigada a exigir certidão do SYSAGA antes de conceder alvará de construção na Estrada do Vinho."),
    ("zona_protecao_aeroportuaria_catarina", "HELIPONTO_PZPH", "Federal", "Portaria", "394", 2018, "Arts. 1º a 4º", "Impeditiva", "Restrição de gabarito no entorno do Taxaquara Golf Club para garantir rampas de descida seguras de helicópteros.", "Demolição sumária sem indenização caso erguida construção após a vigência do PZPH (Art. 46 CBA)."),
    ("zona_protecao_aeroportuaria_catarina", "HELIPONTO_PZPH", "Federal", "Portaria", "1465", 2023, "Arts. 1º a 4º", "Impeditiva", "Servidão aeronáutica do heliponto do NÓR Hotel & Spa na Estrada do Pessegueiro.", "Controle de altura para construções e postes na rampa de voo no bairro Gabriel Piza."),
    ("zona_protecao_aeroportuaria_catarina", "CONGONHAS_SHE_TMA", "Federal", "Portaria", "28", 2015, "Arts. 2º e 3º", "Condicionante", "Subordinação de novas torres de celular, linhas de transmissão e parques eólicos a processo OPEA no DECEA.", "Proteção dos sinais de radiofrequência e trajetórias IFR de Congonhas sobre os morros de São Roque."),
    ("zona_protecao_aeroportuaria_catarina", "HELIPONTO_FATO", "Federal", "Resolução", "155", 2018, "Arts. 10 a 25", "Condicionante", "Parâmetros técnicos mínimos de dimensões, resistência de piso e sinalização visual para helipontos civis.", "Obrigatória renovação periódica de homologação perante a ANAC e inspeção pelo DECEA.")
]

for crz in cruzamentos:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao (
            camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
            artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, crz)

# Atualizar metadados da camada
cur.execute("""
    UPDATE camadas_territoriais
    SET nome = 'Proteção Aeroportuária, Helipontos e TMA (DECEA / ANAC)',
        titulo_documento = 'Complexo de Zonas de Proteção: Aeroporto Catarina (SBJH), Helipontos e Congonhas (SBSP)',
        alerta_juridico = 'Servidões aeronáuticas federais ativas: SBJH (Pista e ASA 20km), 3 helipontos homologados (Vila Don Patto, Taxaquara, NÓR) e SHE Congonhas (10.603 ha). Alvarás municipais exigem certidão prévia no SYSAGA/DECEA.'
    WHERE id = 'zona_protecao_aeroportuaria_catarina'
""")

conn.commit()
print("Sucesso! Ingestão de 5 normas, 3 novas classes e 5 cruzamentos legislativos concluída no SQLite.")
conn.close()
