import sqlite3
import json

print("=== INGESTÃO DA REVISÃO DO PLANO DIRETOR (2024-2026) NO BANCO OFICIAL ===")

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Inserir Normas Jurídicas da Revisão 2026
normas = [
    (
        "minuta_lc_39_2026",
        "Municipal",
        "Minuta de Lei Complementar",
        "Revisão LC 39/2006",
        2026,
        "Prefeitura Municipal da Estância Turística de São Roque / DPMA",
        "Dispõe sobre a Revisão do Plano Diretor Estratégico da Estância Turística de São Roque, estabelecendo diretrizes de ordenamento territorial, sustentabilidade, desenvolvimento econômico, turismo e instrumentos da política urbana (Estatuto da Cidade).",
        "Em Tramitação / Minuta Oficial Final (Agosto/2026)",
        "https://www.saoroque.sp.gov.br",
        "minuta_pd2026/desmembrado/03_minuta_lc39_plano_diretor_estrategico.pdf",
        "Minuta oficial da Revisão da Lei Complementar nº 39/2006 (Plano Diretor Estratégico)",
        "revisao_plano_diretor_2026, macrozoneamento_2026, cartas_tecnicas_2026"
    ),
    (
        "minuta_lc_40_2026",
        "Municipal",
        "Minuta de Lei Complementar",
        "Revisão LC 40/2006",
        2026,
        "Prefeitura Municipal da Estância Turística de São Roque / DPMA",
        "Disciplina o Uso, Ocupação, Parcelamento e Regularização do Solo na Estância Turística de São Roque, definindo as Macrozonas, Zonas de Urbanização Específica (ZUE), Consolidação Urbana (ZUR, ZUC, ZUI), Corredores Comerciais/Turísticos e Quadros I a IX de índices construtivos.",
        "Em Tramitação / Minuta Oficial Final (Agosto/2026)",
        "https://www.saoroque.sp.gov.br",
        "minuta_pd2026/desmembrado/04_minuta_lc40_zoneamento_uso_ocupacao.pdf",
        "Minuta oficial da Revisão da Lei Complementar nº 40/2006 (Zoneamento, Uso e Ocupação)",
        "revisao_plano_diretor_2026, zoneamento_2026, corredores_2026, parametros_urbanisticos"
    )
]

for n in normas:
    cur.execute("""
        INSERT OR REPLACE INTO normas_juridicas 
        (id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, arquivo_integra, texto_integral, camadas_competencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, n)
    print(f"✓ Norma registrada: {n[0]} ({n[2]} {n[3]}/{n[4]})")

# 2. Inserir Camada Territorial da Revisão 2026
camada_pd2026 = (
    "revisao_plano_diretor_2026",
    "Revisão do Plano Diretor Municipal (2024–2026 / Cartas I a XIII)",
    "REVISÃO DO PLANO DIRETOR MUNICIPAL (2024-2026) - REVISÃO 05",
    "Planejamento Urbano e Ordenamento Territorial",
    "minuta_pd2026/Plano Diretor - Combined.pdf",
    "Acervo Cartográfico CAD/GIS Oficial (13 Pranchas)",
    "Indicada (1:10.000 / 1:25.000)",
    "SIRGAS 2000 / UTM Zone 23S (EPSG:31983)",
    "Agosto/2026",
    "David de Mello Berger (Engenheiro Civil)",
    "CREA: 5070025188 (Chefe de Divisão de Engenharia)",
    "Departamento de Planejamento e Meio Ambiente (DPMA)",
    "Prefeitura da Estância Turística de São Roque",
    "Levantamentos Cadastrais DPMA, Ortofoto Dji, Cartas IGC e Estudos Técnicos da Revisão 2024-2026",
    "HOMOLOGADO_DESMEMBRADO",
    260000.0, 305000.0, 7370000.0, 7415000.0,
    "[[-23.68, -47.25], [-23.40, -46.95]]",
    "Documento oficial de revisão urbanística composto por 13 Cartas Técnicas (Macrozoneamento, ZUE, ZUC Sede/Distritos, Corredores, Áreas de Especial Interesse, Sistema Viário e 22 Obras Estruturantes SRQ-01 a SRQ-22)."
)

cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", camada_pd2026)
print("✓ Camada territorial registrada: revisao_plano_diretor_2026")

# 3. Inserir Classes Territoriais Fundamentais de 2026
classes = [
    ("revisao_plano_diretor_2026", "ZUE_TURISTICO", "ZUE - Interesse Turístico", "0-30%", "#E11D48", "RGB(225, 29, 72)", "Quadro I e II da LC 40/2026", "Gabarito básico 12m e máx 24m (OODC). Hotéis, pousadas, gastronomia e enoturismo."),
    ("revisao_plano_diretor_2026", "ZUE_MANANCIAL", "ZUE - Chácaras em Manancial", "0-15%", "#0D9488", "RGB(13, 148, 136)", "Quadro I e III da LC 40/2026", "Lote mínimo 5.000m², frente 50m, TO 50%, TP 50%. Preservação de mananciais."),
    ("revisao_plano_diretor_2026", "ZUE_DESENV_ECON", "ZUE - Desenvolvimento Econômico", "0-20%", "#D97706", "RGB(217, 119, 6)", "Quadro I e II da LC 40/2026", "Indústrias de baixo impacto, logística e comércio atacadista. Vedado aterro sanitário e cemitério."),
    ("revisao_plano_diretor_2026", "ZUE_MOMBACA", "ZUE - Setor Residencial Mombaça", "0-20%", "#7C3AED", "RGB(124, 58, 237)", "Art. 70, §4º da LC 40/2026", "Admite CA 1.2 e gabarito 24m para residencial multifamiliar de trabalhadores da Castello."),
    ("revisao_plano_diretor_2026", "ZUCL_CORREDOR", "ZUCL - Corredor Logístico (Rod. Lívio Tagliassachi)", "0-10%", "#2563EB", "RGB(37, 99, 235)", "Art. 105 da LC 40/2026", "Comércio, logística e turismo. Exige tratamento paisagístico de fachada e proíbe depósitos externos de sucata."),
    ("revisao_plano_diretor_2026", "ZUR_BAIXA", "ZUR-bd (Residencial de Baixa Densidade)", "0-30%", "#10B981", "RGB(16, 185, 129)", "Quadros VIII e IX da LC 40/2026", "Lote mín 250m², frente 10m. Recuos: Frontal 5m, lateral 1.5m, fundo 3m. Edícula máx 30%."),
    ("revisao_plano_diretor_2026", "SRQ_OBRAS", "Intervenções Prioritárias (SRQ-01 a SRQ-22)", "N/A", "#9333EA", "RGB(147, 51, 234)", "Carta XIII da Revisão 2026", "22 projetos prioritários de macrodrenagem, binários centrais e infraestrutura viária e cicloviária.")
]

for c in classes:
    cur.execute("""
        INSERT INTO classes_camada_territorial
        (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, c)
    print(f"✓ Classe registrada: {c[1]}")

con.commit()
con.close()
print("=== INGESTÃO NO BANCO CONCLUÍDA COM SUCESSO! ===")
