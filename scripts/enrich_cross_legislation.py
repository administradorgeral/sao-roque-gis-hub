import sqlite3

print("=== ATRELAMENTO JURÍDICO INTEGRAL: CAMADAS x LEGISLAÇÃO ===")

db_path = r"dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Novos cruzamentos estruturados
novos_cruzamentos = [
    # --- ZONEAMENTO HOMOLOGADO (PMD 2006) ---
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 15 a 18', 'Diretriz Estratégica', 
     'Define o Macrozoneamento Municipal da Estância Turística de São Roque, dividindo o território em Zona Urbana, Zona de Expansão Urbana e Zona Rural.', 
     'VINCULAÇÃO ESTRUTURAL: A LC 40/06 não pode ser interpretada sem os objetivos e diretrizes da LC 39/06 (Plano Diretor Estratégico).'),
    
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 58 e seguintes', 'Condicionante', 
     'Institui os instrumentos da política urbana do Estatuto da Cidade em São Roque: Outorga Onerosa do Direito de Construir, IPTU Progressivo e ZEIS.', 
     'Aplicável diretamente às zonas urbanas ZU e zonas de expansão para fins de regularização fundiária e adensamento.'),
    
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '40', 2006, 'Art. 1º ao 12', 'Regulamentadora', 
     'Institui o Zoneamento de Uso e Ocupação do Solo, discriminando as 31 Zonas Territoriais e seus parâmetros de uso permitido, permissível e proibido.', 
     'Tabela de Usos e Incomodidades (Anexo da LC 40/06).'),
     
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '41', 2006, 'Art. 1º e 2º', 'Condicionante', 
     'Código de Obras e Edificações do Município de São Roque: disciplina os recuos frontais, laterais, taxa de permeabilidade e vagas de garagem em cada zona.', 
     'Deve ser consultado em conjunto com a LC 40/06 para aprovação de qualquer projeto arquitetônico ou construtivo.'),
     
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '99', 2018, 'Art. 40-A a 40-D', 'Regulamentadora', 
     'Altera a LC 40/2006 criando e disciplinando as regras de desdobro e desmembramento de glebas urbanas e rurais no município de São Roque.', 
     'Critérios mínimos de testada e área para divisão de lotes consolidados.'),
     
    ('zoneamento', None, 'Municipal', 'Lei Complementar', '120', 2022, 'Art. 10-A', 'Impeditiva', 
     'Fixa limites máximos de densidade construtiva e gabarito de altura em zonas lindeiras à malha ferroviária e corredores turísticos.', 
     'Restrição de altura e impacto de vizinhança.'),
     
    ('zoneamento', None, 'Federal', 'Lei Ordinária', '10257', 2001, 'Art. 39 a 42', 'Diretriz Estratégica', 
     'Estatuto da Cidade: vincula a obrigatoriedade do Plano Diretor e determina que o zoneamento municipal cumpra a função social da propriedade urbana.', 
     'Matriz federal que rege a validade de todos os instrumentos das LCs 39 e 40/2006.'),

    # --- DECLIVIDADE ---
    ('declividade', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 18', 'Diretriz Estratégica', 
     'Estabelece a diretriz de prevenção de áreas de risco geológico-geotécnico e veda a ocupação desordenada de encostas e topos de morro.', 
     'Compatibilização com o mapa de declividade para direcionar o crescimento urbano para relevos mais suaves.'),
     
    ('declividade', None, 'Federal', 'Lei Ordinária', '12608', 2012, 'Art. 22', 'Impeditiva', 
     'Política Nacional de Proteção e Defesa Civil (PNPDEC): proíbe a concessão de licença ou alvará de construção em áreas com risco de desastre geológico ou declividade crítica sem laudo favorável.', 
     'Responsabilidade solidária do município em caso de licenciamento em área de risco.'),

    # --- MDT (HIPSOMETRIA) ---
    ('mdt', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 22 e 23', 'Diretriz Estratégica', 
     'Proteção do patrimônio paisagístico natural e monumentos geográficos de São Roque, com ênfase na preservação da silhueta visual do Morro do Saboó e Morro do Cruzeiro.', 
     'Restrições de gabarito para não obstruir visuais panorâmicas de topos de morro.'),
     
    ('mdt', None, 'Judiciário Federal (STF)', 'Acórdão STF', 'ADPF 747/749', 2021, 'Art. 102 CF/88 (Efeito Vinculante)', 'Impeditiva / Vinculante', 
     'Julgamento do STF que declarou a inconstitucionalidade da Resolução CONAMA 500/2020 e restabeleceu os critérios da Resolução CONAMA 303/2002 para proteção de topos de morro como APP.', 
     'Vinculação absoluta: topos de morro com altura mínima de 100m e inclinação média > 17° têm APP no seu terço superior.'),

    # --- HIDROGRAFIA ---
    ('hidrografia', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 60 a 64', 'Impeditiva', 
     'Institui as Zonas de Proteção aos Mananciais (ZPM) e Zonas Especiais de Preservação Ambiental (ZEPA) em torno das represas e bacias de abastecimento público de São Roque.', 
     'Exigência de taxas máximas de impermeabilização do solo mais restritivas (máx. 20%) nas bacias de mananciais.'),
     
    ('hidrografia', None, 'Estadual', 'Lei Ordinária', '11579', 2003, 'Art. 1º e seguintes', 'Impeditiva', 
     'Cria a Área de Proteção Ambiental (APA) da Represa de Itupararanga, impondo zoneamento ecológico-econômico e restrições específicas para ocupação em toda a bacia formadora.', 
     'Incide diretamente sobre todo o sudoeste e sul do território de São Roque (bacias do Rio Sorocabuçu e Sorocamirim).'),
     
    ('hidrografia', None, 'Federal', 'Resolução CONAMA', '357', 2005, 'Art. 4º', 'Condicionante', 
     'Classificação das águas doces em classes (Especial, 1, 2, 3 e 4) e padrões de lançamento de efluentes tratados.', 
     'Mananciais de abastecimento de São Roque enquadrados como Classe Especial / Classe 1.'),

    # --- GEOMORFOLÓGICO ---
    ('geomorfologico', None, 'Municipal', 'Lei Complementar', '39', 2006, 'Art. 18 e 19', 'Diretriz Estratégica', 
     'Condiciona a expansão urbana à aptidão do meio físico e compartimentos geomorfológicos, priorizando o Planalto Paulistano e impondo restrições severas no Planalto de Jundiaí (Serras).', 
     'Orientação geotécnica para obras de infraestrutura e viárias.'),
     
    ('geomorfologico', None, 'Municipal', 'Lei Complementar', '40', 2006, 'Art. 13 e 43', 'Impeditiva', 
     'Vedação ao parcelamento e condomínios em áreas geologicamente instáveis ou em escarpas de falha.', 
     'Exigência de estabilização mecânica e vegetal em cortes do Maciço São Roque (Planalto de Ibiúna).'),
     
    ('geomorfologico', None, 'Federal', 'Lei Ordinária', '12608', 2012, 'Art. 22', 'Condicionante', 
     'Exigência de carta geotécnica de aptidão à urbanização para elaboração e revisão do Plano Diretor Municipal.', 
     'O mapa geomorfológico do PDA 2019 cumpre este requisito legal obrigatório da PNPDEC.')
]

# Remover cruzamentos prévios de zoneamento e geomorfologico para evitar duplicatas
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id IN ('zoneamento', 'geomorfologico')")

for row in novos_cruzamentos:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, classe_id, norma_esfera, norma_tipo, norma_numero,
        norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao,
        conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

total = c.execute("SELECT count(*) FROM cruzamento_camada_legislacao").fetchone()[0]
print(f"Total de cruzamentos legislativos registrados no SQLite: {total}")

print("\n--- DISTRIBUIÇÃO POR CAMADA ---")
for r in c.execute("SELECT camada_id, count(*) FROM cruzamento_camada_legislacao GROUP BY camada_id").fetchall():
    print(f"  Camada '{r[0]}': {r[1]} normas jurídicas vinculadas")

conn.close()
print("\n=== ATRELAMENTO CONCLUÍDO COM SUCESSO! ===")
