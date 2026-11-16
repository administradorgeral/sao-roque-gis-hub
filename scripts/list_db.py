import sqlite3

conn = sqlite3.connect(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db")
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("Tabelas no banco:")
for t in tables:
    print(f"  {t}")
conn.close()
