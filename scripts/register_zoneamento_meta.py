import sqlite3

conn = sqlite3.connect('dados_oficiais/sao_roque_geodados.db')
c = conn.cursor()

c.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico,
    responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica,
    status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'zoneamento',
    'Zoneamento Municipal Homologado',
    'PLANO DIRETOR ESTATUTÁRIO - MAPA OFICIAL DE ZONEAMENTO (PMD 2006)',
    'Planejamento Urbano e Ordenamento Territorial',
    'pmsr_zoneamento_pmd2006.geojson',
    'vetor_poligonos',
    '1:10.000',
    'SAD 69 / SIRGAS 2000 UTM Zone 23S',
    '18/12/2006',
    'Equipe Técnica PMSR / Plano Diretor Participativo',
    'Órgão Público Municipal',
    'Departamento de Planejamento e Meio Ambiente',
    'PMSR',
    'Cartas Cadastrais PMSR 1:2.000 e Restituição Aerofotogramétrica IGC 1:10.000 (1978)',
    'Auditado e Homologado (Vinculação Indissociável: LC 39/2006 + LC 40/2006 + LC 41/2006 + Estatuto da Cidade)',
    274588.46, 296738.80, 7382467.97, 7409522.28,
    '[[-23.65459, -47.20889], [-23.40957, -46.98802]]',
    '🏛️ VINCULAÇÃO NORMATIVA INDISSOCIÁVEL: O zoneamento homologado não pode ser lido isoladamente pela LC 40/2006. A LC 39/2006 (Plano Diretor Estratégico) fixa o macrozoneamento e os instrumentos urbanísticos obrigatórios do Estatuto da Cidade (Lei Federal 10.257/01), a LC 41/2006 (Código de Obras) dita os recuos e salubridade, a LC 99/2018 regula os desdobros, e a Lei Federal 6.766/79 veda parcelamentos irregulares.'
)
""")

conn.commit()

rows = c.execute("SELECT id, nome, status_auditoria FROM camadas_territoriais").fetchall()
print(f"Total camadas cadastradas em camadas_territoriais: {len(rows)}")
for r in rows:
    print(f"  {r[0]:15} | {r[1]:32} | {r[2][:50]}...")

conn.close()
