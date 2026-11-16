import geopandas as gpd
import json
import os
import sqlite3
import time
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import split, unary_union

print("=== EXPORTAÇÃO DA CAMADA COMPLETA DA APA ITUPARARANGA (POLÍGONO SUL + LIMITE NORTE) ===")
t_total_start = time.time()

# 1. Carregar a linha do limite norte
gdf_line_orig = gpd.read_file("data/apa_itupararanga_limite_sao_roque.gpkg")
line = gdf_line_orig.geometry.iloc[0]
extensao_km = round(line.length / 1000.0, 2)

# 2. Carregar o contorno municipal de São Roque
gdf_mun = gpd.read_file("data/geomorfologico_sao_roque.gpkg")
mun_poly = unary_union(gdf_mun.geometry)
total_mun_ha = round(mun_poly.area / 10000.0, 2)

# Estender as pontas da linha da APA para cortar o polígono municipal limpo
coords = list(line.coords)
dx0 = coords[0][0] - coords[1][0]
dy0 = coords[0][1] - coords[1][1]
p0_ext = (coords[0][0] + dx0 * 5, coords[0][1] + dy0 * 5)

dx1 = coords[-1][0] - coords[-2][0]
dy1 = coords[-1][1] - coords[-2][1]
p1_ext = (coords[-1][0] + dx1 * 5, coords[-1][1] + dy1 * 5)

extended_line = LineString([p0_ext] + coords + [p1_ext])

parts = split(mun_poly, extended_line)

south_parts = []
for p in parts.geoms:
    if p.centroid.y < 7391000:
        south_parts.append(p)

poly_south = unary_union(south_parts)
area_apa_ha = round(poly_south.area / 10000.0, 2)
pct_municipio = round((area_apa_ha / total_mun_ha) * 100, 2)

print(f"Polígono da APA gerado: {area_apa_ha} ha ({pct_municipio}% do município de São Roque)")

# Montar registros da camada
records = [
    {
        'tipo_elemento': 'Polígono Territorial',
        'codigo': 'POLIGONO_APA',
        'nome': 'Área de Proteção Ambiental da Represa de Itupararanga (APA Itupararanga)',
        'esfera': 'Estadual',
        'lei_criacao': 'Lei Estadual nº 11.579/2003',
        'plano_manejo': 'Decreto Estadual nº 52.879/2008',
        'lei_mananciais': 'Lei Estadual nº 9.866/1997',
        'orgao_gestor': 'Fundação Florestal / SEMIL-SP / Conselho Gestor da APA',
        'area_ha': area_apa_ha,
        'porcentagem_municipio': pct_municipio,
        'extensao_limite_km': extensao_km,
        'cor_hex': '#0070FF',
        'cor_borda': '#E60000',
        'descricao': f'Região sul do município de São Roque abrangendo {area_apa_ha} ha ({pct_municipio}% do território municipal) sob o regime especial de proteção a mananciais da APA da Represa de Itupararanga.',
        'implicacao_juridica': 'Unidade de Conservação de Uso Sustentável (SNUC). Qualquer parcelamento do solo, loteamento, edificação ou atividade na bacia de drenagem do Itupararanga exige anuência prévia da Fundação Florestal, atendimento às restrições do Plano de Manejo (Decreto Estadual 52.879/08), taxa de permeabilidade mínima e sistema eficiente de esgotamento sanitário (Lei 9.866/97 e LC 39/06 Arts. 60-64).',
        'geometry': poly_south
    },
    {
        'tipo_elemento': 'Linha Limite Setentrional',
        'codigo': 'LIMITE_NORTE_APA',
        'nome': 'Limite Norte da APA Itupararanga (Divisor Hidrográfico)',
        'esfera': 'Estadual',
        'lei_criacao': 'Lei Estadual nº 11.579/2003',
        'plano_manejo': 'Decreto Estadual nº 52.879/2008',
        'lei_mananciais': 'Lei Estadual nº 9.866/1997',
        'orgao_gestor': 'Fundação Florestal / SEMIL-SP',
        'area_ha': 0.0,
        'porcentagem_municipio': 0.0,
        'extensao_limite_km': extensao_km,
        'cor_hex': '#E60000',
        'cor_borda': '#E60000',
        'descricao': f'Linha demarcatória oficial com extensão de {extensao_km} km que estabelece o limite norte da bacia contribuinte da Represa de Itupararanga.',
        'implicacao_juridica': 'Linha divisória de jurisdição ambiental. Ao sul desta demarcação incidem todas as restrições normativas da APA de Itupararanga.',
        'geometry': line
    }
]

