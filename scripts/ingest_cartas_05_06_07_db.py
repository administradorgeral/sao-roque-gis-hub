import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# -------------------------------------------------------------
# 1. CARTA V: MAYLASKY (Prancha 05/13)
# -------------------------------------------------------------
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_05_maylasky_2026',
    'Carta V: Consolidação Urbana - Maylasky (Plano Diretor 2026)',
    'CARTA V - ZONEAMENTOS DA MACROZONA DE CONSOLIDAÇÃO URBANA - MAYLASKY - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_05_zoneamento_consolidacao_urbana_maylasky.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:12.500 (Indicada)',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 101, II, 102 a 150) e LC nº 39/2006',
    'HOMOLOGADO_AUDITADO',
    285500.0, 301400.0, 7379900.0, 7394300.0,
    '[[-23.67791, -47.09913], [-23.54788, -46.94378]]',
    'Detalhamento intraurbano do Distrito de Maylasky (escala 1:12.500): ZUR-bd, ZUR-md 2, Zona Industrial e ZUPA, integrando loteamentos históricos (Sun Valley, Las Brisas, Patrimônio do Carmo), eixo ferroviário e Rod. Engº Renê Benedito da Silva.'
)
""")

classes_c5 = [
    ('carta_05_maylasky_2026', 'ZUR_BAIXA', 'ZUR – Baixa Densidade (Maylasky)', 'Lote mín 250m²', '#FFFF7F', 'RGB(255, 255, 127)', 'Arts. 102 (I), 104, 109 a 115 LC 40/2026', 'Residencial de baixa densidade nos núcleos consolidados de Maylasky.'),
    ('carta_05_maylasky_2026', 'ZUR_MEDIA_2', 'ZUR – Média Densidade 2 (Maylasky)', 'Gabarito máx 12m (T+3)', '#FF7F7F', 'RGB(255, 127, 127)', 'Arts. 102 (II), 104, 116 (II) LC 40/2026', 'Padrão distrital com gabarito limitado a 12 metros (Térreo + 3 pavimentos).'),
    ('carta_05_maylasky_2026', 'ZUR_INDUSTRIAL', 'Zona Urbana Industrial (Maylasky)', 'Parque Fabril e Logístico', '#DD00DD', 'RGB(221, 0, 221)', 'Arts. 102 (V), 104, 134 a 138 LC 40/2026', 'Polo industrial contíguo à ferrovia e à Rodovia Renê Benedito da Silva.'),
    ('carta_05_maylasky_2026', 'ZUR_ZUPA', 'Zona Urbana de Preservação Ambiental (Maylasky)', 'APPs e Encostas', '#8AB800', 'RGB(138, 184, 0)', 'Arts. 102 (VI), 104, 139 a 145 LC 40/2026', 'Fundos de vale do Córrego Maylasky e matas de preservação municipal.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_05_maylasky_2026'")
for c in classes_c5:
    cur.execute("INSERT INTO classes_camada_territorial (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", c)

normas_c5 = [
    ('carta_05_maylasky_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 101, II', 'Estruturante', 'Institui o Perímetro de Maylasky na Macrozona de Consolidação Urbana.', 'Obrigatória'),
    ('carta_05_maylasky_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 103', 'Formal', 'Homologa a Carta V como mapa oficial de zoneamento de Maylasky.', 'Obrigatória'),
    ('carta_05_maylasky_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 116, II', 'Urbanística', 'Fixa gabarito máximo de 12 metros para ZUR-md 2 em Maylasky.', 'Vinculante')
]
cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_05_maylasky_2026'")
for cr in normas_c5:
    cur.execute("INSERT INTO cruzamento_camada_legislacao (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cr)

# -------------------------------------------------------------
# 2. CARTA VI: SÃO JOÃO NOVO (Prancha 06/13)
# -------------------------------------------------------------
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_06_sao_joao_novo_2026',
    'Carta VI: Consolidação Urbana - São João Novo (Plano Diretor 2026)',
    'CARTA VI - ZONEAMENTOS DA MACROZONA DE CONSOLIDAÇÃO URBANA - SÃO JOÃO NOVO - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_06_zoneamento_consolidacao_urbana_sao_joao_novo.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:12.500 (Indicada)',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 101, III, 102 a 150) e LC nº 39/2006',
    'HOMOLOGADO_AUDITADO',
    287400.0, 303300.0, 7393900.0, 7408300.0,
    '[[-23.55159, -47.08063], [-23.42156, -46.92527]]',
    'Detalhamento intraurbano do Distrito de São João Novo (escala 1:12.500): ZUR-bd, ZUR-md 2, ZUPA e conexão viária e ambiental com o Aeroporto Internacional Catarina (SBJH).'
)
""")

