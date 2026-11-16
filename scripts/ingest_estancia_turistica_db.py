import sqlite3
import os
import json

db_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=== INGESTÃO LEGISLATIVA E TERRITORIAL NO BANCO DE DADOS OFICIAL ===")

# 1. Registrar a Camada Fixa Matriz em camadas_territoriais
cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais 
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (
        'territorio_municipal',
        'Território Municipal (Estância Turística de São Roque)',
        'DELIMITAÇÃO TERRITORIAL CONTÍNUA E REGIME JURÍDICO DA ESTÂNCIA TURÍSTICA',
        'Planejamento Urbano e Governança Municipal',
        'sao_roque_3550605_setores_CD2022.kmz',
        'vetor_poligonos',
        '1:50.000',
        'SIRGAS 2000 UTM Zone 23S',
        '26/02/2025',
        'IBGE / Prefeitura da Estância Turística de São Roque',
        'Cód. IBGE 3550605',
        'Divisão de Planejamento Territorial e Geoprocessamento',
        'PDTur / LC 140/2025',
        'IBGE Censo Demográfico 2022 (Malha Setorial Contínua Dissolvida 30.701,47 ha)',
        'Auditado e Dissolvido Contínuo (188 Setores Censitários Integrados)',
        274626.28,
        296740.16,
        7382541.32,
        7409302.03,
        '[[-23.65395, -47.20890], [-23.41215, -46.99182]]',
        '🏛️ REGIME JURÍDICO ESPECIAL DE ESTÂNCIA TURÍSTICA: O território integral de São Roque está sujeito a obrigações cogentes do Direito Público paulista (Lei Estadual 6.899/90 e LCE 1.261/15). Exige compatibilização contínua entre o Plano Diretor Estratégico (LC 39/06) e o Plano Diretor de Turismo (LC 140/25, revisado a cada 3 anos), deliberação prévia do COMTUR (Lei 2.871/04) para verbas DADETUR/FUMEST (Art. 146 da Constituição Estadual) e cumprimento de metas de saneamento e capacidade de carga.'
    )
""")

# 2. Registrar classe territorial em classes_camada_territorial
cur.execute("""
    INSERT OR REPLACE INTO classes_camada_territorial 
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (
        'territorio_municipal',
        'TERRITORIO_MUNICIPAL',
        'Município da Estância Turística de São Roque (Território Integral)',
        'Jurisdição Municipal Global',
        '#D4AF37',
        'RGB(212, 175, 55)',
        'IBGE Censo 2022 / Lei Orgânica nº 1.801/90 / Lei Estadual nº 6.899/90 / LCE nº 1.261/15',
        'Área territorial contínua de 30.701,47 ha (307,01 km²). Base de incidência de toda a governança municipal, dotações DADETUR, zoneamento do solo e políticas públicas integradas de turismo e sustentabilidade.'
    )
