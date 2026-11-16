import sqlite3

db_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== INGESTÃO DA CAMADA RBCV (UNESCO) NO BANCO DE DADOS OFICIAL ===")

# 1. Inserir Normas Jurídicas da RBCV
normas_rbcv = [
    (
        "UNESCO_RES_28C_1995", "Internacional (UNESCO)", "Resolução Internacional", "28 C/2.4", 1995,
        "UNESCO - Conferência Geral",
        "Aprova o Marco Estatutário da Rede Mundial de Reservas da Biosfera (Programa MaB), estabelecendo as Zonas-Núcleo, Zonas de Amortecimento e Zonas de Transição.",
        "Em Vigor", "https://en.unesco.org/mab",
        "Marco Estatutário da Rede Mundial de Reservas da Biosfera adotado pela Conferência Geral da UNESCO na sua 28ª Sessão (Paris, 1995). Define as três funções integradas das reservas da biosfera (conservação, desenvolvimento sustentável e apoio logístico) e o sistema tripartite de zoneamento.",
        "rbcv_cinturao_verde,vegetacao_arborea"
    ),
    (
        "DEC_FED_80978_1977", "Federal", "Decreto Federal", "80978", 1977,
        "Presidência da República",
        "Promulga a Convenção sobre a Proteção do Patrimônio Mundial, Cultural e Natural da UNESCO (Paris, 1972).",
        "Em Vigor", "http://www.planalto.gov.br/ccivil_03/decreto/antigos/d80978.htm",
        "Decreto nº 80.978, de 12 de dezembro de 1977. Promulga a Convenção para a Proteção do Patrimônio Mundial, Cultural e Natural, reconhecendo a obrigação do Estado brasileiro de identificar, proteger, conservar e valorizar os patrimônios naturais e culturais de valor universal excepcional.",
        "rbcv_cinturao_verde,territorio_municipal"
    ),
    (
        "LEI_FED_9985_2000", "Federal", "Lei Ordinária", "9985", 2000,
        "Congresso Nacional",
        "Institui o Sistema Nacional de Unidades de Conservação da Natureza (SNUC) e internaliza as Reservas da Biosfera da UNESCO no Direito Brasileiro (Art. 41).",
        "Em Vigor", "http://www.planalto.gov.br/ccivil_03/leis/l9985.htm",
        "Lei nº 9.985, de 18 de julho de 2000. Art. 41: As Reservas da Biosfera são modelo de gestão integrada, participativa e sustentável dos recursos naturais, com os objetivos fundamentais de preservação da biodiversidade, desenvolvimento de atividades sustentáveis e pesquisa científica.",
        "rbcv_cinturao_verde,apa_itupararanga"
    ),
    (
        "DEC_FED_4340_2002", "Federal", "Decreto Federal", "4340", 2002,
        "Presidência da República",
        "Regulamenta artigos da Lei nº 9.985/2000 (SNUC), disciplinando as Reservas da Biosfera e seus conselhos deliberativos.",
        "Em Vigor", "http://www.planalto.gov.br/ccivil_03/decreto/2002/d4340.htm",
        "Decreto nº 4.340, de 22 de agosto de 2002. Regulamenta os arts. 41 a 44 da Lei do SNUC, fixando a competência e representação dos comitês e conselhos das reservas da biosfera no território nacional.",
        "rbcv_cinturao_verde"
    ),
    (
        "DEC_FED_12035_2024", "Federal", "Decreto Federal", "12035", 2024,
        "Presidência da República / MMA",
        "Reestrutura a Comissão Brasileira para o Programa 'O Homem e a Biosfera' (COBRAMAB) junto ao Ministério do Meio Ambiente e Mudança do Clima.",
        "Em Vigor", "http://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/decreto/d12035.htm",
        "Decreto nº 12.035, de 28 de maio de 2024. Dispõe sobre a Comissão Brasileira para o Programa 'O Homem e a Biosfera' - COBRAMAB, órgão colegiado encarregado de coordenar e supervisionar a implementação das reservas da biosfera no Brasil em articulação com a UNESCO.",
        "rbcv_cinturao_verde"
    ),
    (
        "DEC_EST_47094_2002", "Estadual (SP)", "Decreto Estadual", "47094", 2002,
        "Governo do Estado de São Paulo",
        "Cria o Conselho de Gestão da Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo e disciplina sua governança ambiental.",
        "Em Vigor", "https://www.al.sp.gov.br/norma/47094/",
        "Decreto Estadual nº 47.094, de 18 de setembro de 2002. Institui o Conselho de Gestão da Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo (RBCV), como instância colegiada, consultiva e de pactuação territorial entre o Estado, os 73 municípios do Cinturão Verde e a sociedade civil.",
        "rbcv_cinturao_verde,apa_itupararanga"
    ),
    (
        "LEI_MUN_2499_1999", "Municipal (São Roque)", "Lei Ordinária", "2499", 1999,
        "Prefeitura Municipal de São Roque",
        "Cria o Parque Natural Municipal Mata da Câmara em São Roque, Unidade de Conservação de Proteção Integral (Zona-Núcleo da UNESCO).",
        "Em Vigor", "https://www.saoroque.sp.gov.br/",
        "Lei Municipal nº 2.499/1999 e Decreto Regulamentador nº 5.862/2005. Cria e delimita o Parque Natural Municipal Mata da Câmara, com 54 hectares de Mata Atlântica de excepcional valor cênico e ecológico, categorizado como Zona-Núcleo da Reserva da Biosfera da UNESCO.",
        "rbcv_cinturao_verde,vegetacao_arborea"
    )
]

