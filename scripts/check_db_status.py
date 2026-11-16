import sqlite3

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== CAMADAS TERRITORIAIS ATIVAS NO BANCO ===")
cursor.execute("SELECT id, nome, categoria, escala_nominal, tipo_camada, status_auditoria FROM camadas_territoriais")
for r in cursor.fetchall():
    print(dict(r))

print("\n=== TOTAL DE CLASSES POR CAMADA ===")
cursor.execute("SELECT camada_id, COUNT(*) as n_classes FROM classes_camada_territorial GROUP BY camada_id")
for r in cursor.fetchall():
    print(dict(r))

print("\n=== TOTAL DE CRUZAMENTOS LEGAIS POR CAMADA ===")
cursor.execute("SELECT camada_id, COUNT(*) as n_leis FROM cruzamento_camada_legislacao GROUP BY camada_id")
for r in cursor.fetchall():
    print(dict(r))

cursor.execute("SELECT camada_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao FROM cruzamento_camada_legislacao")
for r in cursor.fetchall():
    print(f"[{r['camada_id'].upper()}] {r['norma_esfera']} - {r['norma_tipo']} {r['norma_numero']}/{r['norma_ano']} ({r['artigo_dispositivo']}) -> Restrição: {r['grau_restricao']}")

conn.close()