""")

# Função auxiliar para carregar texto integral de markdown
leg_dir = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/legislacao"
def load_md(filename):
    p = os.path.join(leg_dir, filename)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# 3. Registrar as Novas Normas em normas_juridicas
normas_data = [
    (
        "CE_SP_ART146_180",
        "Estadual",
        "Constituição Estadual",
        "Constituição SP 1989",
        1989,
        "Assembleia Legislativa do Estado de São Paulo (ALESP)",
        "Estabelece o Fundo de Melhoria das Estâncias (Art. 146) e as Diretrizes da Política e Desenvolvimento Urbano (Art. 180) do Estado de São Paulo.",
        "Vigente",
        "https://www.al.sp.gov.br",
        "Constituicao_Estadual_SP_1989_Art146_Art180_Estancias_DADETUR.md",
        load_md("Constituicao_Estadual_SP_1989_Art146_Art180_Estancias_DADETUR.md"),
        json.dumps(["territorio_municipal", "zoneamento", "zoneamento_ambiental_pda2019", "apa_itupararanga"])
    ),
    (
        "LEI_EST_6899_1990",
        "Estadual",
        "Lei Estadual Ordinária",
        "6.899",
        1990,
        "Governo do Estado de São Paulo / ALESP",
        "Transforma em Estância Turística o Município de São Roque, outorgando regime jurídico-administrativo diferenciado.",
        "Vigente",
        "https://www.al.sp.gov.br/norma/39414",
        "Lei_Estadual_6899_1990_Criacao_Estancia_Turistica_Sao_Roque.md",
        load_md("Lei_Estadual_6899_1990_Criacao_Estancia_Turistica_Sao_Roque.md"),
        json.dumps(["territorio_municipal"])
    ),
    (
        "LCE_1261_2015",
        "Estadual",
        "Lei Complementar Estadual",
        "1.261",
        2015,
        "Assembleia Legislativa do Estado de São Paulo (ALESP)",
        "Estabelece condições e requisitos para a classificação de Estâncias e Municípios de Interesse Turístico (Lei-Matriz do Turismo Paulista: PDTur trienal, COMTUR e Ranqueamento).",
        "Vigente",
        "https://www.al.sp.gov.br/norma/174987",
        "LCE_1261_2015_Estatuto_Estancias_Paulistas_DADETUR_PDTur.md",
        load_md("LCE_1261_2015_Estatuto_Estancias_Paulistas_DADETUR_PDTur.md"),
        json.dumps(["territorio_municipal", "zoneamento"])
    ),
    (
        "DEC_EST_65415_2020",
        "Estadual",
        "Decreto Estadual",
        "65.415",
        2020,
        "Secretaria de Turismo e Viagens do Estado de SP (SETUR-SP) / DADETUR",
        "Regulamenta o DADETUR e disciplina a celebração e execução de convênios com as Estâncias Paulistas.",
        "Vigente",
        "https://www.al.sp.gov.br",
        "Decreto_Estadual_65415_2020_Regulamentacao_DADETUR.md",
        load_md("Decreto_Estadual_65415_2020_Regulamentacao_DADETUR.md"),
        json.dumps(["territorio_municipal"])
    ),
    (
        "LEI_ORG_1801_1990",
        "Municipal",
        "Lei Orgânica Municipal",
        "1.801",
        1990,
        "Câmara Municipal da Estância Turística de São Roque",
        "Lei Orgânica do Município da Estância Turística de São Roque, fixando a soberania local, diretrizes de governança e fomento ao turismo.",
        "Vigente",
        "https://www.camarasaoroque.sp.gov.br",
        "Lei_Organica_Sao_Roque_1801_1990_Estancia_Turistica.md",
        load_md("Lei_Organica_Sao_Roque_1801_1990_Estancia_Turistica.md"),
        json.dumps(["territorio_municipal", "zoneamento"])
    ),
    (
        "LC_MUN_94_2018",
        "Municipal",
        "Lei Complementar Municipal",
        "94",
        2018,
        "Prefeitura e Câmara da Estância Turística de São Roque",
        "Institui o Plano Diretor de Desenvolvimento Turístico de São Roque (PDTur) decênio 2018-2028, cumprindo a LCE nº 1.261/2015.",
        "Vigente",
        "https://www.camarasaoroque.sp.gov.br",
        "LC_94_2018_Plano_Diretor_Turismo_Sao_Roque.md",
        load_md("LC_94_2018_Plano_Diretor_Turismo_Sao_Roque.md"),
        json.dumps(["territorio_municipal", "zoneamento"])
    ),
    (
        "LC_MUN_140_2025",
        "Municipal",
        "Lei Complementar Municipal",
        "140",
        2025,
        "Prefeitura e Câmara da Estância Turística de São Roque",
        "Dispõe sobre a Revisão e Atualização Trienal do Plano Diretor de Desenvolvimento Turístico (PDTur), metas trienais, rotas e investimentos DADETUR.",
        "Vigente",
        "https://www.camarasaoroque.sp.gov.br",
        "LC_140_2025_Revisao_Plano_Diretor_Turismo_Sao_Roque.md",
        load_md("LC_140_2025_Revisao_Plano_Diretor_Turismo_Sao_Roque.md"),
        json.dumps(["territorio_municipal", "zoneamento", "apa_itupararanga"])
    ),
    (
        "LEI_MUN_2871_2004",
        "Municipal",
        "Lei Ordinária Municipal",
        "2.871",
        2004,
        "Câmara Municipal da Estância Turística de São Roque",
        "Reestrutura o Conselho Municipal de Turismo - COMTUR, conferindo-lhe caráter consultivo e deliberativo essencial para aplicação de verbas DADETUR.",
        "Vigente",
        "https://www.camarasaoroque.sp.gov.br",
        "Lei_Municipal_2871_2004_COMTUR_Sao_Roque.md",
        load_md("Lei_Municipal_2871_2004_COMTUR_Sao_Roque.md"),
        json.dumps(["territorio_municipal"])
    ),
    (
        "LEI_MUN_4872_2018",
        "Municipal",
        "Lei Ordinária Municipal",
        "4.872",
        2018,
        "Prefeitura e Câmara da Estância Turística de São Roque",
        "Dispõe sobre a obrigatoriedade da presença de Guia de Turismo Regional Cadastur acompanhando grupos e excursões em visitação ao município.",
        "Vigente",
        "https://www.camarasaoroque.sp.gov.br",
        "Lei_Municipal_4872_2018_Guia_Turismo_Cadastur_Sao_Roque.md",
        load_md("Lei_Municipal_4872_2018_Guia_Turismo_Cadastur_Sao_Roque.md"),
        json.dumps(["territorio_municipal"])
    )
]

for n in normas_data:
    cur.execute("""
        INSERT OR REPLACE INTO normas_juridicas 
        (id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, arquivo_integra, texto_integral, camadas_competencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, n)
    print(f"Norma registrada: {n[0]} ({n[1]} - {n[2]} nº {n[3]}/{n[4]})")

