import sqlite3
import json

conn = sqlite3.connect('dados_oficiais/sao_roque_geodados.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print(f"Total de tabelas: {len(tables)}")
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    count = cursor.fetchone()[0]
    cursor.execute(f"PRAGMA table_info({t})")
    cols = [c[1] for c in cursor.fetchall()]
    print(f"- {t} ({count} linhas): {', '.join(cols[:6])}")
