import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import os
import sqlite3
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union
import geopandas as gpd

print("=== EXPORTAÇÃO DA CAMADA PEDOLÓGICA (ANEXO 4.3.6-1) ===")
t_total_start = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\1835_4_3_6_1 Pedológico.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.636295, 272427.45
slope_y, intercept_y = 17.636560, 7381364.75

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()

# Extrair os 6 polígonos
raw_units = []
for idx in [1, 2, 3, 4, 5, 6]:
    p = objs[idx]
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    current_sp = []
    subpaths = []
    for s in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
        stype = pdfium_c.FPDFPathSegment_GetType(seg)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        pt = pdf_to_utm(x.value, y.value)
        if stype == pdfium_c.FPDF_SEGMENT_MOVETO:
            if len(current_sp) >= 3:
                subpaths.append(current_sp)
            current_sp = [pt]
        else:
            current_sp.append(pt)
    if len(current_sp) >= 3:
        subpaths.append(current_sp)
    
    sp0 = subpaths[0]
    if sp0[0] != sp0[-1]:
        sp0.append(sp0[0])
    holes = []
    for h in subpaths[1:]:
        if len(h) >= 3:
            if h[0] != h[-1]:
                h.append(h[0])
            holes.append(h)
    poly = Polygon(sp0, holes)
    if not poly.is_valid:
        poly = make_valid(poly)
    raw_units.append((idx, poly))

doc.close()

# Dissolver PVA46 (Idx 3 e 5)
poly_pva19 = raw_units[0][1] # idx 1
poly_pva41 = raw_units[1][1] # idx 2
poly_pva46 = unary_union([raw_units[2][1], raw_units[4][1]]) # idx 3 e 5
poly_pva55 = raw_units[3][1] # idx 4
poly_lva17 = raw_units[5][1] # idx 6

units_config = [
    {
        'codigo_classe': 'PVA19',
        'macroclasse': 'PVA - Argissolos Vermelho-Amarelos',
        'nome_classe': 'PVA19 · Argissolos Vermelho-Amarelos Distróficos A moderado',
        'cor_hex': '#FFA77F',
        'textura': 'Textura média/argilosa e argilosa',
        'relevo': 'Relevo forte ondulado e ondulado',
        'associacao': 'Argissolos Vermelho-Amarelos Distróficos puros',
        'permeabilidade': 'Média a Lenta no horizonte B textural (suscetível a erosão hídrica em sulcos)',
        'implicacao_obras': 'Exige drenagem superficial eficiente e contenção de taludes (LC 41/06); bom suporte quando confinado.',
        'legislacao_principal': 'LC nº 39/06 (Art. 18), LC nº 40/06 (Art. 24), LC nº 41/06 (Art. 15), Lei 12.608/12',
        'geometry': poly_pva19
    },
    {
        'codigo_classe': 'LVA17',
        'macroclasse': 'LVA - Latossolos Vermelho-Amarelos',
        'nome_classe': 'LVA17 · Latossolos Vermelho-Amarelos Distróficos',
        'cor_hex': '#FFEBBE',
        'textura': 'Textura argilosa profunda',
        'relevo': 'Relevo ondulado a suave ondulado',
        'associacao': 'Associação com Cambissolos Háplicos Distróficos (relevo ondulado e forte ondulado)',
        'permeabilidade': 'Alta e boa drenabilidade natural em profundidade (excelente capacidade de infiltração)',
        'implicacao_obras': 'Solos profundos e estáveis; exigem preservação da recarga de aquíferos (APA Itupararanga / LC 39/06).',
        'legislacao_principal': 'LC nº 39/06 (Art. 60-64), Lei Estadual nº 11.579/03 (APA Itupararanga), Lei 6.766/79',
        'geometry': poly_lva17
    },
    {
        'codigo_classe': 'PVA41',
        'macroclasse': 'PVA - Argissolos Vermelho-Amarelos',
        'nome_classe': 'PVA41 · Argissolos Vermelho-Amarelos + Cambissolos Háplicos',
        'cor_hex': '#FF7F50',
        'textura': 'Textura argilosa e média',
        'relevo': 'Relevo forte ondulado e montanhoso (ambos A moderado)',
        'associacao': 'Associação com Cambissolos Háplicos Distróficos textura argilosa e média',
        'permeabilidade': 'Média a Baixa nas vertentes íngremes; horizonte B textural sobre solos rasos em transição',
        'implicacao_obras': 'Risco acentuado de escorregamento em cortes; sondagem prévia obrigatória (LC 41/06 Art. 18).',
        'legislacao_principal': 'LC nº 39/06 (Art. 18), LC nº 41/06 (Art. 18 e 42), Lei Federal nº 6.766/79 (Art. 3º)',
        'geometry': poly_pva41
    },
    {
        'codigo_classe': 'PVA46',
        'macroclasse': 'PVA - Argissolos Vermelho-Amarelos',
        'nome_classe': 'PVA46 · Argissolos Vermelho-Amarelos + Cambissolos Tb Distróficos',
        'cor_hex': '#FF8C69',
        'textura': 'Textura média/argilosa (fase não pedregosa e pedregosa)',
        'relevo': 'Relevo ondulado e forte ondulado',
        'associacao': 'Associação com Cambissolos Háplicos Tb Distróficos fase pedregosa',
        'permeabilidade': 'Média; pedregosidade e cascalhos limitam escavações e terraplenagens rasas',
        'implicacao_obras': 'Atenção ao contato solo-rocha e presença de matacões/pedregulhos em fundações (LC 41/06).',
        'legislacao_principal': 'LC nº 40/06 (Art. 25), LC nº 41/06 (Art. 15), Lei Federal nº 12.608/12',
        'geometry': poly_pva46
    },
    {
        'codigo_classe': 'PVA55',
        'macroclasse': 'PVA - Argissolos Vermelho-Amarelos',
        'nome_classe': 'PVA55 · Argissolos Vermelho-Amarelos (Fase Rochosa) + Latossolos',
        'cor_hex': '#E97451',
        'textura': 'Textura argilosa e média/argilosa (fase rochosa)',
        'relevo': 'Relevo forte ondulado e montanhoso',
        'associacao': 'Associação com Latossolos Vermelho-Amarelos Distróficos textura argilosa',
        'permeabilidade': 'Variável; afloramentos rochosos e alta declividade geram escoamento superficial rápido',
        'implicacao_obras': 'Restrição severa a parcelamento urbano; proteção ambiental de cristas rochosas (STF ADPF 747).',
        'legislacao_principal': 'Lei Federal nº 6.766/79 (Art. 3º), Lei nº 12.651/12 (Art. 4º), STF ADPF 747/749',
        'geometry': poly_pva55
    }
]

