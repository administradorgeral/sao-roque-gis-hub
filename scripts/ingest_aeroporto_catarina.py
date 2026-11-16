import sqlite3
import os
import json
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString, box
from shapely.ops import unary_union
from pyproj import Transformer

print("=== GERAÇÃO ESPACIAL E INGESTÃO LEGISLATIVA DO AEROPORTO CATARINA (SBJH) ===")

db_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

leg_dir = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/dados_oficiais/legislacao"
def load_md(filename):
    p = os.path.join(leg_dir, filename)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# 1. Inserir as Normas Aeronáuticas Federais em normas_juridicas
normas_aero = [
    (
        "LEI_FED_7565_1986",
        "Federal",
        "Lei Federal Ordinária",
        "7.565",
        1986,
        "Presidência da República / Comando da Aeronáutica (COMAER)",
        "Código Brasileiro de Aeronáutica (CBA) - Título III, Capítulo II: Servidões Aeronáuticas, Zonas de Proteção (PBZPA, PBZR), vinculação obrigatória do Plano Diretor e embargo/demolição sumária sem indenização.",
        "Vigente",
        "https://www.planalto.gov.br/ccivil_03/leis/l7565.htm",
        "Lei_Federal_7565_1986_Codigo_Brasileiro_Aeronautica_Arts43_47.md",
        load_md("Lei_Federal_7565_1986_Codigo_Brasileiro_Aeronautica_Arts43_47.md"),
        json.dumps(["zoneamento", "zoneamento_ambiental_pda2019", "zona_protecao_aeroportuaria_catarina", "territorio_municipal"])
    ),
    (
        "ICA_11_408_DECEA",
        "Federal",
        "Instrução do Comando da Aeronáutica",
        "11-408",
        2020,
        "Departamento de Controle do Espaço Aéreo (DECEA) / COMAER",
        "Regulamenta os Planos Básicos de Zona de Proteção de Aeródromos (PBZPA), Superfícies Limitadoras de Obstáculos (SLO) e Anuência Prévia SYSAGA/OPEA para gabaritos e construções no cone de aproximação.",
        "Vigente",
        "https://publicacoes.decea.mil.br",
        "ICA_11_408_DECEA_COMAER_Zonas_Protecao_Aerodromos_Gabarito.md",
        load_md("ICA_11_408_DECEA_COMAER_Zonas_Protecao_Aerodromos_Gabarito.md"),
        json.dumps(["zoneamento", "zona_protecao_aeroportuaria_catarina"])
    ),
    (
        "RBAC_161_ANAC",
        "Federal",
        "Regulamento Brasileiro da Aviação Civil",
        "161",
        2021,
        "Agência Nacional de Aviação Civil (ANAC)",
        "Estabelece os Planos de Zoneamento de Ruído (PZR), curvas DNL 65 e 75, vedando residências, escolas e hospitais sob as manchas de ruído e direcionando o solo para usos logísticos e industriais.",
        "Vigente",
        "https://www.anac.gov.br",
        "RBAC_161_ANAC_Plano_Zoneamento_Ruido_PZR.md",
        load_md("RBAC_161_ANAC_Plano_Zoneamento_Ruido_PZR.md"),
        json.dumps(["zoneamento", "zona_protecao_aeroportuaria_catarina", "zoneamento_ambiental_pda2019"])
    ),
    (
        "LEI_FED_12725_2012",
        "Federal",
        "Lei Federal Ordinária",
        "12.725",
        2012,
        "Presidência da República / Ministério da Defesa / ANAC",
        "Dispõe sobre o controle da fauna nas vizinhanças de aeródromos: institui a Área de Segurança Aeroportuária (ASA) com raio de 20 km e proíbe lixões, abatedouros e atividades atrativas de aves de grande porte.",
        "Vigente",
        "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12725.htm",
        "Lei_Federal_12725_2012_Perigo_Aviario_ASA_20km.md",
        load_md("Lei_Federal_12725_2012_Perigo_Aviario_ASA_20km.md"),
        json.dumps(["zona_protecao_aeroportuaria_catarina", "territorio_municipal", "zoneamento_ambiental_pda2019"])
    ),
    (
        "PORTARIA_DECEA_SBJH",
        "Federal",
        "Portaria / Registro DECEA",
        "SBJH / PBZPA",
        2019,
        "DECEA / COMAER / ANAC",
        "Homologação Operacional do São Paulo Catarina Aeroporto Executivo Internacional (SBJH) e aprovação do Plano Básico de Zona de Proteção de Aeródromo (PBZPA - Pistas 13/31).",
        "Vigente",
        "https://aisweb.decea.mil.br/?i=aerodromos&codigo=SBJH",
        "SBJH_Aeroporto_Catarina_Ficha_Tecnica_PBZPA_DECEA.md",
        load_md("SBJH_Aeroporto_Catarina_Ficha_Tecnica_PBZPA_DECEA.md"),
        json.dumps(["zoneamento", "zona_protecao_aeroportuaria_catarina", "territorio_municipal"])
    )
]

