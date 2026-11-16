import sqlite3

conn = sqlite3.connect("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db")
cur = conn.cursor()

cur.execute("SELECT * FROM classes_camada_territorial WHERE camada_id LIKE '%apa%'")
rows = cur.fetchall()
col_names = [d[0] for d in cur.description]
print("Columns:", col_names)
for r in rows:
    print(dict(zip(col_names, r)))
