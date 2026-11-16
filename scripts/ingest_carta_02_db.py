import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

# 1. Inserir camada carta_01_macrozoneamento_2026 se não existir
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_01_macrozoneamento_2026',
    'Carta I: Macrozoneamento Municipal (Plano Diretor 2026)',
    'CARTA I - MACROZONEAMENTO MUNICIPAL - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_01_macrozoneamento_municipal.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:25.000',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 39/2006 (Art. 49 e Anexo I) e LC nº 40/2006',
    'HOMOLOGADO_AUDITADO',
    275600.0, 308600.0, 7377000.0, 7409000.0,
    '[[-23.70714, -47.19813], [-23.41770, -46.87444]]',
    'Macrozoneamento estruturante municipal em 3 macrozonas: Consolidação Urbana, Urbanização Específica e Macrozona Rural.'
)
""")

# 2. Inserir camada carta_02_zue_2026
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem,
    tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'carta_02_zue_2026',
    'Carta II: Zoneamentos da Macrozona de Urbanização Específica (Plano Diretor 2026)',
    'CARTA II - ZONEAMENTOS DA MACROZONA DE URBANIZAÇÃO ESPECÍFICA - REVISÃO 05 (AGÔSTO/2026)',
    'Planejamento Urbano e Ordenamento Territorial',
    'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_02_zoneamentos_macrozona_urbanizacao_especifica.pdf',
    'Cartografia Temática Oficial / Raster Georreferenciado',
    '1:25.000',
    'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)',
    'Agosto/2026',
    'David de Mello Berger (Engenheiro Civil)',
    'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
    'Departamento de Planejamento e Meio Ambiente (DPMA)',
    'Prefeitura da Estância Turística de São Roque',
    'Minuta de Revisão da LC nº 40/2006 (Arts. 66 a 100, Quadros I, II, III e IV)',
    'HOMOLOGADO_AUDITADO',
    275600.0, 308600.0, 7377000.0, 7409000.0,
    '[[-23.70714, -47.19813], [-23.41770, -46.87444]]',
    'Regulamenta os 153,33 km² da Macrozona de Urbanização Específica em 5 zonas: Chácaras em Manancial (49,19 km²), Interesse Turístico (89,92 km²), Ocupação Estratégica (7,58 km²), Desenvolvimento Econômico (4,77 km²) e Atividades Especiais Raposo Tavares (1,87 km²).'
)
""")

