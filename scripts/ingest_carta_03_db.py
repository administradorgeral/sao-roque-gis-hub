import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Inserir camada carta_03_consolidacao_urbana_2026
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_03_consolidacao_urbana_2026',
    'Carta III: Zoneamentos da Macrozona de Consolidação Urbana (Plano Diretor 2026)',
    'CARTA III - ZONEAMENTOS DA MACROZONA DE CONSOLIDAÇÃO URBANA - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_03_zoneamentos_macrozona_consolidacao_urbana.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:25.000',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 101 a 150, Quadros V a IX) e LC nº 39/2006',
    'HOMOLOGADO_AUDITADO',
    275600.0, 308600.0, 7377000.0, 7409000.0,
    '[[-23.70714, -47.19813], [-23.41770, -46.87444]]',
    'Visão macroterritorial dos 39,22 km² da Macrozona de Consolidação Urbana articulando os 4 perímetros (Sede, Maylasky, São João Novo e Canguera) em 6 zonas urbanas: ZUR-bd, ZUR-md, ZUR-ad, Zona Central, Zona Industrial e ZUPA.'
)
""")

# 2. Inserir classes de carta_03_consolidacao_urbana_2026
classes_c3 = [
    ('carta_03_consolidacao_urbana_2026', 'ZUR_BAIXA', 'ZUR – Baixa Densidade (6,31 km²)', 'Área: 6,31 km²', '#FFFF80', 'RGB(255, 255, 128)', 'Arts. 102 (I), 104 (Quadro VI), 109 a 115 LC 40/2026', 'Lote mín 250m², frente 10m. Recuos: Frontal 5m, lateral 1.5m, fundos 3m. Ocupação predominantemente unifamiliar.'),
    ('carta_03_consolidacao_urbana_2026', 'ZUR_MEDIA', 'ZUR – Média Densidade (18,88 km²)', 'Área: 18,88 km²', '#FF8080', 'RGB(255, 128, 128)', 'Arts. 102 (II), 104 (Quadro VI), 116 a 122 LC 40/2026', 'Subdividida em ZUR-md 1 (Sede), 2 (Mailasqui), 3 (São João Novo) e 4 (Canguera). Gabarito até 30m em SJN e até 24m com OODC.'),
    ('carta_03_consolidacao_urbana_2026', 'ZUR_ALTA', 'ZUR – Alta Densidade (2,70 km²)', 'Área: 2,70 km²', '#FF5522', 'RGB(255, 85, 34)', 'Arts. 102 (III), 104 (Quadro VI), 123 a 129 LC 40/2026', 'Zona receptora prioritária de Transferência de Potencial Construtivo (TPC até CA 1.4). Edifícios multifamiliares e serviços densos.'),
    ('carta_03_consolidacao_urbana_2026', 'ZUR_CENTRAL', 'Zona Urbana Central (0,63 km²)', 'Área: 0,63 km²', '#D29050', 'RGB(210, 144, 80)', 'Arts. 102 (IV), 104, 130 a 133 LC 40/2026', 'Núcleo histórico e comercial de São Roque. Área de incidência prioritária de IPTU progressivo no tempo e Outorga Onerosa.'),
    ('carta_03_consolidacao_urbana_2026', 'ZUR_INDUSTRIAL', 'Zona Urbana Industrial (1,55 km²)', 'Área: 1,55 km²', '#DF00DF', 'RGB(223, 0, 223)', 'Arts. 102 (V), 104, 134 a 138 LC 40/2026', 'Parques industriais e logísticos com recuos de 10m e destinação de áreas públicas institucionais para ZEIS.'),
    ('carta_03_consolidacao_urbana_2026', 'ZUR_ZUPA', 'Zona Urbana de Preservação Ambiental (9,15 km²)', 'Área: 9,15 km²', '#80B000', 'RGB(128, 176, 0)', 'Arts. 102 (VI), 104, 139 a 145 LC 40/2026', 'Áreas de encosta, matas ciliares e fundos de vale na malha urbana. Emite Transferência de Potencial Construtivo para a ZUR-ad.'),
    ('carta_03_consolidacao_urbana_2026', 'MACROZONA_RURAL', 'Macrozona Rural (Entorno)', 'Módulo INCRA 20.000m²', '#00FF00', 'RGB(0, 255, 0)', 'Minuta LC 39/2006 e LC 40/2026', 'Módulo rural mínimo 20.000m² (INCRA), agricultura familiar, enoturismo e preservação ambiental.'),
    ('carta_03_consolidacao_urbana_2026', 'MACROZONA_ZUE', 'Macrozona de Urbanização Específica (Entorno)', '153,33 km² ZUE', '#FFB6C1', 'RGB(255, 182, 193)', 'Minuta LC 39/2006 e LC 40/2026', 'Articulação periurbana com Turismo, Mananciais, Ocupação Estratégica e Desenvolvimento Econômico.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_03_consolidacao_urbana_2026'")
for c in classes_c3:
    cur.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 3. Vincular normas jurídicas no cruzamento
normas_cruzamento = [
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 101', 'Estruturante', 'Define os 4 perímetros urbanos consolidados: Sede, Maylasky, São João Novo e Canguera.', 'Obrigatória'),
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 102', 'Estruturante', 'Institui as 6 zonas urbanas da Consolidação Urbana (ZUR-bd, ZUR-md, ZUR-ad, Central, Industrial, ZUPA).', 'Obrigatória'),
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 103', 'Formal', 'Homologa a Carta III (Geral) e as Cartas IV a VII (Detalhadas) como mapa oficial.', 'Obrigatória'),
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 104 (Quadro VI)', 'Urbanística', 'Fixa coeficientes de aproveitamento, gabaritos e taxas de ocupação para cada zona urbana.', 'Vinculante'),
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 145', 'Instrumento Urbanístico', 'Autoriza Transferência do Potencial Construtivo (TPC) da ZUPA para a ZUR-ad (limite CA 1.4).', 'Faculdade Legal'),
    ('carta_03_consolidacao_urbana_2026', None, 'Municipal', 'Lei Complementar', '39', 2026, 'Art. 49', 'Macroestratégica', 'Institui a Macrozona de Consolidação Urbana no Plano Diretor Estratégico.', 'Obrigatória')
]

cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_03_consolidacao_urbana_2026'")
for cr in normas_cruzamento:
    cur.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
        artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

con.commit()
con.close()
print("Banco de dados atualizado com sucesso com Carta III (Consolidação Urbana)!")
