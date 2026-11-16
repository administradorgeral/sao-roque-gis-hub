import sqlite3

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

for t in ['camadas', 'conhecimento_espacial_camadas', 'setores_risco_geo']:
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [r['name'] for r in cursor.fetchall()]
    print(f"Colunas de {t}: {cols}")
    cursor.execute(f"SELECT * FROM {t} LIMIT 2")
    for row in cursor.fetchall():
        print(dict(row))
    print()

conn.close()
