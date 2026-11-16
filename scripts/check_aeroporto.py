import sqlite3

conn = sqlite3.connect("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db")
cur = conn.cursor()

cur.execute("""
    SELECT camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, artigo_dispositivo, regra_aplicacao 
    FROM cruzamento_camada_legislacao 
    WHERE camada_id LIKE '%aero%' OR classe_id LIKE '%aero%' OR classe_id LIKE '%catarina%' OR classe_id = 'ZUCAer'
""")
rows = cur.fetchall()
print(f"Cruzamentos Aeronáuticos e ZUCAer ({len(rows)}):")
for r in rows:
    print(" -", r)
conn.close()
