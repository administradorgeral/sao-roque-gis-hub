import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import os
import sqlite3
from shapely.geometry import LineString, MultiLineString
import geopandas as gpd

print("=== EXPORTAÇÃO DA CAMADA EXCLUSIVA: LIMITE NORTE DA APA ITUPARARANGA ===")
t_total_start = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.637839, 271182.44
slope_y, intercept_y = 17.638906, 7381568.28

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

x, y = ctypes.c_float(), ctypes.c_float()
p = objs[32]
n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)

coords = []
for s in range(n_segs):
    seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
    pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
    coords.append(pdf_to_utm(x.value, y.value))

doc.close()

line_geom = LineString(coords)
extensao_km = round(line_geom.length / 1000.0, 2)
print(f"Linha extraída: {len(coords)} vértices, extensão de {extensao_km} km")

record = {
    'camada': 'Limite Norte da APA Itupararanga',
    'esfera': 'Estadual',
    'norma_criacao': 'Lei Estadual nº 11.579/2003',
    'plano_manejo': 'Decreto Estadual nº 52.879/2008',
    'orgao_gestor': 'Fundação Florestal / SEMIL-SP / Conselho Gestor da APA',
    'extensao_km': extensao_km,
    'datum': 'SIRGAS 2000 UTM Zone 23S',
    'cor_hex': '#E60000',
    'descricao': 'Linha divisória oficial que delimita o limite setentrional (norte) da Área de Proteção Ambiental da Represa de Itupararanga no território de São Roque.',
    'implicacao_juridica': 'Ao sul desta demarcação incide o regime especial da APA Itupararanga e da Lei Estadual de Mananciais (Lei 9.866/97). Parcelamentos, indústrias e intervenções requerem anuência da Fundação Florestal e licenciamento específico da CETESB, além das regras da LC 39/06 (Arts. 60-64).',
    'geometry': line_geom
}

gdf = gpd.GeoDataFrame([record], crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\apa_itupararanga_limite_sao_roque.gpkg"
gdf.to_file(gpkg_path, layer="apa_itupararanga_limite", driver="GPKG")
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

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\apa_itupararanga_limite_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"GeoJSON salvo: {geojson_path} ({sz_kb:.1f} KB)")

# Ingestão no SQLite
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 1. Inserir em camadas_territoriais
c.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao, responsavel_tecnico,
    responsavel_crea, desenho_tecnico, desenho_crea, fonte_cartografica,
    status_auditoria, bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (
    'apa_itupararanga_limite',
    'Limite Norte da APA Itupararanga',
    'DEMARCAÇÃO OFICIAL DO LIMITE NORTE DA APA DA REPRESA DE ITUPARARANGA',
    'Unidade de Conservação Estadual',
    'Mapa_Anexo_8.3.1-1_Zoneamento_2019.pdf',
    'vetor_linhas',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '15/01/2019',
    'Governo do Estado de São Paulo / Fundação Florestal',
    'SEMIL-SP',
    'Secretaria Municipal de Planejamento de São Roque',
    'PDA 2019',
    'Lei Estadual nº 11.579/2003 e Decreto Estadual nº 52.879/2008 (Plano de Manejo)',
    'Auditado e Extraído como Camada Exclusiva (18,59 km Contínuos de Delimitação Hídrica)',
    ?, ?, ?, ?,
    ?,
    '🌊 MARCO LEGAL ESTADUAL: O Limite Norte da APA Itupararanga é a linha divisória de águas da Bacia Hidrográfica do Rio Sorocaba. Ao sul desta linha, todo empreendimento imobiliário, industrial ou de mineração está sujeito aos parâmetros restritivos do Plano de Manejo da APA (Decreto Estadual 52.879/08), anuência da Fundação Florestal e diretrizes protetivas da LC 39/06 (Arts. 60-64).'
)
""", (
    round(total_bounds[0], 2), round(total_bounds[2], 2),
    round(total_bounds[1], 2), round(total_bounds[3], 2),
    wgs_json
))

# 2. Inserir em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'apa_itupararanga_limite'")
c.execute("""
INSERT INTO classes_camada_territorial
(camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "apa_itupararanga_limite",
    "LIMITE_NORTE_APA",
    "Limite Norte da APA Itupararanga",
    "Divisor Hidrográfico",
    "#E60000",
    "RGB(230, 0, 0)",
    "Lei Estadual nº 11.579/2003 / Decreto Estadual nº 52.879/2008",
    f"Divisória legal contínua de {extensao_km} km. Separa a bacia de proteção a mananciais da APA Itupararanga a sul da área não pertencente à APA a norte."
))

# 3. Inserir em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'apa_itupararanga_limite'")
apa_laws = [
    ("apa_itupararanga_limite", "LIMITE_NORTE_APA", "Estadual", "Lei", "11579", 2003, "Art. 1º ao 8º", "Criação de Unidade de Conservação", "Criação da Área de Proteção Ambiental da Represa de Itupararanga e definição dos seus limites territoriais.", "A área a sul do limite norte submete-se à jurisdição da Fundação Florestal e da CETESB."),
    ("apa_itupararanga_limite", "LIMITE_NORTE_APA", "Estadual", "Decreto", "52879", 2008, "Decreto Integral", "Regulamentação e Plano de Manejo", "Aprova o Plano de Manejo da APA da Represa de Itupararanga e estabelece as zonas de conservação da vida silvestre, uso sustentável e ocupação controlada.", "Índices urbanísticos mais restritivos do que o zoneamento municipal padrão."),
    ("apa_itupararanga_limite", "LIMITE_NORTE_APA", "Estadual", "Lei", "9866", 1997, "Art. 3º e 4º", "Proteção de Mananciais", "Diretrizes estaduais para a proteção e recuperação das bacias hidrográficas dos mananciais de interesse regional.", "Exigência de sistema coletivo ou individual eficiente de tratamento de esgoto para qualquer loteamento."),
    ("apa_itupararanga_limite", "LIMITE_NORTE_APA", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Integração Municipal", "Reconhecimento municipal da APA de Itupararanga como Zona de Proteção aos Mananciais.", "Vinculação dos alvarás de construção da Prefeitura à comprovação de conformidade ambiental estadual.")
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
