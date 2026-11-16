import sqlite3

conn = sqlite3.connect("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db")
cur = conn.cursor()

# Check FTS count
cur.execute("SELECT COUNT(*) FROM normas_fts")
print("normas_fts count:", cur.fetchone()[0])

# Check how normas_fts is structured
cur.execute("PRAGMA table_info(normas_fts)")
cols = [c[1] for c in cur.fetchall()]
print("normas_fts cols:", cols)

# Search for turismo
try:
    cur.execute("SELECT * FROM normas_fts WHERE normas_fts MATCH 'turismo' LIMIT 5")
    rows = cur.fetchall()
    print("Matches for 'turismo':", len(rows))
    for r in rows:
        print(" -", r[0], r[1])
except Exception as e:
    print("FTS error:", e)

# If needed, rebuild FTS
try:
    cur.execute("INSERT INTO normas_fts(normas_fts) VALUES('rebuild')")
    conn.commit()
    print("FTS index rebuilt successfully.")
except Exception as e:
    print("FTS rebuild note:", e)

cur.execute("SELECT COUNT(*) FROM normas_fts WHERE normas_fts MATCH 'turismo'")
print("Matches after rebuild:", cur.fetchone()[0])
conn.close()