gdf = gpd.GeoDataFrame(records, crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\apa_itupararanga_sao_roque.gpkg"
gdf.to_file(gpkg_path, layer="apa_itupararanga", driver="GPKG")
print(f"GeoPackage salvo: {gpkg_path}")

# Reprojetar para EPSG:4326 e salvar GeoJSON
gdf_wgs84 = gdf.to_crs("EPSG:4326")
total_bounds = gdf.total_bounds
wgs_bounds = gdf_wgs84.total_bounds
wgs_json = json.dumps([
    [round(wgs_bounds[1], 5), round(wgs_bounds[0], 5)],
    [round(wgs_bounds[3], 5), round(wgs_bounds[2], 5)]
])

geojson_dict = json.loads(gdf_wgs84.to_json())
def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in geojson_dict["features"]:
    if feat.get("geometry") and "coordinates" in feat["geometry"]:
        feat["geometry"]["coordinates"] = round_coords(feat["geometry"]["coordinates"])

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\apa_itupararanga_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

# Atualizar também o arquivo de compatibilidade anterior se chamado
with open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\apa_itupararanga_limite_sao_roque_web.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"GeoJSON salvo: {geojson_path} ({sz_kb:.1f} KB)")

# Ingestão no SQLite
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Atualizar camadas_territoriais
c.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico,
    responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica,
    status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'apa_itupararanga',
    'Área de Proteção Ambiental da Represa de Itupararanga (APA Itupararanga)',
    'DELIMITAÇÃO TERRITORIAL E LIMITE NORTE DA APA ITUPARARANGA',
    'Unidade de Conservação Estadual',
    'Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf',
    'vetor_poligonos_e_linhas',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '15/01/2019',
    'Governo do Estado de São Paulo / Fundação Florestal',
    'SEMIL-SP',
    'Secretaria Municipal de Planejamento de São Roque',
    'PDA 2019',
    'Lei Estadual nº 11.579/2003 e Decreto Estadual nº 52.879/2008 (Plano de Manejo)',
    'Auditado e Demarcado (Polígono Sul de 10.805,84 ha + Linha Divisória de 18,59 km)',
    ?, ?, ?, ?,
    ?,
    '🌊 REGIME JURÍDICO ESTADUAL DA APA ITUPARARANGA: A totalidade da porção sul de São Roque (10.805,84 ha / 35,19% do município) está sob a jurisdição ambiental especial da Lei Estadual nº 11.579/2003 e do Decreto Estadual nº 52.879/2008 (Plano de Manejo). Qualquer obra, loteamento ou supressão vegetal necessita de anuência prévia da Fundação Florestal, licenciamento da CETESB e atendimento às Zonas de Proteção aos Mananciais da LC nº 39/2006 (Arts. 60-64).'
)
""", (
    round(total_bounds[0], 2), round(total_bounds[2], 2),
    round(total_bounds[1], 2), round(total_bounds[3], 2),
    wgs_json
))

# 2. Inserir em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id IN ('apa_itupararanga', 'apa_itupararanga_limite')")

c.execute("""
INSERT INTO classes_camada_territorial
(camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "apa_itupararanga",
    "POLIGONO_APA",
    "Território da APA Itupararanga em São Roque",
    "Bacia de Mananciais",
    "#0070FF",
    "RGB(0, 112, 255)",
    "Lei Estadual nº 11.579/2003 / Decreto Estadual nº 52.879/2008",
    f"Polígono territorial de {area_apa_ha} ha ({pct_municipio}% do município) ao sul da linha divisória de águas. Regime especial de uso sustentável e proteção de mananciais."
))