total_area_ha = sum(u['geometry'].area for u in units_config) / 10000.0
print(f"Área Pedológica Total: {total_area_ha:.2f} ha (PDA São Roque: 30.709,52 ha)")

records = []
for u in units_config:
    area_ha = round(u['geometry'].area / 10000.0, 2)
    pct = round((area_ha / total_area_ha) * 100, 2)
    records.append({
        'camada': 'Solos e Unidades Pedológicas',
        'anexo_oficial': 'Anexo 4.3.6-1 - PDA 2019',
        'codigo_classe': u['codigo_classe'],
        'macroclasse': u['macroclasse'],
        'nome_classe': u['nome_classe'],
        'cor_hex': u['cor_hex'],
        'textura': u['textura'],
        'relevo': u['relevo'],
        'associacao': u['associacao'],
        'permeabilidade': u['permeabilidade'],
        'area_ha': area_ha,
        'porcentagem': pct,
        'implicacao_obras': u['implicacao_obras'],
        'legislacao_principal': u['legislacao_principal'],
        'geometry': u['geometry']
    })
    print(f"  {u['codigo_classe']}: {area_ha} ha ({pct}%)")

gdf = gpd.GeoDataFrame(records, crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\pedologico_sao_roque.gpkg"
gdf.to_file(gpkg_path, layer="pedologico", driver="GPKG")
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
    feat["geometry"]["coordinates"] = round_coords(feat["geometry"]["coordinates"])

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\pedologico_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"GeoJSON salvo: {geojson_path} ({sz_kb:.1f} KB)")