classes_c6 = [
    ('carta_06_sao_joao_novo_2026', 'ZUR_BAIXA', 'ZUR – Baixa Densidade (São João Novo)', 'Lote mín 250m²', '#FFFF7F', 'RGB(255, 255, 127)', 'Arts. 102 (I), 104, 109 a 115 LC 40/2026', 'Ocupação unifamiliar nos núcleos residenciais de São João Novo.'),
    ('carta_06_sao_joao_novo_2026', 'ZUR_MEDIA_2', 'ZUR – Média Densidade 2 (São João Novo)', 'Gabarito máx 12m', '#FF7F7F', 'RGB(255, 127, 127)', 'Arts. 102 (II), 104, 116 (II) LC 40/2026', 'Núcleo central distrital com gabarito restrito.'),
    ('carta_06_sao_joao_novo_2026', 'ZUR_ZUPA', 'Zona Urbana de Preservação Ambiental (São João Novo)', 'Preservação de Encostas', '#8AB800', 'RGB(138, 184, 0)', 'Arts. 102 (VI), 104, 139 a 145 LC 40/2026', 'Matas de encosta e bacia hidrográfica distrital.'),
    ('carta_06_sao_joao_novo_2026', 'PROTECAO_CATARINA', 'Interface Aeroporto Catarina (SBJH)', 'Cone e Rampa DECEA', '#EF4444', 'RGB(239, 68, 68)', 'Portaria 230/SAGA/2020 DECEA e CBA Lei 7.565/86', 'Restrições aeronáuticas incidentes sobre São João Novo.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_06_sao_joao_novo_2026'")
for c in classes_c6:
    cur.execute("INSERT INTO classes_camada_territorial (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", c)

normas_c6 = [
    ('carta_06_sao_joao_novo_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 101, III', 'Estruturante', 'Institui o Perímetro de São João Novo na Macrozona de Consolidação Urbana.', 'Obrigatória'),
    ('carta_06_sao_joao_novo_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 103', 'Formal', 'Homologa a Carta VI como mapa oficial de zoneamento de São João Novo.', 'Obrigatória'),
    ('carta_06_sao_joao_novo_2026', None, 'Federal', 'Portaria', '230/SAGA', 2020, 'PBZPA SBJH', 'Aeronáutica', 'Gabaritos vinculados às superfícies limitadoras do Aeroporto Catarina.', 'Vinculante')
]
cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_06_sao_joao_novo_2026'")
for cr in normas_c6:
    cur.execute("INSERT INTO cruzamento_camada_legislacao (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cr)

# -------------------------------------------------------------
# 3. CARTA VII: CANGUERA (Prancha 07/13)
# -------------------------------------------------------------
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_07_canguera_2026',
    'Carta VII: Consolidação Urbana - Canguera (Plano Diretor 2026)',
    'CARTA VII - ZONEAMENTOS DA MACROZONA DE CONSOLIDAÇÃO URBANA - CANGUERA - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_07_zoneamento_consolidacao_urbana_canguera.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:12.500 (Indicada)',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 101, IV, 102 a 150) e LC nº 39/2006',
    'HOMOLOGADO_AUDITADO',
    265500.0, 281400.0, 7381300.0, 7395700.0,
    '[[-23.66545, -47.29555], [-23.53541, -47.14019]]',
    'Detalhamento intraurbano do Distrito de Canguera (escala 1:12.500): ZUR-bd, ZUR-md 2, ZUPA e Corredores Comerciais e Turísticos ao longo da Rota do Vinho e Rod. Quintino de Lima, em conformidade com o Plano de Manejo da APA de Itupararanga.'
)
""")

classes_c7 = [
    ('carta_07_canguera_2026', 'ZUR_BAIXA', 'ZUR – Baixa Densidade (Canguera)', 'Lote mín 250m²', '#FFFF7F', 'RGB(255, 255, 127)', 'Arts. 102 (I), 104, 109 a 115 LC 40/2026', 'Residencial horizontal e chácaras integradas à paisagem rural/turística.'),
    ('carta_07_canguera_2026', 'ZUR_MEDIA_2', 'ZUR – Média Densidade 2 (Canguera)', 'Gabarito máx 12m', '#FF7F7F', 'RGB(255, 127, 127)', 'Arts. 102 (II), 104, 116 (II) LC 40/2026', 'Núcleo central de Canguera (Campininha, Pavão, Goianã).'),
    ('carta_07_canguera_2026', 'ZUR_ZUPA', 'Zona Urbana de Preservação Ambiental (Canguera)', 'Mananciais / Mata Atlântica', '#8AB800', 'RGB(138, 184, 0)', 'Arts. 102 (VI), 104, 139 a 145 LC 40/2026', 'Encostas e bacias de contribuição da Represa de Itupararanga.'),
    ('carta_07_canguera_2026', 'CORREDOR_TURISTICO', 'Corredores Turísticos e Gastronômicos', 'Estrada do Vinho / SP-077', '#F59E0B', 'RGB(245, 158, 11)', 'Arts. 151 a 165 LC 40/2026', 'Atividades enoturísticas, adegas, restaurantes e hotelaria.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_07_canguera_2026'")
for c in classes_c7:
    cur.execute("INSERT INTO classes_camada_territorial (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", c)

normas_c7 = [
    ('carta_07_canguera_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 101, IV', 'Estruturante', 'Institui o Perímetro de Canguera na Macrozona de Consolidação Urbana.', 'Obrigatória'),
    ('carta_07_canguera_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 103', 'Formal', 'Homologa a Carta VII como mapa oficial de zoneamento de Canguera.', 'Obrigatória'),
    ('carta_07_canguera_2026', None, 'Estadual', 'Lei Ordinária', '11579', 2003, 'APA Itupararanga', 'Ambiental', 'Restrições de uso do solo em área de preservação de mananciais.', 'Vinculante')
]
cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_07_canguera_2026'")
for cr in normas_c7:
    cur.execute("INSERT INTO cruzamento_camada_legislacao (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cr)

con.commit()
con.close()
print("Banco de dados sao_roque_geodados.db atualizado com sucesso com Cartas V, VI e VII!")
