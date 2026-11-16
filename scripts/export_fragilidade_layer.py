import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import json
import sqlite3
from shapely.geometry import Polygon, MultiPolygon, mapping
from shapely.validation import make_valid
from shapely.ops import unary_union
import geopandas as gpd
from pyproj import Transformer

print("=== EXPORTAÇÃO DA CAMADA DE FRAGILIDADE POTENCIAL (ANEXO 7.3.1-1) ===")
t_total_start = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Mapa Fragilidade Potencial.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x, intercept_x = 17.639957, 273175.28
slope_y, intercept_y = 17.638071, 7380747.19

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

red, grn, blu, alf = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
x, y = ctypes.c_float(), ctypes.c_float()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

class_metadata = {
    '#006100': {
        'codigo_classe': 'muito_fraca',
        'nome_classe': 'Muito Fraca',
        'vulnerabilidade': 'Muito Baixa Vulnerabilidade à Erosão',
        'restricao_uso': 'Fundos de vale aluvionares e planícies com relevo plano a suave-ondulado e solos profundos. Baixa restrição morfodinâmica geral, ressalvada a faixa marginal de APP dos cursos d\'água (Lei 12.651/12).',
        'legislacao_principal': 'LC nº 39/06 (art. 12), LC nº 40/06 (art. 24), Lei Federal nº 12.651/12 (art. 4º)'
    },
    '#7AAB00': {
        'codigo_classe': 'fraca',
        'nome_classe': 'Fraca',
        'vulnerabilidade': 'Baixa Vulnerabilidade à Erosão',
        'restricao_uso': 'Colinas e relevo suave com baixa declividade e boa estabilidade pedológica. Permite ocupação urbana e agrícola com sistemas adequados de drenagem pluvial.',
        'legislacao_principal': 'LC nº 39/06 (art. 13), LC nº 40/06 (art. 25), LC nº 41/06 (art. 15), Lei nº 6.766/79'
    },
    '#FFFF00': {
        'codigo_classe': 'media',
        'nome_classe': 'Média',
        'vulnerabilidade': 'Média Vulnerabilidade à Erosão',
        'restricao_uso': 'Relevo ondulado dominante do município com suscetibilidade intermediária a processos erosivos e sulcos. Exige controle rigoroso de terraplenagem, contenção de taludes e manejo de águas pluviais.',
        'legislacao_principal': 'LC nº 39/06 (art. 18), LC nº 40/06 (art. 31), LC nº 41/06 (art. 18), Lei nº 12.608/12'
    },
    '#FF0000': {
        'codigo_classe': 'forte',
        'nome_classe': 'Forte',
        'vulnerabilidade': 'Alta Vulnerabilidade à Erosão',
        'restricao_uso': 'Encostas íngremes e áreas de declividade elevada com alto risco de ravinamento e escorregamentos. Restrição severa a cortes e aterros; proibido parcelamento em declividades > 30% sem laudo geotécnico circunstanciado.',
        'legislacao_principal': 'LC nº 39/06 (art. 18), LC nº 41/06 (art. 42), Lei Federal nº 6.766/79 (art. 3º), Lei Federal nº 12.608/12 (art. 8º)'
    },
    '#A80000': {
        'codigo_classe': 'muito_forte',
        'nome_classe': 'Muito Forte',
        'vulnerabilidade': 'Muito Alta Vulnerabilidade / Escarpas e Cristas',
        'restricao_uso': 'Escarpas rochosas, cristas de serras e encostas com solos rasos ou afloramentos rochosos. Áreas não edificáveis de preservação permanente e contenção morfológica absoluta.',
        'legislacao_principal': 'LC nº 39/06 (art. 18), LC nº 40/06 (art. 31), Lei nº 12.651/12 (art. 4º, IX), STF ADPF 747/749'
    }
}

polys_by_color = {c: [] for c in class_metadata}

print("1. Extraindo polígonos nativos do PDF...")
t0 = time.time()
for p in objs:
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            if left.value >= 25 and right.value <= 1675:
                pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(red), ctypes.byref(grn), ctypes.byref(blu), ctypes.byref(alf))
                f_hex = f'#{red.value:02X}{grn.value:02X}{blu.value:02X}'
                if f_hex in class_metadata:
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
                    for sp in subpaths:
                        if len(sp) >= 3:
                            if sp[0] != sp[-1]:
                                sp.append(sp[0])
                            poly = Polygon(sp)
                            if not poly.is_valid:
                                poly = make_valid(poly)
                            if not poly.is_empty and poly.area > 25:
                                polys_by_color[f_hex].append(poly)