c.execute("""
INSERT INTO classes_camada_territorial
(camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "apa_itupararanga",
    "LIMITE_NORTE_APA",
    "Limite Norte da APA Itupararanga",
    "Divisor Hidrográfico",
    "#E60000",
    "RGB(230, 0, 0)",
    "Lei Estadual nº 11.579/2003 / PDA 2019",
    f"Linha divisória de {extensao_km} km. Separa a bacia de proteção aos mananciais a sul do território não enquadrado a norte."
))

# 3. Inserir em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id IN ('apa_itupararanga', 'apa_itupararanga_limite')")
apa_laws = [
    ("apa_itupararanga", "POLIGONO_APA", "Estadual", "Lei", "11579", 2003, "Arts. 1º a 8º", "Criação de Unidade de Conservação", "Criação da APA da Represa de Itupararanga e definição territorial da área de mananciais em São Roque.", "Jurisdição ambiental compartilhada com a Fundação Florestal e a CETESB."),
    ("apa_itupararanga", "POLIGONO_APA", "Estadual", "Decreto", "52879", 2008, "Decreto Integral", "Regulamentação e Plano de Manejo", "Aprova o Zoneamento e Plano de Manejo da APA Itupararanga (Zonas de Conservação da Vida Silvestre, Ocupação Controlada e Uso Sustentável).", "Parâmetros urbanísticos restritivos, vedação de indústrias poluentes e taxa de permeabilidade mínima obrigatória."),
    ("apa_itupararanga", "POLIGONO_APA", "Estadual", "Lei", "9866", 1997, "Arts. 3º e 4º", "Proteção de Mananciais", "Diretrizes estaduais para a proteção e recuperação dos mananciais de interesse da Região Metropolitana e bacias vizinhas.", "Qualquer parcelamento urbano exige comprovação de 100% de coleta e tratamento de efluentes."),
    ("apa_itupararanga", "POLIGONO_APA", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Integração Municipal", "Reconhecimento municipal da APA de Itupararanga como Zona de Proteção aos Mananciais no Plano Diretor.", "Condicionamento dos alvarás de construção da Prefeitura à conformidade com a legislação da APA."),
    ("apa_itupararanga", "POLIGONO_APA", "Municipal", "Lei Complementar", "40", 2006, "Art. 24 e 25", "Uso e Ocupação Restritivos", "Coeficientes de aproveitamento reduzidos e exigência de áreas verdes permeáveis nos lotes da bacia do Itupararanga.", "Atenção redobrada aos recuos e impermeabilização do solo."),
    ("apa_itupararanga", "POLIGONO_APA", "Federal", "Lei", "9985", 2000, "Art. 15", "SNUC - Uso Sustentável", "Enquadramento da APA como Unidade de Conservação de Uso Sustentável.", "Objetivo de compatibilizar a conservação da natureza com o uso sustentável de parcela dos recursos naturais."),
    ("apa_itupararanga", "LIMITE_NORTE_APA", "Estadual", "Lei", "11579", 2003, "Art. 2º", "Delimitação Legal", "Demarcação do divisor de águas setentrional da Bacia do Rio Sorocaba em São Roque.", "Ao sul desta linha incidem todas as restrições ambientais estaduais da APA.")
]

for row in apa_laws:
    c.execute("""
    INSERT INTO cruzamento_camada_legislacao
    (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

c.execute("SELECT count(*) FROM cruzamento_camada_legislacao")
total_laws = c.fetchone()[0]
c.execute("SELECT count(*) FROM camadas_territoriais")
total_layers = c.fetchone()[0]
conn.close()

print(f"Banco de dados atualizado: {total_layers} camadas ativas, {total_laws} vinculações normativas registradas!")
print(f"=== SUCESSO TOTAL EM {time.time()-t_total_start:.1f}s ===")
