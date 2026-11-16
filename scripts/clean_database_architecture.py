import sqlite3
import shutil
import os

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
bak_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db.bak_orig'

# 1. Fazer backup seguro do banco antes de qualquer alteração
if not os.path.exists(bak_path):
    shutil.copy2(db_path, bak_path)
    print(f"Backup de seguranca criado em: {bak_path}")
else:
    print(f"Backup ja existe em: {bak_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelas a preservar (LEIS E ÍNDICES TEXTUAIS VÁLIDOS)
preserve = [
    'normas_juridicas',
    'artigos_dispositivos',
    'normas_fts',
    'normas_fts_data',
    'normas_fts_idx',
    'normas_fts_content',
    'normas_fts_docsize',
    'normas_fts_config'
]

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [r[0] for r in cursor.fetchall()]

# Remover tabelas contaminadas do antigo projeto
dropped = []
for t in all_tables:
    if t not in preserve and not t.startswith('sqlite_'):
        cursor.execute(f"DROP TABLE IF EXISTS \"{t}\"")
        dropped.append(t)

print(f"Tabelas contaminadas removidas ({len(dropped)}): {dropped}")

# 2. Criar tabelas limpas e modernas para o novo projeto de camadas territoriais
cursor.execute("""
CREATE TABLE IF NOT EXISTS camadas_territoriais (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    titulo_documento TEXT NOT NULL,
    categoria TEXT NOT NULL,
    arquivo_origem TEXT NOT NULL,
    tipo_camada TEXT NOT NULL, -- 'vetor_poligonos', 'mvt_tiles', 'raster'
    escala_nominal TEXT NOT NULL,
    datum_projecao TEXT NOT NULL,
    data_elaboracao TEXT NOT NULL,
    responsavel_tecnico TEXT NOT NULL,
    responsavel_crea TEXT NOT NULL,
    desenho_tecnico TEXT NOT NULL,
    desenho_crea TEXT NOT NULL,
    fonte_cartografica TEXT NOT NULL,
    status_auditoria TEXT NOT NULL,
    bbox_utm_x0 REAL,
    bbox_utm_x1 REAL,
    bbox_utm_y0 REAL,
    bbox_utm_y1 REAL,
    bounds_wgs84_json TEXT,
    alerta_juridico TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS classes_camada_territorial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camada_id TEXT NOT NULL,
    codigo_classe TEXT NOT NULL,
    nome_classe TEXT NOT NULL,
    angulo_equivalente TEXT,
    cor_hex TEXT NOT NULL,
    cor_rgb TEXT NOT NULL,
    metodologia_referencia TEXT NOT NULL, -- ex: 'Lepsch (1983) / Embrapa Pedologia'
    implicacao_pratica TEXT NOT NULL,
    FOREIGN KEY (camada_id) REFERENCES camadas_territoriais(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cruzamento_camada_legislacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    camada_id TEXT NOT NULL,
    classe_id INTEGER,
    norma_esfera TEXT NOT NULL, -- 'Federal', 'Estadual', 'Municipal'
    norma_tipo TEXT NOT NULL,
    norma_numero TEXT NOT NULL,
    norma_ano INTEGER,
    artigo_dispositivo TEXT NOT NULL,
    grau_restricao TEXT NOT NULL, -- 'Impeditiva', 'Condicionante', 'Incentivo'
    regra_aplicacao TEXT NOT NULL,
    conflito_ou_ponto_atencao TEXT,
    FOREIGN KEY (camada_id) REFERENCES camadas_territoriais(id),
    FOREIGN KEY (classe_id) REFERENCES classes_camada_territorial(id)
)
""")

conn.commit()

# Verificar tabelas finais
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
final_tables = [r[0] for r in cursor.fetchall()]
print(f"Tabelas finais limpas no banco ({len(final_tables)}): {final_tables}")

# Contagem de leis preservadas
cursor.execute("SELECT COUNT(*) FROM normas_juridicas")
print(f"Total de Leis Oficiais preservadas: {cursor.fetchone()[0]}")
cursor.execute("SELECT COUNT(*) FROM artigos_dispositivos")
print(f"Total de Artigos preservados: {cursor.fetchone()[0]}")

conn.close()
