import sqlite3
import json

db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== TABELAS ESPACIAIS / GEODADOS NO BANCO ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r['name'] for r in cursor.fetchall()]
for t in tables:
    if any(k in t.lower() for k in ['zone', 'geom', 'limite', 'setor', 'camada', 'mapa', 'municipio']):
        cursor.execute(f"SELECT COUNT(*) as cnt FROM {t}")
        cnt = cursor.fetchone()['cnt']
        print(f"Tabela '{t}': {cnt} registros")

# Inspecionar zonas_zoneamento
if 'zonas_zoneamento' in tables:
    cursor.execute("SELECT sigla, nome, geom_geojson FROM zonas_zoneamento LIMIT 3")
    for r in cursor.fetchall():
        print(f"Zona: {r['sigla']} - {r['nome']} (geom len: {len(r['geom_geojson'] if r['geom_geojson'] else '')})")

conn.close()