for n in normas_rbcv:
    cur.execute("""
        INSERT OR REPLACE INTO normas_juridicas 
        (id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, texto_integral, camadas_competencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, n)

print("Normas jurídicas da RBCV inseridas com sucesso.")

# 2. Inserir em camadas_territoriais
cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais 
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (
        'rbcv_cinturao_verde',
        'Reserva da Biosfera do Cinturão Verde (RBCV / UNESCO)',
        'MAPA DA RESERVA DA BIOSFERA DO CINTURÃO VERDE DA CIDADE DE SÃO PAULO',
        'Patrimônio Internacional e Governança Regional (UNESCO)',
        'zoneamento_rbcv_2019.pdf',
        'vetor_e_raster_regional',
        '1:1.300.000',
        'WGS84 (EPSG:4326) / SIRGAS 2000 UTM 23S',
        '01/06/2019',
        'Instituto Florestal (IF / SIMA / Fundação Florestal)',
        'Órgão Estadual de Pesquisa e Conservação Florestal',
        'Equipe Técnica RBCV / MaB UNESCO',
        'Cadastro Nacional de UCs / UNESCO',
        'Instituto Florestal (IF), Esri, OpenStreetMap, MMA e UNESCO (Programa MaB 1994/2019)',
        'Auditado e Integrado Regional (Extensão Macroregional dos 73 Municípios + Zonas-Núcleo Vetoriais)',
        274626.28,
        296740.16,
        7382541.32,
        7409302.03,
        '[[-25.35759, -47.48216], [-22.43963, -45.28217]]',
        '🌐 CHANCELA INTERNACIONAL UNESCO / MaB: A Reserva da Biosfera do Cinturão Verde da Cidade de São Paulo engloba São Roque e 72 municípios paulistas. Divide-se em Zonas-Núcleo (proteção integral estrita, incluindo o Parque Natural Municipal Mata da Câmara), Zonas de Amortecimento (APA Itupararanga) e Zonas de Transição. Subordinada ao Art. 41 do SNUC (Lei Federal 9.985/00), Dec. Federal 12.035/24 (COBRAMAB) e Dec. Estadual 47.094/02.'
    )
""")

