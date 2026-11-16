import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Inserir camada carta_04_sede_2026
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_04_sede_2026',
    'Carta IV: Consolidação Urbana - Sede (Plano Diretor 2026)',
    'CARTA IV - ZONEAMENTOS DA MACROZONA DE CONSOLIDAÇÃO URBANA - SEDE - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_04_zoneamento_consolidacao_urbana_sede.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:12.500 (Indicada)',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 101 a 150, Quadros V a IX) e LC nº 39/2006',
    'HOMOLOGADO_AUDITADO',
    276700.0, 286000.0, 7389800.0, 7402600.0,
    '[[-23.58853, -47.18916], [-23.47295, -47.09810]]',
    'Detalhamento intraurbano do Distrito Sede de São Roque (escala 1:12.500): ZUR-bd, ZUR-md 1, ZUR-ad, Zona Central, Zona Industrial e ZUPA, integrando patrimônio tombado da Brasital, malha ferroviária e encostas da Mata da Câmara.'
)
""")

# 2. Inserir classes de carta_04_sede_2026
classes_c4 = [
    ('carta_04_sede_2026', 'ZUR_BAIXA', 'ZUR – Baixa Densidade (Sede)', 'Lote mín 250m²', '#FFFF7F', 'RGB(255, 255, 127)', 'Arts. 102 (I), 104 (Quadro VI), 109 a 115 LC 40/2026', 'Ocupação residencial horizontal unifamiliar com recuo frontal 5m, lateral 1.5m e fundos 3m.'),
    ('carta_04_sede_2026', 'ZUR_MEDIA', 'ZUR – Média Densidade 1 (Sede)', 'Lote mín 250m² / Gabarito 12-24m', '#FF7F7F', 'RGB(255, 127, 127)', 'Arts. 102 (II), 104 (Quadro VI), 116 a 122 LC 40/2026', 'Bairros centrais e peri-centrais da Sede (Vila Aguiar, Junqueira, Vila Nova, Marmeleiro).'),
    ('carta_04_sede_2026', 'ZUR_ALTA', 'ZUR – Alta Densidade (Sede)', 'Eixo Adensável / Receptora TPC', '#FF622E', 'RGB(255, 98, 46)', 'Arts. 102 (III), 104 (Quadro VI), 123 a 129 LC 40/2026', 'Eixos viários de transporte coletivo receptores prioritários de Transferência de Potencial Construtivo (até CA 1.4).'),
    ('carta_04_sede_2026', 'ZUR_CENTRAL', 'Zona Urbana Central (Sede)', 'Núcleo Comercial Histórico', '#DDA56E', 'RGB(221, 165, 110)', 'Arts. 102 (IV), 104, 130 a 133 LC 40/2026', 'Centro histórico (Praça da Matriz, Av. Antonino Dias Bastos, Av. John Kennedy). Aplicação de IPTU progressivo.'),
    ('carta_04_sede_2026', 'ZUR_INDUSTRIAL', 'Zona Urbana Industrial (Sede)', 'Eixo Ferroviário / Logística', '#DD00DD', 'RGB(221, 0, 221)', 'Arts. 102 (V), 104, 134 a 138 LC 40/2026', 'Parques industriais e logísticos lindeiros à malha ferroviária e acessos viários.'),
    ('carta_04_sede_2026', 'ZUR_ZUPA', 'Zona Urbana de Preservação Ambiental (Sede)', 'Matas Urbanas / Encostas', '#8AB800', 'RGB(138, 184, 0)', 'Arts. 102 (VI), 104, 139 a 145 LC 40/2026', 'Parque da Mata da Câmara, morros e fundos de vale na Sede. Emite Transferência de Potencial Construtivo para a ZUR-ad.'),
    ('carta_04_sede_2026', 'PERIMETRO_APA_ITUPARARANGA', 'Perímetro da APA de Itupararanga', 'UC Estadual', '#EF4444', 'RGB(239, 68, 68)', 'Lei Estadual nº 10.100/1998 e Dec. Est. 52.281/2007', 'Limite sul de proteção de mananciais incidindo sobre o distrito sede.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_04_sede_2026'")
for c in classes_c4:
    cur.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 3. Vincular normas jurídicas no cruzamento
normas_cruzamento = [
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 101, I', 'Estruturante', 'Institui o Perímetro da Sede na Macrozona de Consolidação Urbana.', 'Obrigatória'),
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 103', 'Formal', 'Homologa a Carta IV como mapa oficial de zoneamento da Sede.', 'Obrigatória'),
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 104 (Quadro VI)', 'Urbanística', 'Parâmetros urbanísticos de ocupação na Sede (CA, TO, Gabaritos).', 'Vinculante'),
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 116, I', 'Setorização', 'Define a ZUR-md 1 especificamente para o perímetro urbano da Sede.', 'Vinculante'),
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 130 a 133', 'Instrumento Urbanístico', 'Regras da Zona Central e IPTU progressivo no tempo no núcleo sede.', 'Vinculante'),
    ('carta_04_sede_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 145', 'Transferência de Potencial', 'Autoriza TPC da ZUPA da Sede para terrenos receptores em ZUR-ad.', 'Faculdade Legal')
]

cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_04_sede_2026'")
for cr in normas_cruzamento:
    cur.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
        artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

con.commit()
con.close()
print("Banco de dados atualizado com sucesso com Carta IV (Consolidação Urbana: Sede)!")
