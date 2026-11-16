import sqlite3

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM erros_embasados_plano_diretor WHERE id = 'erro_4_7'")
r = cursor.fetchone()
for k in r.keys():
    print(f"--- {k} ---")
    print(r[k])

conn.close()