# Ingestão no SQLite sao_roque_geodados.db
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
    'pedologico',
    'Solos e Unidades Pedológicas',
    'ANEXO 4.3.6-1 - MAPA PEDOLÓGICO DO MUNICÍPIO DE SÃO ROQUE',
    'Ambiental e Geotécnica',
    '1835_4_3_6_1 Pedológico.pdf',
    'vetor_poligonos',
    '1:50.000',
    'SIRGAS 2000 UTM Zone 23S',
    '12/11/2018',
    'Maurício Scorsatto Sartori (Eng. Florestal)',
    '5.060.532.187',
    'Ana Clara Cerminaro (Analista de Geoprocessamento)',
    '473.423.455',
    'Instituto Agronômico de Campinas (IAC 1999) / EMBRAPA Solos / IGC (1978)',
    'Auditado, Calibrado e Dissolvido (5 Unidades Pedológicas Oficiais PDA 2019)',
    ?, ?, ?, ?,
    ?,
    '🌱 DIRETRIZ PEDOLÓGICA E DE FUNDAÇÕES: Os Argissolos Vermelho-Amarelos (PVA) dominam 76,5% do município e apresentam forte gradiente textural entre horizontes A e B (risco de erosão laminar e em sulcos sob desmatamento), exigindo sondagem mecânica prévia (LC 41/06 Art. 18). Os Latossolos Vermelho-Amarelos (LVA - 23,5%) são profundos e permeáveis, cruciais para a recarga hídrica da APA Itupararanga (Lei Estadual 11.579/03 e LC 39/06 Arts. 60-64).'
)
""", (
    round(total_bounds[0], 2), round(total_bounds[2], 2),
    round(total_bounds[1], 2), round(total_bounds[3], 2),
    wgs_json
))

# 2. Inserir em classes_camada_territorial
c.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'pedologico'")
for r in records:
    c.execute("""
    INSERT INTO classes_camada_territorial
    (camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "pedologico",
        r['codigo_classe'],
        r['nome_classe'],
        r['textura'],
        r['cor_hex'],
        f"RGB({int(r['cor_hex'][1:3], 16)}, {int(r['cor_hex'][3:5], 16)}, {int(r['cor_hex'][5:7], 16)})",
        "IAC (1999) / EMBRAPA Solos / PDA 2019",
        f"{r['implicacao_obras']} · Relevo: {r['relevo']} · Área: {r['area_ha']} ha ({r['porcentagem']}%)"
    ))

# 3. Inserir em cruzamento_camada_legislacao
c.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'pedologico'")
pedologico_laws = [
    ("pedologico", "PVA19", "Municipal", "Lei Complementar", "41", 2006, "Arts. 15 e 18", "Técnica Obrigatória", "Exigência de sondagem de solo (SPT) e ensaios de permeabilidade para aprovação de fundações em Argissolos com horizonte B textural.", "Atenção ao risco de recalque diferencial em transição de corte e aterro."),
    ("pedologico", "PVA41", "Municipal", "Lei Complementar", "40", 2006, "Art. 24", "Restritiva", "Exigência de contenção de taludes e proteção superficial contra erosão em relevo forte ondulado e montanhoso.", "Proibição de cortes abruptos sem muro de arrimo ou retaludamento dimensionado por ART."),
    ("pedologico", "LVA17", "Estadual", "Lei", "11579", 2003, "Arts. 4º a 8º", "Proteção de Mananciais", "Preservação da capacidade de infiltração natural dos Latossolos Vermelho-Amarelos na APA da Represa de Itupararanga.", "Infiltração de efluentes no solo condicionada a fossa séptica técnica licenciada pela CETESB."),
    ("pedologico", "LVA17", "Municipal", "Lei Complementar", "39", 2006, "Arts. 60 a 64", "Diretriz de Sustentabilidade", "Zona de Proteção aos Mananciais municipais e manutenção de altos coeficientes de permeabilidade em áreas de Latossolo.", "Taxa de permeabilidade mínima obrigatória nos lotes urbanos e rurais."),
    ("pedologico", "PVA46", "Federal", "Lei", "12608", 2012, "Arts. 3º e 8º", "Vigilância Geotécnica", "Mapeamento e fiscalização das áreas com solos pedregosos e Cambissolos associados sujeitos a rastejo e escorregamentos.", "Integração ao Plano de Contingência da Defesa Civil Municipal."),
    ("pedologico", "PVA55", "Federal", "Lei", "6766", 1979, "Art. 3º, Parágrafo Único", "Vedação / Restrição Severa", "Veda o parcelamento do solo em terrenos com declividade acentuada e solos com afloramentos rochosos sem laudo de viabilidade.", "Comprovação técnica de escoamento das águas pluviais e estabilidade pedológica."),
    ("pedologico", "PVA55", "Estadual / Federal", "STF ADPF", "747", 2021, "Acórdão Plenário", "Proteção Integral", "Proteção das cristas rochosas e topos de morro com solos delgados contra degradação e desmatamento.", "Áreas non aedificandi de preservação permanente.")
]

for row in pedologico_laws:
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
c.execute("SELECT count(*) FROM classes_camada_territorial WHERE camada_id = 'pedologico'")
total_classes = c.fetchone()[0]
conn.close()

print(f"Banco de dados atualizado: {total_layers} camadas ativas, {total_classes} classes de solo, {total_laws} vinculações normativas registradas!")
print(f"=== SUCESSO TOTAL EM {time.time()-t_total_start:.1f}s ===")
