import sqlite3
import json

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("--- REGISTROS EM 'camadas' ---")
cursor.execute("SELECT id_camada, nome, categoria, tipo_geometria FROM camadas")
for r in cursor.fetchall():
    print(dict(r))

print("\n--- REGISTROS EM 'conhecimento_espacial_camadas' ---")
cursor.execute("SELECT id_camada, descricao_espacial, normas_aplicaveis, palavras_chave FROM conhecimento_espacial_camadas LIMIT 5")
for r in cursor.fetchall():
    print(dict(r))

print("\n--- REGISTROS EM 'setores_risco_geo' ---")
cursor.execute("SELECT * FROM setores_risco_geo")
for r in cursor.fetchall():
    print(dict(r))

conn.close()
