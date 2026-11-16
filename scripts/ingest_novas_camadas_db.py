import sqlite3
import json

db_path = "dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 1. Camadas
camadas = [
    (
        "distritos",
        "Distritos Municipais (IBGE 2022)",
        "Divisão Político-Administrativa e Distritos Oficiais de São Roque",
        "Divisão Político-Administrativa e Cidadania",
        "sao_roque_3550605_setores_CD2022.kmz / IBGE",
        "vetor_poligono",
        "1:50.000",
        "SIRGAS 2000 (EPSG: 31983) / WGS84",
        "2022-12-31",
        "IBGE - Instituto Brasileiro de Geografia e Estatística",
        "CONFEA/CREA - Geociências Oficiais",
        "Divisão Territorial IBGE Censo 2022",
        "Base de Informações Geográficas",
        "IBGE Censo Demográfico 2022 e Lei Orgânica Municipal nº 1.801/1990",
        "HOMOLOGADO",
        273000.0, 303000.0, 7378000.0, 7409000.0,
        json.dumps([[-23.684, -47.235], [-23.428, -46.974]]),
        "Divisão oficial em 4 distritos com competência administrativa local e representação comunitária."
    ),
    (
        "setores_censitarios",
        "Setores Censitários (IBGE Censo 2022)",
        "Malha de Setores Censitários do Censo Demográfico 2022",
        "Demografia e Estatística Territorial",
        "sao_roque_3550605_setores_CD2022.kmz / IBGE",
        "vetor_poligono",
        "1:25.000",
        "SIRGAS 2000 (EPSG: 31983) / WGS84",
        "2022-12-31",
        "IBGE - Instituto Brasileiro de Geografia e Estatística",
        "Coordenação Operacional dos Censos",
        "IBGE Malha Censitária Contínua",
        "Base Cartográfica Territorial",
        "IBGE Censo Demográfico 2022 (Código Municipal 3550605)",
        "HOMOLOGADO",
        273000.0, 303000.0, 7378000.0, 7409000.0,
        json.dumps([[-23.684, -47.235], [-23.428, -46.974]]),
        "188 setores censitários (134 urbanos e 54 rurais) com dados estatísticos e demográficos domiciliares."
    ),
    (
        "logradouros",
        "Sistema Viário e Logradouros (3.241 Ruas)",
        "Malha Cartográfica do Sistema Viário e Logradouros Municipais",
        "Infraestrutura Urbana e Mobilidade",
        "OpenStreetMap / DER-SP / CCR ViaOeste / PMSP",
        "vetor_linha",
        "1:10.000",
        "SIRGAS 2000 (EPSG: 31983) / WGS84",
        "2026-01-01",
        "Prefeitura da Estância Turística de São Roque / DER-SP / OSM contributors",
        "Engenharia de Tráfego e Transportes",
        "OpenStreetMap Geocoding e DER-SP",
        "Rede Viária Integrada",
        "OpenStreetMap 2024-2026, Malha Viária DER-SP e Plano Diretor LC nº 40/06",
        "HOMOLOGADO",
        273000.0, 303000.0, 7378000.0, 7409000.0,
        json.dumps([[-23.684, -47.235], [-23.428, -46.974]]),
        "4.868 trechos de vias e 3.241 logradouros catalogados com hierarquia de tráfego e recuos de alinhamento."
    )
]

