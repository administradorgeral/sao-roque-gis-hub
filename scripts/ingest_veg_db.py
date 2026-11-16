import sqlite3
import json

db_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== INGESTÃO DA CAMADA DE VEGETAÇÃO NATIVA ARBÓREA NO BANCO DE DADOS OFICIAL ===")

# 0. Inserir Resolução CONAMA 1/1994 em normas_juridicas se não existir
cur.execute("""
    INSERT OR IGNORE INTO normas_juridicas 
    (id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, texto_integral, camadas_competencia)
    VALUES (
        'RES_CONAMA_1_1994',
        'Federal',
        'Resolução CONAMA',
        '1',
        1994,
        'Conselho Nacional do Meio Ambiente (CONAMA)',
        'Define as características básicas da vegetação primária e dos estágios sucessionais secundários (inicial, médio e avançado) da Mata Atlântica para o Estado de São Paulo.',
        'Em Vigor',
        'http://conama.mma.gov.br/',
        'Resolução CONAMA nº 1, de 31 de janeiro de 1994. Define vegetação primária e estágios sucessionais secundários da Mata Atlântica no Estado de São Paulo para fins de aplicação da legislação ambiental e procedimentos de licenciamento florestal.',
        'vegetacao_arborea,zoneamento_ambiental'
    )
""")

# 1. Inserir em camadas_territoriais
cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais 
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (
        'vegetacao_arborea',
        'Vegetação Nativa Arbórea (Mata Atlântica)',
        'MAPA DE VEGETAÇÃO FLORESTAL NATIVA DO MUNICÍPIO DE SÃO ROQUE',
        'Cobertura Vegetal e Biodiversidade',
        '34218_5_3_2_1_1 Vegetação Nativa arbórea.pdf',
        'vetor_poligonos',
        '1:35.000',
        'SIRGAS 2000 UTM Zone 23S',
        '15/01/2019',
        'Maurício Scorsatto Sartori (Eng. Florestal)',
        'CREA: 5.060.532.187',
        'Ana Clara Cerminaro (Analista de Geoprocessamento)',
        'CREA: 473.423.455',
        'IGC 1:10.000 (1978), Código Florestal (Lei 12.651/12), SPOT 1,5m (2016) e PDA 2019',
        'Auditado e Dissolvido Contínuo (1.275 Polígonos Nativos Dissolvidos / 15.613,05 ha / 50,85% do Território)',
        274626.28,
        296740.16,
        7382541.32,
        7409302.03,
        '[[-23.65395, -47.20890], [-23.41215, -46.99182]]',
        '🌳 BIOMA MATA ATLÂNTICA E PATRIMÔNIO NATURAL: A vegetação nativa arbórea cobre 15.613,05 ha (50,85% de São Roque), sendo 15.145,72 ha em Estágio Avançado e Médio (49,33%) e 467,33 ha em Estágio Inicial (1,52%). A supressão é estritamente vedada para loteamentos urbanos em maciços primários e encostas, nos termos da Lei Federal nº 11.428/2006 (Lei da Mata Atlântica), Decreto Federal nº 6.660/2008 e LC nº 39/2006.'
    )
""")

# 2. Inserir classes em classes_camada_territorial
cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'vegetacao_arborea',
        'VN_AVANCADO_MEDIO',
        'Vegetação Nativa Arbórea em Estágio Avançado e Médio',
        'Maciços Florestais Secundários em Estágio Médio e Avançado',
        '#267300',
        'RGB(38, 115, 0)',
        'Lei da Mata Atlântica (Lei 11.428/06) / Decreto 6.660/08 / Resolução CONAMA 1/94',
        '15.145,72 ha (49,33% do município). Proteção absoluta contra corte e parcelamento predatório. Supressão admitida apenas para utilidade pública ou interesse social com autorização expressa da CETESB e compensação ambiental gravada em matrícula.'
    )
""")

cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'vegetacao_arborea',
        'VN_INICIAL',
        'Vegetação Nativa Arbórea em Estágio Inicial',
        'Capoeiras e Regeneração Florestal Inicial',
        '#55FF00',
        'RGB(85, 255, 0)',
        'Lei da Mata Atlântica (Lei 11.428/06 Art. 25) / Decreto 6.660/08',
        '467,33 ha (1,52% do município). Área em regeneração ecológica. Supressão depende de autorização do órgão ambiental competente com preservação da conectividade de fragmentos florestais.'
    )
""")

# 3. Inserir Cruzamentos Legislativos em cruzamento_camada_legislacao
cruzamentos_veg = [
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Federal", "Lei Ordinária", "11428", 2006, "Arts. 11, 14 e 21", "Impeditiva / Restritiva", "Proibição de corte e supressão de vegetação primária e secundária em estágio avançado e médio de regeneração da Mata Atlântica.", "Exceção exclusiva para obras de utilidade pública com laudo da CETESB."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Federal", "Decreto Federal", "6660", 2008, "Arts. 3º a 7º e 23", "Regulamentação Técnica", "Critérios fisionômicos, estratificação e espécies indicadoras para classificação dos estágios sucessionais da Mata Atlântica.", "Vedada descaracterização de fragmentos florestais urbanos e rurais."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Federal", "Resolução CONAMA", "1", 1994, "Arts. 1º a 6º", "Parâmetros Fitossociológicos", "Fixa as características básicas dos estágios de regeneração da vegetação da Mata Atlântica no Estado de São Paulo.", "Classificação vinculante para laudos florestais, perícias ambientais e licenciamento junto à CETESB."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Federal", "Lei Ordinária", "12651", 2012, "Arts. 4º e 12", "Condicionante / Obrigatória", "Obrigação de manutenção de Reserva Legal (20%) e APPs com cobertura vegetal nativa.", "Inscrição obrigatória no Cadastro Ambiental Rural (CAR)."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Estadual", "Lei Ordinária", "11579", 2003, "Arts. 2º e 3º", "APA de Itupararanga", "Proteção dos remanescentes florestais que compõem a bacia formadora da Represa de Itupararanga.", "Anuência prévia da Fundação Florestal e vedação a parcelamentos que fragmentem o dossel."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Sistema de Áreas Verdes", "Plano Diretor estabelecendo as florestas nativas como infraestrutura verde estruturante do ecoturismo e recarga hídrica.", "Restrições severas de ocupação nas encostas e cabeceiras de drenagem."),
    ("vegetacao_arborea", "VN_AVANCADO_MEDIO", "Municipal", "Lei Complementar", "140", 2025, "Arts. 1º a 3º", "Diretrizes de Ecoturismo", "Plano Diretor de Turismo (PDTur) ancorando a vocação de Estância Turística na integridade da paisagem florestal e rotas cênicas.", "Preservação da visada panorâmica das serras e morros do município."),
    ("vegetacao_arborea", "VN_INICIAL", "Federal", "Lei Ordinária", "11428", 2006, "Art. 25", "Autorizativa / Condicionante", "O corte e a supressão de vegetação secundária em estágio inicial dependem de autorização prévia fundamentada.", "Exigência de compensação florestal e preservação de corredores de fauna.")
]

for cr in cruzamentos_veg:
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
    print("FTS index rebuilt com as normas de vegetação nativa.")
except Exception as e:
    print("FTS note:", e)

cur.execute("SELECT COUNT(*) FROM camadas_territoriais")
print("Total Camadas Territoriais:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM classes_camada_territorial")
print("Total Classes Cadastradas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao")
print("Total Cruzamentos:", cur.fetchone()[0])

conn.close()
print("=== BASE DE DADOS SINCRONIZADA COM VEGETAÇÃO NATIVA ARBÓREA! ===")