# 3. Inserir classes em classes_camada_territorial
cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'rbcv_cinturao_verde',
        'RBCV_ZONA_NUCLEO',
        'Zona-Núcleo da Reserva da Biosfera (UNESCO)',
        'Unidades de Proteção Integral e Maciços Primários',
        '#38A800',
        'RGB(56, 168, 0)',
        'UNESCO / Marco Estatutário MaB (1995) / SNUC Art. 41',
        'Proteção integral absoluta. Dedicada exclusivamente à preservação da biodiversidade, monitoramento ambiental e pesquisa científica. Inclui em São Roque o Parque Natural Municipal Mata da Câmara (Lei 2.499/99).'
    )
""")

cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'rbcv_cinturao_verde',
        'RBCV_LIMITE',
        'Limite Oficial da Reserva da Biosfera do Cinturão Verde',
        'Perímetro de Cooperação e Amortecimento dos 73 Municípios',
        '#000000',
        'RGB(0, 0, 0)',
        'Decreto Estadual nº 47.094/2002 / UNESCO MaB 1994',
        'Perímetro de contenção do espraiamento urbano predatório e proteção da macrobacia de mananciais de abastecimento metropolitano e do interior.'
    )
""")

# 4. Inserir Cruzamentos Legislativos em cruzamento_camada_legislacao (10 parâmetros cada)
cruzamentos_rbcv = [
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Internacional (UNESCO)", "Resolução Internacional", "28 C/2.4", 1995, "Art. 4º, § 5º", "Proteção Integral Estrita", "Zonas-núcleo são áreas legalmente constituídas dedicadas à conservação da natureza a longo prazo.", "Vedada qualquer atividade antrópica predatória ou descaracterização do ecossistema."),
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Federal", "Lei Ordinária", "9985", 2000, "Art. 41", "Marco Legal SNUC", "As reservas da biosfera são geridas por conselho deliberativo ou consultivo com representação paritária.", "Zoneamento tripartite vinculante para instrumentos de planejamento territorial."),
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Federal", "Decreto Federal", "12035", 2024, "Art. 2º", "Gestão COBRAMAB / MMA", "Supervisão e fiscalização da conformidade das reservas brasileiras com os padrões da UNESCO.", "Exigência de planos de ação territorial e relatórios periódicos de sustentabilidade."),
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Federal", "Decreto Federal", "80978", 1977, "Art. 4º e 5º", "Convenção Patrimônio Mundial", "Dever do Estado brasileiro de adotar medidas jurídicas, científicas e técnicas eficazes para a conservação do patrimônio natural.", "Subordina intervenções a padrões internacionais de conservação."),
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Estadual", "Decreto Estadual", "47094", 2002, "Arts. 1º a 4º", "Conselho de Gestão RBCV", "Cria e estrutura o Conselho de Gestão da RBCV sob coordenação do Instituto Florestal de SP.", "Articulação de políticas públicas ambientais intermunicipais."),
    ("rbcv_cinturao_verde", "RBCV_ZONA_NUCLEO", "Municipal", "Lei Ordinária", "2499", 1999, "Art. 1º a 3º", "Parque Mata da Câmara", "Criação do Parque Natural Municipal da Mata da Câmara como Unidade de Conservação de Proteção Integral.", "Classificação oficial como Zona-Núcleo da Reserva da Biosfera da UNESCO."),
    ("rbcv_cinturao_verde", "RBCV_LIMITE", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Plano Diretor de São Roque", "Definição do cinturão verde da reserva da biosfera como arco florestado de continuidade territorial na Macrozona Rural.", "Contenção do perímetro urbano e fomento do ecoturismo e enoturismo sustentável.")
]

for cr in cruzamentos_rbcv:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao 
        (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

conn.commit()

# Rebuild FTS
try:
    cur.execute("INSERT INTO normas_fts(normas_fts) VALUES('rebuild')")
    conn.commit()
    print("FTS index rebuilt com normas da RBCV.")
except Exception as e:
    print("FTS note:", e)

cur.execute("SELECT COUNT(*) FROM camadas_territoriais")
print("Total Camadas Territoriais:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM classes_camada_territorial")
print("Total Classes Cadastradas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao")
print("Total Cruzamentos:", cur.fetchone()[0])

conn.close()
print("=== BASE DE DADOS SINCRONIZADA COM RBCV (UNESCO)! ===")
