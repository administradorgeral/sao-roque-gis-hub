import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

sheets_meta = [
    (
        'carta_08_corredores_2026',
        'Carta VIII: Corredores de Comércio, Serviços e Turismo (Plano Diretor 2026)',
        'CARTA VIII - CORREDORES DE COMÉRCIO, SERVIÇOS E TURISMO - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_08_corredores_comercio_servicos_turismo.pdf',
        '1:25.000 (Indicada)',
        268500.0, 290600.0, 7382000.0, 7408800.0,
        '[[-23.65394, -47.20889], [-23.41153, -46.99093]]',
        'Corredores de Comércio, Serviços e Turismo: Estrada do Vinho, Rodovia Raposo Tavares (SP-270), Rod. Lívio Tagliassachi, Rod. Quintino de Lima (SP-077) e Rod. Engº Renê Benedito da Silva.'
    ),
    (
        'carta_09_aeis_2026',
        'Carta IX: Áreas de Especial Interesse - AEIS, AEIT, AEIU (Plano Diretor 2026)',
        'CARTA IX - ÁREAS DE ESPECIAL INTERESSE - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_09_areas_especial_interesse_aeis_aeit_aeiu.pdf',
        '1:25.000 (Indicada)',
        268500.0, 290600.0, 7382000.0, 7408800.0,
        '[[-23.65394, -47.20889], [-23.41153, -46.99093]]',
        'Áreas de Especial Interesse Social (AEIS 1, 2 e 3 para HIS e Reurb), Áreas de Especial Interesse Turístico (AEIT) e Áreas de Especial Interesse Urbanístico (AEIU).'
    ),
    (
        'carta_10_viario_sede_2026',
        'Carta X: Sistema Viário e Drenagem - Sede (Plano Diretor 2026)',
        'CARTA X - PROPOSTAS DO SISTEMA VIÁRIO E DE DRENAGEM - SEDE - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_10_sistema_viario_drenagem_sede.pdf',
        '1:12.500 (Indicada)',
        276700.0, 286000.0, 7389800.0, 7402600.0,
        '[[-23.58853, -47.18916], [-23.47295, -47.09810]]',
        'Propostas do Sistema Viário Estruturador e Bacias de Retenção de Macrodrenagem no Distrito Sede.'
    ),
    (
        'carta_11_viario_maylasky_2026',
        'Carta XI: Sistema Viário e Drenagem - Maylasky (Plano Diretor 2026)',
        'CARTA XI - PROPOSTAS DO SISTEMA VIÁRIO E DE DRENAGEM - MAYLASKY - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_11_sistema_viario_drenagem_maylasky.pdf',
        '1:12.500 (Indicada)',
        285500.0, 301400.0, 7379900.0, 7394300.0,
        '[[-23.67791, -47.09913], [-23.54788, -46.94378]]',
        'Diretrizes viárias estruturais e canais de drenagem de Maylasky ao longo da ferrovia e da SP-274.'
    ),
    (
        'carta_12_viario_canguera_2026',
        'Carta XII: Sistema Viário e Drenagem - Canguera (Plano Diretor 2026)',
        'CARTA XII - PROPOSTAS DO SISTEMA VIÁRIO E DE DRENAGEM - CANGUERA - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_12_sistema_viario_drenagem_canguera.pdf',
        '1:12.500 (Indicada)',
        265500.0, 281400.0, 7381300.0, 7395700.0,
        '[[-23.66545, -47.29555], [-23.53541, -47.14019]]',
        'Diretrizes viárias, ciclovias turísticas e macrodrenagem de Canguera na Bacia de Itupararanga.'
    ),
    (
        'carta_13_obras_prioritarias_2026',
        'Carta XIII: Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (Plano Diretor 2026)',
        'CARTA XIII - INTERVENÇÕES E OBRAS PRIORITÁRIAS (SRQ-01 A SRQ-22) - REVISÃO 05 (AGÔSTO/2026)',
        'Planejamento Urbano e Ordenamento Territorial',
        'minuta_pd2026/desmembrado/02_cartas_tecnicas/carta_13_intervencoes_obras_prioritarias_srq01_srq22.pdf',
        '1:25.000 (Indicada)',
        268500.0, 290600.0, 7382000.0, 7408800.0,
        '[[-23.65394, -47.20889], [-23.41153, -46.99093]]',
        'Mapeamento georreferenciado das 22 Obras Estruturantes Prioritárias SRQ-01 a SRQ-22 (anéis viários, pontes, contenções de encostas e desassoreamento).'
    )
]

for m in sheets_meta:
    cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais (
        id, nome, titulo_documento, categoria, arquivo_origem,
        tipo_camada, escala_nominal, datum_projecao, data_elaboracao,
        responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
        fonte_cartografica, status_auditoria,
        bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
        bounds_wgs84_json, alerta_juridico
    ) VALUES (
        ?, ?, ?, ?, ?,
        'Cartografia Temática Oficial / Raster Georreferenciado', ?, 'SIRGAS 2000 / UTM Zone 23S (EPSG:31983)', 'Agosto/2026',
        'David de Mello Berger (Engenheiro Civil)', 'CREA: 5070025188 (Chefe de Divisão de Engenharia)',
        'Departamento de Planejamento e Meio Ambiente (DPMA)', 'Prefeitura da Estância Turística de São Roque',
        'Minuta de Revisão da LC nº 40/2006 e LC nº 39/2006 (Agosto/2026 - Revisão 05)', 'HOMOLOGADO_AUDITADO',
        ?, ?, ?, ?,
        ?, ?
    )
    """, (m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], m[9], m[10], m[11]))

con.commit()
con.close()
print("Banco sao_roque_geodados.db atualizado com sucesso com Cartas 08 a 13!")
