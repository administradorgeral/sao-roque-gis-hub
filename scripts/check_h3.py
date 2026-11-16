import sqlite3
import json

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(zonas_plano_diretor)")
print("Colunas de zonas_plano_diretor:", [r['name'] for r in cursor.fetchall()])

cursor.execute("PRAGMA table_info(h3_cells_r8)")
print("Colunas de h3_cells_r8:", [r['name'] for r in cursor.fetchall()])

cursor.execute("SELECT COUNT(*) as cnt FROM h3_cells_r8")
print(f"Total de células H3 no município: {cursor.fetchone()['cnt']}")

cursor.execute("SELECT * FROM h3_cells_r8 LIMIT 3")
for r in cursor.fetchall():
    print(dict(r))

conn.close()