# 3. Inserir classes de carta_02_zue_2026
classes_c2 = [
    ('carta_02_zue_2026', 'ZUE_MANANCIAL', 'ZUE – Chácaras em Manancial (49,19 km²)', 'Área: 49,19 km²', '#007FFF', 'RGB(0, 127, 255)', 'Arts. 66 (II), 69 (Quadro I), 81 a 87 LC 40/2026', 'Lote mín 5.000m², testada 50m, TO 50%, TP 50%, Gabarito 30m (anteriores 8m). Usos CS, TL, IT, RG, RL.'),
    ('carta_02_zue_2026', 'ZUE_TURISTICO', 'ZUE – Interesse Turístico (89,92 km²)', 'Área: 89,92 km²', '#FFCF3D', 'RGB(255, 207, 61)', 'Arts. 66 (III), 69 (Quadro I), 88 a 93 LC 40/2026', 'Gabarito básico 12m, máx 24m (OODC), TO 50%, CA máx 1.2. Mombaça admite habitação multifamiliar operária até 24m.'),
    ('carta_02_zue_2026', 'ZUE_RAPOSO', 'ZUE – Atividades Especiais Raposo Tavares (1,87 km²)', 'Área: 1,87 km²', '#7F00FF', 'RGB(127, 0, 255)', 'Arts. 66 (I), 71 §2º LC 40/2026', 'Comércio e serviços com frente para Rod. Raposo Tavares. Vedados condomínios residenciais horizontais ou verticais exclusivos.'),
    ('carta_02_zue_2026', 'ZUE_OCUP_ESTRATEGICA', 'ZUE – Ocupação Estratégica (7,58 km²)', 'Área: 7,58 km²', '#FF7FDF', 'RGB(255, 127, 223)', 'Arts. 66 (V), 69, 72 (Quadro IV), 99-100 LC 40/2026', 'Recuos frontal e fundo mín 10m. Vedado aterro sanitário e cemitério. Projetos estruturantes e tecnologia.'),
    ('carta_02_zue_2026', 'ZUE_DESENV_ECONOMICO', 'ZUE – Desenvolvimento Econômico (4,77 km²)', 'Área: 4,77 km²', '#FF0000', 'RGB(255, 0, 0)', 'Arts. 66 (IV), 69, 72 (Quadro IV), 94-98 LC 40/2026', 'Indústria limpa, logística e distribuição. Recuos frontal e fundo mín 10m. Vedado aterro sanitário e cemitério.'),
    ('carta_02_zue_2026', 'MACROZONA_RURAL', 'Macrozona Rural (Entorno)', 'Módulo INCRA 20.000m²', '#00FF00', 'RGB(0, 255, 0)', 'Minuta LC 39/2006 e LC 40/2026', 'Módulo rural mínimo 20.000m² (INCRA), agricultura familiar, enoturismo e preservação ambiental.'),
    ('carta_02_zue_2026', 'MACROZONA_CONSOLIDACAO', 'Macrozona de Consolidação Urbana (Entorno)', 'Sede e Distritos', '#FF7F00', 'RGB(255, 127, 0)', 'Minuta LC 39/2006 e LC 40/2026', 'Malha urbana consolidada da Sede, Maylasky, São João Novo e Canguera.'),
    ('carta_02_zue_2026', 'PERIMETRO_APA_ITUPARARANGA', 'Perímetro da APA de Itupararanga', 'UC Estadual', '#EF4444', 'RGB(239, 68, 68)', 'Lei Estadual nº 10.100/1998 e Dec. Est. 52.281/2007', 'Delimitação da APA Estadual com regras de restrição ambiental e zoneamento da bacia.')
]

cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'carta_02_zue_2026'")
for c in classes_c2:
    cur.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 4. Vincular normas jurídicas no cruzamento
normas_cruzamento = [
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 66', 'Estruturante', 'Define as 5 zonas integrantes da Macrozona de Urbanização Específica.', 'Obrigatória'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 67', 'Formal', 'Homologa a Carta II como mapa oficial integrante da lei de zoneamento.', 'Obrigatória'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 69 (Quadro I)', 'Urbanística', 'Lote mínimo, TO máx, TP mín, CA e Gabarito de altura para cada ZUE.', 'Vinculante'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 70 (Quadro II)', 'Uso do Solo', 'Usos permitidos, tolerados e proibidos nas zonas ZUE (vedado aterro/cemitério).', 'Vinculante'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 71 (Quadro III)', 'Parcelamento', 'Parâmetros de parcelamento, desmembramento e desdobro em ZUE.', 'Vinculante'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '40', 2026, 'Art. 72 (Quadro IV)', 'Edificação', 'Recuos mínimos obrigatórios frontais (até 10m), laterais e de fundos.', 'Vinculante'),
    ('carta_02_zue_2026', None, 'Municipal', 'Lei Complementar', '39', 2026, 'Art. 49', 'Macroestratégica', 'Institui a Macrozona de Urbanização Específica no Plano Diretor Estratégico.', 'Obrigatória'),
    ('carta_02_zue_2026', None, 'Estadual', 'Lei Ordinária', '10100', 1998, 'Art. 1º', 'Ambiental', 'Incidência do Perímetro da APA de Itupararanga sobre o sul da Macrozona ZUE.', 'Sobreposição')
]

cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'carta_02_zue_2026'")
for cr in normas_cruzamento:
    cur.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
        artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

con.commit()
con.close()
print("Banco de dados atualizado com sucesso com Carta I e Carta II!")
