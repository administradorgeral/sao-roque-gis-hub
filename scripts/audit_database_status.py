import sqlite3

conn = sqlite3.connect('dados_oficiais/sao_roque_geodados.db')
c = conn.cursor()

print("=== AUDITORIA DO BANCO DE DADOS ===")
c.execute("SELECT id, nome, status_auditoria FROM camadas_territoriais")
for row in c.fetchall():
    print(f"Camada: {row[0]} | {row[1]} | {row[2]}")

c.execute("SELECT count(*) FROM classes_camada_territorial")
print(f"\nTotal de Classes de Camadas: {c.fetchone()[0]}")

c.execute("SELECT count(*) FROM cruzamento_camada_legislacao")
print(f"Total de Vinculações Normativas: {c.fetchone()[0]}")

print("\nClasses do Pedológico:")
c.execute("SELECT codigo_classe, nome_classe, cor_hex, implicacao_pratica FROM classes_camada_territorial WHERE camada_id = 'pedologico'")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]} ({row[2]}) -> {row[3][:60]}...")

print("\nLeis vinculadas ao Pedológico:")
c.execute("SELECT norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao FROM cruzamento_camada_legislacao WHERE camada_id = 'pedologico'")
for row in c.fetchall():
    print(f"  [{row[0]}] {row[1]} {row[2]}/{row[3]} ({row[4]}): {row[5]}")

conn.close()
