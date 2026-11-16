import sqlite3

conn = sqlite3.connect("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db")
cur = conn.cursor()

cur.execute("SELECT camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao FROM cruzamento_camada_legislacao WHERE camada_id LIKE '%apa%'")
rows = cur.fetchall()
print(f"Total rows for apa: {len(rows)}")
for r in rows:
    print(r)