doc.close()
print(f"   Extração concluída em {time.time()-t0:.1f}s.")

print("2. Dissolvendo classes (eliminação de costuras internas)...")
dissolved = {}
for c, plist in polys_by_color.items():
    t_c = time.time()
    simplified = [p.simplify(1.0, preserve_topology=True) for p in plist]
    u = unary_union(simplified)
    if not u.is_valid:
        u = make_valid(u)
    dissolved[c] = u
    print(f"   {class_metadata[c]['nome_classe']} ({c}): {len(plist)} partes -> {u.area/10000.0:.2f} ha em {time.time()-t_c:.1f}s")

print("3. Ajustando sobreposição topológica da classe Média (background)...")
other_classes = unary_union([dissolved['#006100'], dissolved['#7AAB00'], dissolved['#FF0000'], dissolved['#A80000']])
cleaned_yellow = dissolved['#FFFF00'].difference(other_classes)
if not cleaned_yellow.is_valid:
    cleaned_yellow = make_valid(cleaned_yellow)
dissolved['#FFFF00'] = cleaned_yellow
print(f"   Média limpa: {dissolved['#FFFF00'].area/10000.0:.2f} ha")

total_ha = sum(g.area for g in dissolved.values()) / 10000.0
print(f"\nÁrea Total Final: {total_ha:.2f} ha (PDA Oficial: 30.709,52 ha)")

# Montar GeoDataFrame
records = []
for c, geom in dissolved.items():
    meta = class_metadata[c]
    area_ha = round(geom.area / 10000.0, 2)
    pct = round((area_ha / total_ha) * 100, 2)
    records.append({
        'camada': 'Fragilidade Potencial e Erosão',
        'anexo_oficial': 'Anexo 7.3.1-1 - PDA 2019',
        'codigo_classe': meta['codigo_classe'],
        'nome_classe': meta['nome_classe'],
        'cor_hex': c,
        'vulnerabilidade': meta['vulnerabilidade'],
        'area_ha': area_ha,
        'porcentagem': pct,
        'restricao_uso': meta['restricao_uso'],
        'legislacao_principal': meta['legislacao_principal'],
        'geometry': geom
    })

gdf = gpd.GeoDataFrame(records, crs="EPSG:31983")

# Salvar GeoPackage
gpkg_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\fragilidade_potencial_sao_roque.gpkg"
gdf.to_file(gpkg_path, layer="fragilidade_potencial", driver="GPKG")
print(f"4. GeoPackage gravado com sucesso: {gpkg_path}")

# Reprojetar para EPSG:4326 e salvar GeoJSON com 5 casas decimais
print("5. Reprojetando para WGS84 (EPSG:4326) e otimizando GeoJSON...")
gdf_wgs84 = gdf.to_crs("EPSG:4326")

geojson_dict = json.loads(gdf_wgs84.to_json())
def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in geojson_dict["features"]:
    feat["geometry"]["coordinates"] = round_coords(feat["geometry"]["coordinates"])

geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\fragilidade_potencial_sao_roque_web.geojson"
with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, separators=(',', ':'))

import os
sz_kb = os.path.getsize(geojson_path) / 1024.0
print(f"   GeoJSON gravado: {geojson_path} ({sz_kb:.1f} KB)")

# 6. Ingestão no SQLite
print("6. Ingerindo metadados no SQLite sao_roque_geodados.db...")
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Atualizar camadas_territoriais
cur.execute("""
INSERT OR REPLACE INTO camadas_territoriais 
(id, nome, categoria, ano_base, orgao_fonte, escala_original, sistema_referencia, tipo_geometria, total_poligonos, area_total_ha, status_auditoria, descricao)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "fragilidade_potencial",
    "Fragilidade Potencial e Erosão (Anexo 7.3.1-1)",
    "Ambiental e Geotécnica",
    2019,
    "Prefeitura Municipal de São Roque / PDA 2019 / Ross (1994) / Crepani et al. (2008)",
    "1:50.000",
    "SIRGAS 2000 / UTM zone 23S (EPSG:31983)",
    "MultiPolygon",
    5,
    round(total_ha, 2),
    "Auditado e Dissolvido (Calibração Vetorial Sub-Métrica, 5 Classes Sem Falsas Divisões)",
    "Mapeamento temático oficial da fragilidade ambiental e suscetibilidade à erosão mecânica e hidrológica do solo de São Roque em 5 classes morfodinâmicas, integrando relevo, declividade, litologia e cobertura pedológica conforme Anexo 7.3.1-1 do Plano Diretor Ambiental."
))

# Inserir classes em classes_camada_territorial
cur.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'fragilidade_potencial'")
for r in records:
    cur.execute("""
    INSERT INTO classes_camada_territorial
    (camada_id, classe_id, nome_classe, cor_hex, descricao, restricao_uso)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "fragilidade_potencial",
        r['codigo_classe'],
        r['nome_classe'],
        r['cor_hex'],
        f"{r['vulnerabilidade']} · Área: {r['area_ha']} ha ({r['porcentagem']}%)",
        r['restricao_uso']
    ))

