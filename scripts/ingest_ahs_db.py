import sqlite3
import json

db_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== INGESTÃO DA CAMADA AHS NO BANCO DE DADOS OFICIAL ===")

# 1. Inserir em camadas_territoriais
cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais 
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (
        'ahs',
        'Áreas Hidrologicamente Sensíveis (AHS)',
        'MAPA DE ÁREAS HIDROLOGICAMENTE SENSÍVEIS DO MUNICÍPIO DE SÃO ROQUE',
        'Recursos Hídricos e Proteção Ambiental',
        '34229_4.2.5.1-1 AHS.pdf',
        'vetor_poligonos',
        '1:35.000',
        'SIRGAS 2000 UTM Zone 23S',
        '15/01/2019',
        'Maurício Scorsatto Sartori (Eng. Florestal)',
        'CREA: 5.060.532.187',
        'Ana Clara Cerminaro (Analista de Geoprocessamento)',
        'CREA: 473.423.455',
        'IGC 1:10.000 (1978), Código Florestal (Lei 12.651/12), SPOT 1,5m (2016) e PDA 2019',
        'Auditado e Dissolvido Contínuo (7.527 Polígonos Nativos Dissolvidos / 7.514,71 ha)',
        274626.28,
        296740.16,
        7382541.32,
        7409302.03,
        '[[-23.65395, -47.20890], [-23.41215, -46.99182]]',
        '💧 ÁREAS DE PRESERVAÇÃO PERMANENTE E PROTEÇÃO DE MANANCIAIS: As Áreas Hidrologicamente Sensíveis (AHS) abrangem 7.514,71 ha (24,48% de São Roque), compreendendo APPs de nascentes (50m), faixas marginais de rios (30m a 100m) e várzeas de meandro. É terminantemente vedada a ocupação, aterro, impermeabilização ou edificação, sendo obrigatória a regeneração da mata ciliar (Lei Federal nº 12.651/2012 e LC nº 39/2006 Arts. 60-64).'
    )
""")

# 2. Inserir classe em classes_camada_territorial
cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'ahs',
        'AHS_SAO_ROQUE',
        'Áreas Hidrologicamente Sensíveis (AHS)',
        'Zonas Úmidas, APPs Hídricas e Várzeas Aluviais',
        '#A80084',
        'RGB(168, 0, 132)',
        'Código Florestal (Lei 12.651/12) / IGC 1:10.000 / SPOT 1,5m / PDA 2019',
        '7.514,71 ha (24,48% do território municipal). Área de preservação absoluta e recarga de aquíferos. Intervenção admitida apenas em casos excepcionais de utilidade pública ou interesse social com compensação ambiental e outorga do DAEE.'
    )
""")

# 3. Inserir Cruzamentos Legislativos em cruzamento_camada_legislacao
cruzamentos_ahs = [
    ("ahs", "AHS_SAO_ROQUE", "Federal", "Lei Ordinária", "12651", 2012, "Arts. 4º e 6º", "Proteção Absoluta (APP)", "Área de Preservação Permanente (APP) ao longo de cursos d'água (30m a 100m) e nascentes (raio 50m).", "Vedada qualquer supressão de vegetação ou impermeabilização."),
    ("ahs", "AHS_SAO_ROQUE", "Estadual", "Lei Ordinária", "9866", 1997, "Arts. 3º e 4º", "Proteção de Mananciais Regionais", "Diretrizes de proteção e recuperação de bacias de mananciais de abastecimento público no Estado de SP.", "Exigência de esgotamento sanitário estanque e taxa mínima de permeabilidade."),
    ("ahs", "AHS_SAO_ROQUE", "Estadual", "Lei Ordinária", "11579", 2003, "Art. 2º e 3º", "APA Represa de Itupararanga", "Afluentes contribuintes diretos da Represa de Itupararanga na porção sul de São Roque.", "Anuência prévia da Fundação Florestal para qualquer plano de manejo."),
    ("ahs", "AHS_SAO_ROQUE", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Zonas de Proteção de Mananciais", "Plano Diretor Estratégico subordinando o uso do solo à qualidade e recarga das bacias hídricas.", "Restrição severa a parcelamentos e loteamentos adensados."),
    ("ahs", "AHS_SAO_ROQUE", "Municipal", "Lei Complementar", "40", 2006, "Art. 13", "Restrição Geotécnico-Ambiental", "Proibição de loteamentos em terrenos alagadiços e sujeitos a inundações.", "Exigência de laudo hidrológico de macrodrenagem aprovado pelo DAEE."),
    ("ahs", "AHS_SAO_ROQUE", "Federal", "Resolução CONAMA", "357", 2005, "Arts. 1º a 4º", "Classificação Hídrica", "Enquadramento dos corpos hídricos receptores e padrões de lançamento de efluentes.", "Proibição de lançamento de esgoto in natura ou efluentes tóxicos sem tratamento adequado homologado.")
]

for cr in cruzamentos_ahs:
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
    print("FTS index rebuilt com as normas de AHS.")
except Exception as e:
    print("FTS note:", e)

cur.execute("SELECT COUNT(*) FROM camadas_territoriais")
print("Total Camadas Territoriais:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM classes_camada_territorial")
print("Total Classes Cadastradas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao")
print("Total Cruzamentos:", cur.fetchone()[0])

conn.close()
print("=== BASE DE DADOS SINCRONIZADA COM AHS! ===")