# 4. Registrar artigos específicos em artigos_dispositivos
artigos_novos = [
    # Constituição Estadual Art. 146 e 180
    ("CE_SP_ART146_180", "Art. 146", "O Estado manterá um fundo especial de despesa, denominado Fundo de Melhoria das Estâncias, com o objetivo de desenvolver programas de urbanização, melhoria, serviços e preservação do patrimônio ambiental das estâncias.", "Repasse a fundo perdido vinculado a projetos turísticos e aprovação do COMTUR.", "fundo de melhoria das estancias, dadetur, fumest, estancia turistica, repasse"),
    ("CE_SP_ART146_180", "Art. 180", "No estabelecimento de diretrizes e normas relativas ao desenvolvimento urbano, o Estado e os Municípios assegurarão a ordenação do solo, áreas de especial interesse turístico e preservação do patrimônio natural e cênico.", "Função social da propriedade e compatibilização do uso do solo com áreas de interesse turístico.", "politica urbana, uso do solo, patrimonio historico, interesse turistico, plano diretor"),

    # Lei Estadual 6.899/1990
    ("LEI_EST_6899_1990", "Art. 1º", "É transformado em Estância Turística o Município de São Roque.", "Outorga do regime jurídico-administrativo de Estância Turística com acesso a dotações estaduais.", "criacao estancia, sao roque, estatus estancia, regime juridico"),

    # LCE 1.261/2015
    ("LCE_1261_2015", "Art. 2º, VI", "Dispor de Plano Diretor de Turismo, aprovado por lei municipal específica e obrigatoriamente revisado a cada 3 (três) anos.", "Obrigação legal de revisão trienal do PDTur sob pena de perda do status de Estância.", "pdtur, revisao trienal, plano diretor de turismo, requisito legal"),
    ("LCE_1261_2015", "Art. 2º, VII", "Manter em pleno e regular funcionamento o Conselho Municipal de Turismo - COMTUR, composto de forma paritária e multissetorial.", "Gestão participativa e deliberação obrigatória sobre as verbas do DADETUR.", "comtur, conselho municipal de turismo, paritario, gestao participativa"),
    ("LCE_1261_2015", "Art. 4º", "É vedada a aplicação dos recursos do Fundo de Melhoria das Estâncias em pagamento de pessoal, despesas correntes de custeio municipal ou publicidade institucional.", "Verba carimbada estritamente para investimentos de capital em infraestrutura turística.", "vedacao, custeio, folha de pessoal, carimbada, investimento capital"),
    ("LCE_1261_2015", "Art. 5º", "A cada 3 anos a ALESP revisará a classificação dos municípios através de Lei Revisional, com ranqueamento pontuado pela Secretaria de Turismo.", "Sistema dinâmico de ranqueamento: risco de rebaixamento a MIT caso São Roque perca pontuação.", "ranqueamento trienal, revisao das estancias, alesp, perda de status"),

    # Decreto Estadual 65.415/2020
    ("DEC_EST_65415_2020", "Art. 2º", "A celebração dos convênios de repasse do DADETUR exige ata de aprovação prévia do COMTUR, projeto executivo de engenharia e comprovação de vigência trienal do PDTur.", "Condicionantes documentais obrigatórias para formalização de convênios anuais de repasse.", "convenio dadetur, ata comtur, projeto executivo, certidao pdtur"),

    # Lei Orgânica de São Roque 1.801/1990
    ("LEI_ORG_1801_1990", "Art. 1º, § 2º", "A cidade de São Roque é a sede do Governo Municipal e ostenta, de pleno direito, o título honorífico e o regime jurídico-administrativo de Estância Turística do Estado de São Paulo.", "Consagração do regime de Estância Turística na Constituição Municipal.", "lei organica, titulo estancial, regime juridico administrativo"),
    ("LEI_ORG_1801_1990", "Art. 178", "O Município promoverá e incentivará o turismo como atividade estratégica, mantendo permanentemente atualizado o PDTur em harmonia com o Plano Diretor Estratégico (LC 39/06).", "Integração institucional cogente entre planejamento urbano físico e políticas turísticas.", "turismo estrategico, integracao plano diretor, dotacao orcamentaria"),

    # LC 94/2018 e LC 140/2025 (PDTur)
    ("LC_MUN_94_2018", "Art. 1º e 2º", "Fica instituído o Plano Diretor de Desenvolvimento Turístico de São Roque (PDTur) decênio 2018-2028 para cumprir a LCE 1.261/15 e ordenar os eixos de enoturismo, gastronomia e ecoturismo.", "Primeiro plano estruturante decenal da estância turística.", "pdtur 2018, enoturismo, rota do vinho, ecoturismo"),
    ("LC_MUN_140_2025", "Art. 1º e 2º", "Aprova a Revisão e Atualização Trienal do PDTur, consolidando os eixos de Enoturismo/Gastronomia, Ecoturismo/Paisagem Cênica (Morro do Saboó e Cruzeiro) e Mananciais (APA Itupararanga).", "Matriz trienal 2025-2028 de projetos executivos financiados com verbas DADETUR.", "revisao 2025, morro do saboo, estrada do vinho, apa itupararanga, dadetur 2025"),

    # Lei 2.871/2004 (COMTUR)
    ("LEI_MUN_2871_2004", "Art. 1º e 2º", "O COMTUR é órgão colegiado permanente com caráter deliberativo privativo sobre a aplicação de recursos do DADETUR e aprovação dos projetos técnicos da Estância.", "Poder de veto e exigência de ata deliberativa vinculante para celebração de convênios.", "comtur deliberativo, aprovacao dadetur, fiscalizacao de obras"),

    # Lei 4.872/2018 (Guias Regionais)
    ("LEI_MUN_4872_2018", "Art. 1º e 2º", "Obrigatoriedade de contratação de Guia de Turismo Regional Cadastur para todos os grupos e excursões turísticas transportadas por ônibus ou vans em visitação a São Roque.", "Exercício do poder de polícia da estância para segurança, controle de carga de atrativos e combate ao turismo clandestino.", "guia de turismo regional, cadastur, excursao, onibus de turismo, poder de policia")
]

