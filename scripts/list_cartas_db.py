import sqlite3

con = sqlite3.connect(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db")
cur = con.cursor()
cur.execute("SELECT id, nome FROM camadas_territoriais WHERE id LIKE 'carta_%' ORDER BY id")
rows = cur.fetchall()
print(f"Total de Cartas Oficiais registradas no banco: {len(rows)}")
for r in rows:
    print(f"  {r[0]}: {r[1]}")
con.close()