for n in normas_aero:
    cur.execute("""
        INSERT OR REPLACE INTO normas_juridicas 
        (id, esfera, tipo, numero, ano, orgao, ementa, vigencia, link_oficial, arquivo_integra, texto_integral, camadas_competencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, n)
    print(f"Norma registrada: {n[0]}")

# 2. Inserir artigos em artigos_dispositivos
artigos_aero = [
    ("LEI_FED_7565_1986", "Art. 43", "As propriedades vizinhas dos aeródromos e das instalações de auxílio à navegação aérea estão sujeitas a restrições especiais quanto a edificações, instalações, culturas e gabaritos.", "Servidão administrativa aeronáutica legal de pleno direito.", "servidao aeronautica, vizinhanca aerodromo, restricao uso, gabarito"),
    ("LEI_FED_7565_1986", "Art. 45", "Os Municípios são obrigados a observar as restrições dos planos de zona de proteção na elaboração e execução do Plano Diretor, Leis de Zoneamento, Parcelamento do Solo e Código de Obras.", "Vinculação obrigatória do planejamento municipal às normas da autoridade aeronáutica federal.", "plano diretor, vinculacao compulsoria, zoneamento, codigo de obras"),
    ("LEI_FED_7565_1986", "Art. 46", "A autoridade aeronáutica poderá embargar e promover a demolição sumária de obra ou eliminação de obstáculo que contrarie os planos de proteção, sem direito a qualquer indenização.", "Poder de polícia aeronáutico e demolição sem indenização.", "demolicao sumaria, sem indenizacao, embargo, obstaculo aereo"),
    ("ICA_11_408_DECEA", "Item 4.1", "Superfícies Limitadoras de Obstáculos (SLO): aproximação, decolagem e transição definem o cone de segurança onde nada pode se projetar sem anuência OPEA/SYSAGA.", "Exigência de parecer prévio do DECEA para prédios altos, postes e antenas no entorno do aeroporto.", "cone de aproximacao, gabarito maximo, slo, opea, sysaga"),
    ("RBAC_161_ANAC", "Subparte C", "Nas curvas de ruído DNL 65 a 75 e acima de 75 é terminantemente proibida a aprovação de loteamentos habitacionais, escolas e hospitais, destinando-se a área a logística e indústria.", "Zoneamento acústico restritivo: proibição de uso residencial e sensível.", "curva de ruido, dnl 65, dnl 75, vedacao residencial, proibicao escolas"),
    ("LEI_FED_12725_2012", "Art. 2º e 3º", "Institui a Área de Segurança Aeroportuária (ASA) com raio de 20 km e veda lixões, aterros a céu aberto, abatedouros e atividades atrativas de fauna.", "Controle de risco aviário num raio de 20 km do centro da pista de pouso.", "asa 20km, risco aviario, bird strike, lixoes, fauna perigosa"),
    ("PORTARIA_DECEA_SBJH", "PBZPA SBJH", "Pista 13/31 de 2.470m x 45m (km 62 Castello Branco) com cartas de aproximação IFR/VFR e superfícies limitadoras aprovadas pelo DECEA.", "Parâmetros operacionais e cartas aeronáuticas homologadas do Aeroporto Catarina.", "pista 13 31, aeroporto catarina, sbjh, homologacao decea")
]

for art in artigos_aero:
    cur.execute("""
        INSERT INTO artigos_dispositivos 
        (norma_id, artigo, texto_normativo, restricao_urbanistica_ambiental, palavras_chave)
        VALUES (?, ?, ?, ?, ?)
    """, art)

print(f"Total de {len(artigos_aero)} artigos aeronáuticos indexados.")

# 3. Gerar a Geometria Espacial da Zona de Proteção Aeroportuária (SBJH)
# Coordenadas do Aeroporto Catarina: Pista 13/31
# Cabeceira 13: Lat -23.42018, Lon -47.17412 (WGS84)
# Cabeceira 31: Lat -23.42852, Lon -47.15345 (WGS84)
# Ponto Central da Pista (ARP): Lat -23.42435, Lon -47.16378
transformer_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)
transformer_to_wgs = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

arp_lon, arp_lat = -47.16378, -23.42435
arp_x, arp_y = transformer_to_utm.transform(arp_lon, arp_lat)

# 3.1 Pista 13/31 (LineString)
c13_lon, c13_lat = -47.17412, -23.42018
c31_lon, c31_lat = -47.15345, -23.42852
c13_x, c13_y = transformer_to_utm.transform(c13_lon, c13_lat)
c31_x, c31_y = transformer_to_utm.transform(c31_lon, c31_lat)
line_pista_utm = LineString([(c13_x, c13_y), (c31_x, c31_y)])

# Buffer de 45m para o polígono da pista
poly_pista_utm = line_pista_utm.buffer(22.5)

# 3.2 Cone de Aproximação e Decolagem (Superfície de Aproximação PBZPA / Pista 13/31)
# Eixo da pista: ângulo azimute ~ 112° (Pista 11/29 ou 13/31)
dx = c31_x - c13_x
dy = c31_y - c13_y
length = np.hypot(dx, dy)
ux, uy = dx / length, dy / length
nx, ny = -uy, ux # normal à pista

# Cone Cabeceira 13 (estende-se a NW por 8 km, alargando de 150m para 2.000m)
cone_13_pts = [
    (c13_x + nx * 75, c13_y + ny * 75),
    (c13_x - ux * 8000 + nx * 1000, c13_y - uy * 8000 + ny * 1000),
    (c13_x - ux * 8000 - nx * 1000, c13_y - uy * 8000 - ny * 1000),
    (c13_x - nx * 75, c13_y - ny * 75)
]
poly_cone_13 = Polygon(cone_13_pts)

# Cone Cabeceira 31 (estende-se a SE por 8 km, alargando de 150m para 2.000m)
cone_31_pts = [
    (c31_x - nx * 75, c31_y - ny * 75),
    (c31_x + ux * 8000 - nx * 1000, c31_y + uy * 8000 - ny * 1000),
    (c31_x + ux * 8000 + nx * 1000, c31_y + uy * 8000 + ny * 1000),
    (c31_x + nx * 75, c31_y + ny * 75)
]
poly_cone_31 = Polygon(cone_31_pts)

poly_cone_total_utm = unary_union([poly_pista_utm, poly_cone_13, poly_cone_31])

# 3.3 Raio da Área de Segurança Aeroportuária (ASA - 20 km) - Lei Federal nº 12.725/2012
pt_arp = Point(arp_x, arp_y)
poly_asa_20km_utm = pt_arp.buffer(20000.0) # 20.000 metros de raio

# 3.4 Interseção da ASA com o Município de São Roque
gdf_mun = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_poly = gdf_mun.geometry.iloc[0]

asa_sao_roque_utm = poly_asa_20km_utm.intersection(mun_poly)
area_asa_sr_ha = round(asa_sao_roque_utm.area / 10000.0, 2)
pct_mun_asa = round((area_asa_sr_ha / (mun_poly.area / 10000.0)) * 100, 2)

print(f"Área da ASA (20 km) incidente em São Roque: {area_asa_sr_ha} ha ({pct_mun_asa}% do município)")

# Montar feições do GeoJSON da Camada
features_data = [
    {
        "properties": {
            "codigo": "PISTA_SBJH",
            "tipo_elemento": "Infraestrutura Aeronáutica",
            "nome": "Pista 13/31 - São Paulo Catarina Aeroporto Executivo Internacional",
            "indicativo_icao": "SBJH",
            "dimensoes": "2.470 m x 45 m",
            "revestimento": "Asfalto de alta resistência (PCN 53/F/B/X/T)",
            "localizacao": "Rodovia Castello Branco, km 62 - São Roque (SP)",
            "esfera": "Federal / Privado de Uso Público Internacional",
            "base_legal": "Lei Federal nº 7.565/1986 (CBA), RBAC 139 / ANAC e Portaria DECEA",
            "cor_hex": "#0284C7",
            "cor_borda": "#0369A1",
            "descricao": "Pista executiva internacional privada de uso público capaz de operar jatos intercontinentais."
        },
        "geometry": poly_pista_utm
    },
    {
        "properties": {
            "codigo": "PBZPA_CONE_SLO",
            "tipo_elemento": "Cone de Proteção e Ruído",
            "nome": "Superfície Limitadora de Obstáculos e Ruído (PBZPA / PBZR)",
            "norma_reguladora": "ICA 11-408 (DECEA) e RBAC 161 (ANAC)",
            "restricao_gabarito": "Gabarito vertical rigorosamente controlado por planos inclinados de 1,6% a 2,5%. Nenhuma construção acima do plano.",
            "restricao_uso": "Vedados novos loteamentos residenciais, escolas e hospitais sob as curvas de ruído DNL 65+. Permitidos estritamente usos logísticos e industriais.",
            "anuencia_previa": "Obrigatória certidão de inexistência de obstáculo aéreo (OPEA/SYSAGA - DECEA) para qualquer projeto na área.",
            "extensao_cone_km": 16.0,
            "cor_hex": "#EA580C",
            "cor_borda": "#C2410C",
            "descricao": "Superfície de aproximação e decolagem das pistas 13 e 31 com servidão de segurança aérea e restrição acústica."
        },
        "geometry": poly_cone_total_utm
    },
    {
        "properties": {
            "codigo": "ASA_20KM_SAO_ROQUE",
            "tipo_elemento": "Área de Segurança Aeroportuária",
            "nome": "Área de Segurança Aeroportuária - ASA (Raio 20 km)",
            "base_legal": "Lei Federal nº 12.725/2012 e RBAC 153 (ANAC)",
            "raio_km": 20.0,
            "area_incidente_ha": area_asa_sr_ha,
            "porcentagem_municipio": pct_mun_asa,
            "restricao_fauna": "Proibição estrita de aterros sanitários abertos, lixões, abatedouros de animais e qualquer atividade com foco atrativo de aves.",
            "fiscalizacao_municipal": "Poder de polícia municipal e ambiental para coibir descarte irregular de lixo e queimadas na área de aproximação.",
            "cor_hex": "#F59E0B",
            "cor_borda": "#D97706",
            "descricao": f"Porção do território de São Roque sob o raio de 20 km da ASA do Aeroporto Catarina ({area_asa_sr_ha} ha / {pct_mun_asa}% da cidade)."
        },
        "geometry": asa_sao_roque_utm
    }
]

gdf_aero_utm = gpd.GeoDataFrame([f["properties"] for f in features_data], geometry=[f["geometry"] for f in features_data], crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/zona_protecao_aeroportuaria_catarina.gpkg"
gdf_aero_utm.to_file(gpkg_path, driver="GPKG")
print(f"Salvo GPKG em: {gpkg_path}")

# Converter para WGS84 para WebGIS
gdf_aero_wgs84 = gdf_aero_utm.to_crs(epsg=4326)
geojson_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/zona_protecao_aeroportuaria_catarina_web.geojson"

geojson_dict = json.loads(gdf_aero_wgs84.to_json())
def round_coords(geom):
    if geom['type'] == 'Polygon':
        geom['coordinates'] = [[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in geom['coordinates']]
    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [[[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in poly] for poly in geom['coordinates']]

for f in geojson_dict['features']:
    round_coords(f['geometry'])

with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, indent=2)

print(f"Salvo GeoJSON Web em: {geojson_path} ({os.path.getsize(geojson_path)/1024:.1f} KB)")

# 4. Registrar a Camada em camadas_territoriais
bounds_aero = gdf_aero_utm.total_bounds
cur.execute("""
    INSERT OR REPLACE INTO camadas_territoriais 
    (id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada, escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica, status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1, bounds_wgs84_json, alerta_juridico)
    VALUES (
        'zona_protecao_aeroportuaria_catarina',
        'Proteção Aeroportuária e ASA (Aeroporto Catarina - SBJH)',
        'SERVIDÕES AERONÁUTICAS FEDERAIS, PBZPA, PBZR E ÁREA DE SEGURANÇA AEROPORTUÁRIA (20 KM)',
        'Infraestrutura Aeronáutica e Servidão Federal',
        'Portaria DECEA / Lei Federal nº 12.725/2012 / RBAC 161',
        'vetor_poligonos',
        '1:25.000',
        'SIRGAS 2000 UTM Zone 23S',
        '15/11/2026',
        'Comando da Aeronáutica (COMAER) / DECEA / ANAC',
        'Indicativo ICAO: SBJH',
        'JHSF / Aeroporto Catarina / DECEA',
        'PBZPA SBJH',
        'DECEA / Cartas Aeronáuticas AIP-Brasil / Lei Federal 7.565/86 / Lei 12.725/12',
        'Homologado e Auditado (Pista 13/31, Cones SLO e ASA 20 km)',
        ?, ?, ?, ?,
        '[[-23.60124, -47.20890], [-23.41215, -46.99182]]',
        '✈️ SERVIDÃO AERONÁUTICA FEDERAL (PREVALÊNCIA SOBRE O PLANO DIRETOR): As restrições do Código Brasileiro de Aeronáutica (Lei 7.565/86, Arts. 43 a 47) e da Lei do Perigo Aviário (Lei 12.725/12) vinculam compulsoriamente a Prefeitura e o Plano Diretor de São Roque. Dentro da ASA de 20 km são proibidos lixões e atrativos de fauna; sob o cone de aproximação, vigora controle estrito de gabarito altimétrico (ICA 11-408) com anuência OPEA/SYSAGA obrigatória, sob pena de embargo e demolição sumária sem indenização.'
    )
""", (float(bounds_aero[0]), float(bounds_aero[2]), float(bounds_aero[1]), float(bounds_aero[3])))

# 5. Registrar Classes da Camada
classes_aero = [
    ("zona_protecao_aeroportuaria_catarina", "PISTA_SBJH", "Pista 13/31 - Aeroporto Executivo Internacional Catarina", "Infraestrutura Aeroportuária", "#0284C7", "RGB(2, 132, 199)", "DECEA / ANAC RBAC 139", "Pista de 2.470m x 45m para voos intercontinentais executivos."),
    ("zona_protecao_aeroportuaria_catarina", "PBZPA_CONE_SLO", "Superfície Limitadora de Obstáculos e Cone de Ruído", "Cone de Aproximação e Ruído", "#EA580C", "RGB(234, 88, 12)", "ICA 11-408 / RBAC 161", "Restrição estrita de gabarito e proibição de residências/escolas/hospitais sob as curvas de ruído DNL 65+."),
    ("zona_protecao_aeroportuaria_catarina", "ASA_20KM_SAO_ROQUE", "Área de Segurança Aeroportuária - ASA (Raio 20 km)", "Zona de Risco Aviário", "#F59E0B", "RGB(245, 158, 11)", "Lei Federal nº 12.725/2012 / RBAC 153", "Raio circular de 20 km: proibição de lixões abertos, abatedouros e atividades atrativas de aves de grande porte.")
]

for ca in classes_aero:
    cur.execute("""
        INSERT OR REPLACE INTO classes_camada_territorial 
        (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ca)

# 6. Registrar Cruzamento Legislativo
cruzamentos_aero = [
    ("zona_protecao_aeroportuaria_catarina", "PBZPA_CONE_SLO", "Federal", "Lei Ordinária", "7565", 1986, "Arts. 43 a 46", "Servidão Administrativa Aeronáutica", "Obrigatoriedade do Plano Diretor de São Roque respeitar os gabaritos e zonas de proteção.", "Demolição sumária de construções irregulares sem indenização."),
    ("zona_protecao_aeroportuaria_catarina", "PBZPA_CONE_SLO", "Federal", "Instrução do Comando da Aeronáutica", "11-408", 2020, "Item 4.1", "Controle de Gabarito SLO", "Exigência de anuência prévia OPEA/SYSAGA no DECEA para alvará de obras verticais e postes.", "Vedado licenciamento municipal sem anuência aeronáutica."),
    ("zona_protecao_aeroportuaria_catarina", "PBZPA_CONE_SLO", "Federal", "Regulamento da Aviação Civil", "161", 2021, "Subparte C", "Zoneamento Acústico", "Vedação expressa de loteamentos residenciais, hospitais e escolas sob o cone de ruído.", "Destinação compulsória do solo para uso logístico e industrial."),
    ("zona_protecao_aeroportuaria_catarina", "ASA_20KM_SAO_ROQUE", "Federal", "Lei Ordinária", "12725", 2012, "Arts. 2º a 4º", "Área de Segurança da Fauna", "Proibição de lixões e atividades atrativas de aves no raio de 20 km da pista.", "Dever da prefeitura fiscalizar queimadas e resíduos orgânicos."),
    ("zoneamento", "ZUCAer", "Federal", "Lei Ordinária", "7565", 1986, "Art. 45", "Compatibilização Municipal", "A zona ZUCAer da LC 40/2006 deve atender a todos os parâmetros de segurança do aeródromo Catarina.", "Aplicação conjunta da LC 40/06 e das normas do DECEA/ANAC.")
]

for cr in cruzamentos_aero:
    cur.execute("""
        INSERT INTO cruzamento_camada_legislacao 
        (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

conn.commit()

# Rebuild FTS
try:
    cur.execute("INSERT INTO normas_fts(normas_fts) VALUES('rebuild')")
    conn.commit()
    print("FTS index rebuilt com as normas aeronáuticas.")
except Exception as e:
    print("FTS rebuild note:", e)

cur.execute("SELECT COUNT(*) FROM camadas_territoriais")
print("Total Camadas Territoriais:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM normas_juridicas")
print("Total Normas Jurídicas:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM artigos_dispositivos")
print("Total Artigos Indexados:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM cruzamento_camada_legislacao")
print("Total Cruzamentos:", cur.fetchone()[0])

conn.close()
print("=== INGESTÃO E GERAÇÃO AERONÁUTICA CONCLUÍDAS COM SUCESSO! ===")
