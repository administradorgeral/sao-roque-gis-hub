import sqlite3

conn = sqlite3.connect(r'dados_oficiais/sao_roque_geodados.db')
cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print('Tables in sao_roque_geodados.db:')
for t in tables:
    count = cursor.execute(f"SELECT count(*) FROM {t[0]}").fetchone()[0]
    print(f'  {t[0]}: {count} records')

print('\nChecking camadas_territoriais:')
cols = [c[1] for c in cursor.execute("PRAGMA table_info(camadas_territoriais);").fetchall()]
print(f'Columns: {cols}')
for row in cursor.execute('SELECT * FROM camadas_territoriais').fetchall():
    print(f'  {row}')

conn.close()
