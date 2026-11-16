import sqlite3

conn = sqlite3.connect("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db")
cur = conn.cursor()

# Ensure classes for apa_itupararanga_limite
cur.execute("SELECT codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica FROM classes_camada_territorial WHERE camada_id = 'apa_itupararanga'")
rows = cur.fetchall()

for r in rows:
    cur.execute("""
        INSERT OR IGNORE INTO classes_camada_territorial 
        (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
        VALUES ('apa_itupararanga_limite', ?, ?, ?, ?, ?, ?, ?)
    """, r)

# Ensure cruzamento for apa_itupararanga_limite
cur.execute("SELECT classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao FROM cruzamento_camada_legislacao WHERE camada_id = 'apa_itupararanga'")
cruz_rows = cur.fetchall()

for cr in cruz_rows:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao 
        (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
        SELECT 'apa_itupararanga_limite', ?, ?, ?, ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM cruzamento_camada_legislacao 
            WHERE camada_id = 'apa_itupararanga_limite' AND classe_id = ? AND norma_numero = ? AND artigo_dispositivo = ?
        )
    """, cr + (cr[0], cr[3], cr[5]))

conn.commit()

cur.execute("SELECT COUNT(*) FROM classes_camada_territorial WHERE camada_id LIKE '%apa%'")
print("Classes for apa:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao WHERE camada_id LIKE '%apa%'")
print("Cruzamentos for apa:", cur.fetchone()[0])
conn.close()