for art in artigos_novos:
    cur.execute("""
        INSERT INTO artigos_dispositivos 
        (norma_id, artigo, texto_normativo, restricao_urbanistica_ambiental, palavras_chave)
        VALUES (?, ?, ?, ?, ?)
    """, art)

print(f"Total de {len(artigos_novos)} artigos novos indexados com sucesso.")

# 5. Registrar os Cruzamentos Legislativos em cruzamento_camada_legislacao
cruzamentos_novos = [
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Estadual", "Constituição Estadual", "Constituição SP", 1989, "Art. 146", "Repasse Condicionado", "Direito a repasses do Fundo de Melhoria das Estâncias (DADETUR) condicionado a projetos executivos e COMTUR.", "Exige dotação orçamentária carimbada e vedação de despesas de custeio/pessoal."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Estadual", "Constituição Estadual", "Constituição SP", 1989, "Art. 180", "Ordenamento Territorial", "Diretrizes de ordenação do uso do solo e preservação de áreas de interesse turístico e patrimônio natural.", "Harmonização entre função social e vocação turística."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Estadual", "Lei Ordinária", "6899", 1990, "Art. 1º", "Status Jurídico-Institucional", "Transformação oficial de São Roque em Estância Turística com deveres e direitos decorrentes.", "Regime especial permanente do Direito Público paulista."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Estadual", "Lei Complementar", "1261", 2015, "Art. 2º, VI e VII", "Requisito Mandatório Trienal", "Obrigação legal de Plano Diretor de Turismo (PDTur) revisado a cada 3 anos e COMTUR ativo.", "Risco de perda da condição de Estância no ranqueamento trienal da ALESP em caso de inobservância."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Estadual", "Decreto", "65415", 2020, "Art. 2º", "Execução Orçamentária", "Regras para formalização de convênios DADETUR com aprovação vinculante do COMTUR e projeto técnico aprovado.", "Impedimento de celebração sem aprovação prévia do Conselho."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Municipal", "Lei Orgânica", "1801", 1990, "Art. 1º e 178", "Diretriz Constitucional Municipal", "Consagração do regime de Estância e obrigação de fomento orçamentário ao turismo e compatibilização do Plano Diretor.", "Vinculação institucional de dotações orçamentárias."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Municipal", "Lei Complementar", "39", 2006, "Arts. 1º, 3º e 60", "Macrozoneamento Geral", "Plano Diretor Estratégico articulando o desenvolvimento urbano com a proteção dos corredores de vocação turística e mananciais.", "Subordinação de novas edificações e parcelamentos à vocação turística sustentável."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Municipal", "Lei Complementar", "140", 2025, "Art. 1º a 3º", "Planejamento Setorial Vigente", "Revisão e Atualização do PDTur 2025-2028: metas trienais, rotas enogastronômicas, ecoturismo e prioridades DADETUR.", "Instrumento técnico executivo com força de lei complementar."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Municipal", "Lei Ordinária", "2871", 2004, "Art. 1º e 2º", "Governança Deliberativa", "Competência deliberativa vinculante do COMTUR sobre as dotações DADETUR.", "Nenhum repasse pode ser empenhado sem ata formal do Conselho."),
    ("territorio_municipal", "TERRITORIO_MUNICIPAL", "Municipal", "Lei Ordinária", "4872", 2018, "Art. 1º", "Poder de Polícia Turística", "Exigência obrigatória de Guia Regional Cadastur para grupos e excursões no território da estância.", "Fiscalização de tráfego, estacionamento e capacidade de carga nos atrativos."),
    
    # Cruzamento com a camada de zoneamento (LC 40/2006)
    ("zoneamento", "ZUE-DT", "Municipal", "Lei Complementar", "140", 2025, "Art. 2º, I", "Zoneamento de Vocação Específica", "Diretrizes do PDTur 2025 para Zonas de Desenvolvimento Turístico e corredores da Estrada do Vinho.", "Compatibilização de lote mínimo e incentivos hoteleiros e enológicos."),
    ("zoneamento", "ZR", "Estadual", "Lei Complementar", "1261", 2015, "Art. 2º, V", "Preservação da Paisagem Rural", "Proteção dos atrativos naturais e rurais contra o desmembramento urbano predatório.", "Resguardo da oferta turística e cênica.")
]

for cr in cruzamentos_novos:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao 
        (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

print(f"Total de {len(cruzamentos_novos)} cruzamentos cadastrados com sucesso.")

conn.commit()

# 6. Atualizar contagens finais
cur.execute("SELECT COUNT(*) FROM camadas_territoriais")
print("Total Camadas Territoriais:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM classes_camada_territorial")
print("Total Classes Cadastradas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM normas_juridicas")
print("Total Normas Jurídicas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM artigos_dispositivos")
print("Total Artigos Indexados:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao")
print("Total Cruzamentos Legislativos:", cur.fetchone()[0])

conn.close()
print("=== BASE DE DADOS ATUALIZADA COM SUCESSO! ===")
