import sqlite3

conn = sqlite3.connect('dados_oficiais/sao_roque_geodados.db')
c = conn.cursor()

print('=== NORMAS JURÍDICAS MUNICIPAIS ===')
rows = c.execute("SELECT id, tipo, numero, ano, ementa FROM normas_juridicas WHERE esfera = 'Municipal'").fetchall()
print(f'Total Leis Municipais: {len(rows)}')
for r in rows:
    print(f"  {r[0]} | {r[1]} nº {r[2]}/{r[3]}: {r[4][:80]}")

print('\n=== NORMAS JURÍDICAS FEDERAIS E ESTADUAIS ===')
fed_rows = c.execute("SELECT id, esfera, tipo, numero, ano, ementa FROM normas_juridicas WHERE esfera != 'Municipal'").fetchall()
print(f'Total Federais/Estaduais: {len(fed_rows)}')
for r in fed_rows:
    print(f"  {r[0]} | {r[1]} {r[2]} nº {r[3]}/{r[4]}: {r[5][:80]}")

print('\n=== CRUZAMENTOS ATUAIS CAMADA x LEGISLAÇÃO ===')
cross = c.execute("""
    SELECT c.camada_id, n.numero, n.ano, n.tipo, n.esfera, c.artigo, c.relevancia 
    FROM cruzamento_camada_legislacao c
    LEFT JOIN normas_juridicas n ON c.norma_id = n.id
""").fetchall()
print(f'Total Cruzamentos: {len(cross)}')
for cr in cross:
    print(f"  Camada '{cr[0]}' -> {cr[4]} {cr[3]} nº {cr[1]}/{cr[2]} (Art. {cr[5]}): {cr[6]}")

conn.close()
