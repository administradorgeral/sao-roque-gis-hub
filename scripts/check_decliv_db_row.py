import sqlite3

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM camadas WHERE id='declividade' OR arquivo_pdf LIKE '%Declividade%'")
row = cursor.fetchone()
if row:
    print("CAMADA DECLIVIDADE:")
    for k in row.keys():
        print(f"  {k}: {row[k]}")
else:
    print("Não encontrado em camadas")

cursor.execute("SELECT * FROM conhecimento_espacial_camadas WHERE camada_id='declividade'")
row_c = cursor.fetchone()
if row_c:
    print("\nCONHECIMENTO ESPACIAL DECLIVIDADE:")
    for k in row_c.keys():
        print(f"  {k}: {row_c[k]}")
else:
    print("Não encontrado em conhecimento_espacial_camadas")

conn.close()