for cam in camadas:
    cur.execute("""
        INSERT OR REPLACE INTO camadas_territoriais (
            id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal,
            datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea,
            desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria,
            bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cam)

# 2. Classes
classes = [
    # Distritos
    ("distritos", "DISTRITO_SAO_ROQUE", "Distrito Sede de São Roque", "12.336,51 ha (40,18%) · 92 setores censitários", "#2563EB", "rgb(37,99,235)", "IBGE 2022 / Lei 1.801/90", "Distrito sede concentrador da administração municipal, centro histórico, comércio e serviços."),
    ("distritos", "DISTRITO_CANGUERA", "Distrito de Canguera", "8.639,17 ha (28,14%) · 43 setores censitários", "#059669", "rgb(5,150,105)", "IBGE 2022 / Lei 1.801/90", "Polo do turismo enológico e gastronômico (Roteiro do Vinho), área de mananciais da bacia de Itupararanga."),
    ("distritos", "DISTRITO_SAO_JOAO_NOVO", "Distrito de São João Novo", "6.409,34 ha (20,88%) · 26 setores censitários", "#7C3AED", "rgb(124,58,237)", "IBGE 2022 / Lei 1.801/90", "Vetor norte-leste com vocação ferroviária, industrial, aeroportuária (Catarina) e residencial."),
    ("distritos", "DISTRITO_MAILASQUI", "Distrito de Mailasqui", "3.316,45 ha (10,80%) · 27 setores censitários", "#D97706", "rgb(217,119,6)", "IBGE 2022 / Lei 1.801/90", "Eixo leste conectado à Rodovia Raposo Tavares, com perfil misto de polo industrial e moradia popular."),
    
    # Setores Censitários
    ("setores_censitarios", "SETOR_URBANO", "Setores Censitários Urbanos (134 setores)", "Malha Urbana Contínua e Loteamentos", "#3B82F6", "rgb(59,130,246)", "IBGE Censo 2022", "Áreas urbanizadas, bairros consolidados e condomínios com densidade populacional e cobertura de saneamento."),
    ("setores_censitarios", "SETOR_RURAL", "Setores Censitários Rurais (54 setores)", "Áreas Rurais e de Proteção Ambiental", "#10B981", "rgb(16,185,129)", "IBGE Censo 2022", "Propriedades agrícolas, áreas de preservação permanente, turismo rural e remanescentes de Mata Atlântica."),
    
    # Logradouros
    ("logradouros", "RODOVIAS_ESTADUAIS", "Rodovias Principais (SP-280, SP-270, SP-053)", "Pistas Duplas e Rodovias Concessionadas", "#DC2626", "rgb(220,38,38)", "DER-SP / Artesp / OSM", "Faixas de domínio restritas (15m a 35m 'non aedificandi'), acessos controlados e alta velocidade."),
    ("logradouros", "AVENIDAS_ESTRADAS_TURISTICAS", "Avenidas Coletoras e Estradas Turísticas", "Eixos Estruturantes e Roteiro do Vinho", "#D97706", "rgb(217,119,6)", "LC 40/06 / Turismo", "Recuos frontais mínimos de 5,00m, faixas para pedestres, ciclovias turísticas e velocidade até 60 km/h."),
    ("logradouros", "RUAS_LOCAIS_RESIDENCIAIS", "Ruas Locais e Residenciais (3.241 vias)", "Malha Viária Secundária e Residencial", "#64748B", "rgb(100,116,139)", "LC 40/06 Sistema Viário", "Largura mínima de caixa de rua de 14,00m a 10,00m, recuos prediais obrigatórios de 4,00m.")
]

for cls in classes:
    cur.execute("""
        INSERT OR REPLACE INTO classes_camada_territorial (
            camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb,
            metodologia_referencia, implicacao_pratica
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cls)

# 3. Cruzamentos Legais
cruzamentos = [
    # Distritos
    ("distritos", None, "Municipal", "Lei Orgânica", "1.801", 1990, "Arts. 2º a 5º", "Condicionante", "Fixa a divisão administrativa municipal em 4 distritos, garantindo representação e descentralização de postos de saúde e escolas.", "Revisões de perímetros distritais demandam lei municipal específica e consulta às comunidades."),
    ("distritos", None, "Municipal", "Lei Complementar", "39", 2006, "Arts. 18 e 19", "Condicionante", "Determina que as políticas públicas setoriais do Plano Diretor devem ser territorializadas por distrito.", "Exigência de planos de desenvolvimento local para Canguera, Mailasqui e São João Novo."),
    ("distritos", None, "Federal", "Lei Ordinária", "5.534", 1968, "Art. 1º", "Informativa", "Obrigatoriedade de observância da malha estatística e distrital nos censos decenais do IBGE.", "Compatibilização entre os limites cartográficos do IBGE e os memoriais descritivos municipais."),
    
    # Setores Censitários
    ("setores_censitarios", None, "Federal", "Lei Ordinária", "5.534", 1968, "Art. 2º", "Condicionante", "Garante o sigilo individual das informações coletadas pelo IBGE e autoriza o uso agregado para planejamento.", "Dados individualizados de moradores são sigilosos; agregados por setor são públicos."),
    ("setores_censitarios", None, "Federal", "Lei Ordinária", "10.257", 2001, "Art. 4º, III", "Condicionante", "O planejamento urbano e a concessão de incentivos devem basear-se em indicadores demográficos e socioeconômicos.", "Aplicação do IPTU progressivo e ZEIS com base na densidade e carência diagnosticada nos setores."),
    ("setores_censitarios", None, "Municipal", "Lei Complementar", "39", 2006, "Art. 7º", "Informativa", "Determina o monitoramento permanente das taxas de crescimento populacional por setor urbano e rural.", "Necessidade de atualização do cadastro municipal a cada Censo do IBGE."),
    
    # Logradouros
    ("logradouros", None, "Federal", "Lei Ordinária", "9.503", 1997, "Arts. 60 a 67", "Condicionante", "Classificação funcional das vias em de trânsito rápido, arteriais, coletoras e locais, fixando velocidades máximas.", "Prevalência do Código de Trânsito Brasileiro sobre normas municipais divergentes de sinalização."),
    ("logradouros", None, "Municipal", "Lei Complementar", "40", 2006, "Arts. 45 a 55", "Condicionante / Impeditiva", "Fixa larguras mínimas de vias públicas (14m para coletoras, 11m para locais) e recuo non aedificandi de 15m em rodovias.", "Proibição de loteamentos com vias sem saída sem praça de manobra (cul-de-sac) de raio mínimo 8m."),
    ("logradouros", None, "Estadual", "Decreto Estadual", "26.673", 1987, "Arts. 1º a 12", "Impeditiva", "Regulamenta a faixa de domínio de rodovias estaduais e a faixa non aedificandi de 15 metros ao longo de estradas paulistas.", "Vedada qualquer construção civil particular dentro da faixa de 15m a contar da divisa da rodovia.")
]

for crz in cruzamentos:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao (
            camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano,
            artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, crz)

conn.commit()
print(f"Sucesso! Registradas 3 novas camadas territoriais, 9 classes e 9 cruzamentos legislativos no sao_roque_geodados.db.")
conn.close()
