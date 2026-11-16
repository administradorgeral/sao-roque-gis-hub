import sqlite3

db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Cruzamentos completos para Geomorfologia (Pirâmide de Precedência Integral)
cruzamentos_geomorf = [
    ('geomorfologico', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 18 e 19', 'Diretriz Estratégica',
     'Condiciona a expansão urbana à aptidão do meio físico e compartimentos geomorfológicos, priorizando o Planalto Paulistano e impondo restrições severas no Planalto de Jundiaí (Serras).',
     'Orientação geotécnica estrutural para obras de infraestrutura viária e loteamentos.'),

    ('geomorfologico', None, 'Municipal', 'Lei Complementar', '40', 2006, 'Art. 13 e 43', 'Impeditiva',
     'Vedação ao parcelamento e condomínios em áreas geologicamente instáveis, escarpas ou com declividade crítica sem laudo geotécnico favorável.',
     'Exigência de obras de estabilização mecânica e vegetal em cortes do Maciço São Roque (Planalto de Ibiúna).'),

    ('geomorfologico', None, 'Municipal', 'Lei Complementar', '41', 2006, 'Art. 25 a 30', 'Condicionante',
     'Código de Obras e Edificações: dimensionamento de muros de arrimo, contenção de encostas e fundações adequadas ao compartimento geomorfológico.',
     'Obrigatória sondagem mecânica de solo prévia à aprovação de projetos construtivos em relevo ondulado ou serrano.'),

    ('geomorfologico', None, 'Estadual', 'Lei Ordinária', '11579', 2003, 'Art. 1º a 8º', 'Impeditiva / Protetiva',
     'Área de Proteção Ambiental (APA) da Represa de Itupararanga: incide sobre o compartimento Planalto de Ibiúna / São Roque, restringindo desmatamento, movimentação de terra e terraplenagem na bacia formadora.',
     'Licenciamento obrigatório perante a CETESB e Fundação Florestal para intervenções no relevo da APA.'),

    ('geomorfologico', None, 'Federal', 'Lei Ordinária', '6766', 1979, 'Art. 3º, parágrafo único, I', 'Impeditiva',
     'Lei Lehmann de Parcelamento do Solo Urbano: veda expressamente o parcelamento em terrenos onde as condições geológicas e morfológicas não aconselhem a edificação.',
     'Matriz federal inderrogável: loteamentos em áreas serranas ou de declive acentuado exigem laudo e obras saneadoras.'),

    ('geomorfologico', None, 'Federal', 'Lei Ordinária', '12608', 2012, 'Art. 22', 'Condicionante',
     'Política Nacional de Proteção e Defesa Civil (PNPDEC): exigência de carta geotécnica de aptidão à urbanização para direcionamento do Plano Diretor e controle de áreas de risco.',
     'O mapeamento dos compartimentos morfoesculturais cumpre este requisito legal obrigatório da PNPDEC.'),

    ('geomorfologico', None, 'Federal', 'Lei Ordinária', '12651', 2012, 'Art. 4º, IX', 'Impeditiva',
     'Código Florestal Federal: estabelece Áreas de Preservação Permanente (APP) em topos de morros, montanhas e cristas estruturais no Planalto de Jundiaí (Morro do Saboó e serras associadas).',
     'Vedada qualquer supressão vegetal ou edificação na faixa do terço superior de morros com altura mínima de 100m.'),

    ('geomorfologico', None, 'Judiciário Federal (STF)', 'Acórdão STF', 'ADPF 747/749', 2021, 'Art. 102 CF/88 (Efeito Vinculante)', 'Impeditiva / Vinculante',
     'Jurisprudência vinculante do Supremo Tribunal Federal que restaurou a proteção integral de topos de morro e cristas estruturais como APP.',
     'Eficácia erga omnes que anula qualquer ato administrativo municipal que autorize parcelamento em cristas serranas.')
]

c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'geomorfologico'")

for row in cruzamentos_geomorf:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero,
        norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao,
        conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

# Verificação completa da tabela
print("=== LEGISLAÇÃO ATUALIZADA NO BANCO DE DADOS OFICIAL ===")
c.execute("SELECT norma_esfera, norma_tipo, norma_numero, artigo_dispositivo, grau_restricao, regra_aplicacao FROM cruzamento_camada_legislacao WHERE camada_id = 'geomorfologico'")
for r in c.fetchall():
    print(f"[{r[0]}] {r[1]} nº {r[2]} ({r[3]}) - Grau: {r[4]}")
    print(f"    Regra: {r[5]}")

total_geral = c.execute("SELECT count(*) FROM cruzamento_camada_legislacao").fetchone()[0]
print(f"\nTotal Geral de Normas Vinculadas no SQLite: {total_geral}")

conn.close()
print("=== BANCO DE DADOS sao_roque_geodados.db 100% ALIMENTADO E SINCRONIZADO! ===")