# Inserir cruzamento com legislação
cur.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'fragilidade_potencial'")
fragilidade_laws = [
    ("fragilidade_potencial", "muito_fraca", "Federal", "Lei", "12651", 2012, "Art. 4º, I", "Restrição Proporcional à Faixa Marginal", "Preservação da faixa de APP ao longo dos corpos hídricos em fundos de vale aluvionares.", "Incompatibilidade de qualquer edificação não dispensável dentro da faixa non aedificandi de APP."),
    ("fragilidade_potencial", "fraca", "Municipal", "Lei Complementar", "40", 2006, "Arts. 24 e 25", "Permissivo com Mitigação", "Ocupação urbana e rural com implantação de rede de macro e microdrenagem pluvial para evitar processos de ravinamento.", "Atenção ao coeficiente de permeabilidade do solo para evitar saturação superficial."),
    ("fragilidade_potencial", "media", "Municipal", "Lei Complementar", "39", 2006, "Art. 18", "Condicionado", "Condicionamento de projetos de loteamento e terraplenagem a obras de contenção de taludes e terraceamento.", "Exigência de medidas preventivas de contenção em cortes de morro superiores a 3 metros."),
    ("fragilidade_potencial", "media", "Municipal", "Lei Complementar", "41", 2006, "Art. 18", "Técnica Obrigatória", "Exigência de laudo geotécnico e dimensionamento de águas pluviais para aprovação de edificações residenciais e industriais.", "Responsabilidade técnica por ART/RRT de estabilidade do terreno."),
    ("fragilidade_potencial", "forte", "Federal", "Lei", "6766", 1979, "Art. 3º, Parágrafo Único", "Vedação / Restrição Severa", "Proibição expressa de parcelamento do solo em terrenos com declividade igual ou superior a 30% ou sujeitos a erosão e deslizamento.", "Áreas com declividade acentuada requerem comprovação de estabilidade absoluta e atendimento às diretrizes do Plano Diretor."),
    ("fragilidade_potencial", "forte", "Federal", "Lei", "12608", 2012, "Arts. 3º e 8º", "Vigilância Geotécnica", "Mapeamento obrigatório de áreas suscetíveis à ocorrência de deslizamentos de grande impacto e processos correlatos.", "Prioridade máxima de fiscalização municipal pela Defesa Civil em eventos pluviométricos extremos."),
    ("fragilidade_potencial", "muito_forte", "Estadual / Federal", "STF ADPF", "747", 2021, "Acórdão Plenário", "Proteção Integral", "Declaração de inconstitucionalidade da Resolução CONAMA 500/2020, restaurando a proteção permanente das escarpas, topos de morro e cristas.", "Nenhuma autorização municipal de desmatamento ou supressão de vegetação pode subsistir em topos de morro ou áreas de preservação permanente.")
]

for row in fragilidade_laws:
    cur.execute("""
    INSERT INTO cruzamento_camada_legislacao
    (camada_id, classe_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, row)

conn.commit()

# Auditoria final do banco
cur.execute("SELECT count(*) FROM cruzamento_camada_legislacao")
total_laws = cur.fetchone()[0]
cur.execute("SELECT count(*) FROM camadas_territoriais")
total_layers = cur.fetchone()[0]
conn.close()

print(f"   Banco de dados atualizado: {total_layers} camadas ativas, {total_laws} vinculações normativas registradas!")
print(f"=== SUCESSO TOTAL EM {time.time()-t_total_start:.1f}s ===")
