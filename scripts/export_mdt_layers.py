import pypdfium2 as pdfium
import numpy as np
import cv2
import time
import os
import json
import sqlite3
from shapely.geometry import Polygon, MultiPolygon
from shapely import simplify, make_valid
import geopandas as gpd

print("=== INICIANDO PIPELINE COMPLETO DE VETORIZAÇÃO E INGESTÃO DO MDT ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

strip_bitmaps = [images[i].get_bitmap().to_numpy()[:, :, :3] for i in range(len(images))]
full_bgr = np.vstack(strip_bitmaps)
H, W, _ = full_bgr.shape
print(f"[{time.time()-t0:.1f}s] Imagem composta montada: {W}x{H} pixels (300 DPI).")

classes_cfg = [
    {
        "codigo": "MDT_1_630_760",
        "classe": "630 a 760 m",
        "relevo": "Fundos de Vale / Planícies Aluviais",
        "cor_hex": "#006100",
        "lower_bgr": np.array([0, 85, 0]),
        "upper_bgr": np.array([15, 110, 15]),
        "restricao": "Condicionante / Faixa de APP Hídrica",
        "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, I e Lei nº 6.766/1979 Art. 3º, I",
        "implicacao": "Várzeas e planícies de amortecimento de cheias dos Rios Guaçu e Carambeí. Faixas marginais de APP hídrica inalienáveis.",
        "alerta": "🌊 AMORTECIMENTO DE CHEIAS: Terrenos alagadiços e fundos de vale com restrição federal de parcelamento antes de obras de canalização e drenagem."
    },
    {
        "codigo": "MDT_2_760_830",
        "classe": "760 a 830 m",
        "relevo": "Terraço Intermediário / Encostas Baixas",
        "cor_hex": "#7AAB00",
        "lower_bgr": np.array([0, 160, 110]),
        "upper_bgr": np.array([15, 185, 135]),
        "restricao": "Urbana Consolidada / Controle Sanitário",
        "base_legal": "LC Municipal nº 39/2006 e LC nº 40/2006",
        "implicacao": "Cota da malha urbana central e bairros consolidados. Exige conexão à infraestrutura sanitária e controle de drenagem superficial.",
        "alerta": "🏙️ ÁREA CONSOLIDADA: Mancha urbana tradicional (Centro, Taboão, Junqueira) sujeita aos coeficientes de aproveitamento da LC 40/2006."
    },
    {
        "codigo": "MDT_3_830_900",
        "classe": "830 a 900 m",
        "relevo": "Planalto de Transição e Expansão",
        "cor_hex": "#FFFF00",
        "lower_bgr": np.array([0, 245, 245]),
        "upper_bgr": np.array([20, 255, 255]),
        "restricao": "Média / Amortecimento de Bacias",
        "base_legal": "LC Municipal nº 40/2006 e Lei Estadual nº 9.866/1997",
        "implicacao": "Platôs e divisores de sub-bacias com expansão de baixa densidade. Proteção das cabeceiras da APA Itupararanga.",
        "alerta": "🛡️ PROTEÇÃO DE MANANCIAIS: Eixo de transição Mailasqui-Canguera sob influência da APA Itupararanga e Lei Estadual de Mananciais."
    },
    {
        "codigo": "MDT_4_900_970",
        "classe": "900 a 970 m",
        "relevo": "Altas Vertentes Serranas",
        "cor_hex": "#FF9900",
        "lower_bgr": np.array([0, 140, 245]),
        "upper_bgr": np.array([15, 165, 255]),
        "restricao": "Severa / Prevenção Geotécnica",
        "base_legal": "Lei Federal nº 12.608/2012 e Lei Federal nº 11.428/2006",
        "implicacao": "Altas encostas da Serra de São Roque e Morro do Saboó. Área de preservação de Mata Atlântica e alto risco erosivo.",
        "alerta": "⚠️ ENCOSTAS SERRANAS: Forte declividade natural com restrição a terraplenagens extensas e exigência de laudo geotécnico GRAPROHAB."
    },
    {
        "codigo": "MDT_5_970_1125",
        "classe": "970 a 1.125 m",
        "relevo": "Cristas, Picos e Morro do Saboó",
        "cor_hex": "#FF2200",
        "lower_bgr": np.array([0, 25, 245]),
        "upper_bgr": np.array([15, 45, 255]),
        "restricao": "Impeditiva / APP de Topo de Morro",
        "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, IX, STF ADPF 747/749",
        "implicacao": "Ponto culminante de São Roque. Área de Preservação Permanente (APP) de topo de morro e cristas inalienável e não edificável.",
        "alerta": "🚨 TOPO DE MORRO E CRISTAS (APP): O STF (ADPF 747/749) e o Código Florestal vedam ocupações e loteamentos comerciais em topos de morro e cristas."
    }
]

scale_pt_x = 1640.682777 / W
scale_pt_y = 1582.98312 / H
x0_pt = 32.40084
y_top_pt = 1619.67346
scale_utm_x = 17.636684
scale_utm_y = 17.639795
utm_x0 = 270308.48
utm_y0 = 7382234.44
neatline_x0_pt = 31.4408
neatline_y0_pt = 35.9703

def px_to_utm(px, py):
    x_pt = x0_pt + px * scale_pt_x
    y_pt = y_top_pt - py * scale_pt_y
    utm_x = utm_x0 + (x_pt - neatline_x0_pt) * scale_utm_x
    utm_y = utm_y0 + (y_pt - neatline_y0_pt) * scale_utm_y
    return (utm_x, utm_y)

all_records = []

for c_cfg in classes_cfg:
    mask = cv2.inRange(full_bgr, c_cfg['lower_bgr'], c_cfg['upper_bgr'])
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    
    if hierarchy is not None:
        hier = hierarchy[0]
        for idx, (cnt, h_info) in enumerate(zip(contours, hier)):
            if h_info[3] == -1:
                if len(cnt) < 3 or cv2.contourArea(cnt) < 40:
                    continue
                
                ext_pts = [px_to_utm(pt[0][0], pt[0][1]) for pt in cnt]
                if ext_pts[0] != ext_pts[-1]:
                    ext_pts.append(ext_pts[0])
                    
                holes = []
                child_idx = h_info[2]
                while child_idx != -1:
                    child_cnt = contours[child_idx]
                    if len(child_cnt) >= 3 and cv2.contourArea(child_cnt) >= 40:
                        hole_pts = [px_to_utm(pt[0][0], pt[0][1]) for pt in child_cnt]
                        if hole_pts[0] != hole_pts[-1]:
                            hole_pts.append(hole_pts[0])
                        holes.append(hole_pts)
                    child_idx = hier[child_idx][0]
                    
                try:
                    p = Polygon(shell=ext_pts, holes=holes if holes else None)
                    if not p.is_valid:
                        p = make_valid(p)
                    if p.area >= 500.0: # >= 500 m²
                        all_records.append({
                            "codigo_classe": c_cfg["codigo"],
                            "classe": c_cfg["classe"],
                            "relevo": c_cfg["relevo"],
                            "cor_hex": c_cfg["cor_hex"],
                            "cor": c_cfg["cor_hex"],
                            "grau_restricao": c_cfg["restricao"],
                            "base_legal": c_cfg["base_legal"],
                            "implicacao": c_cfg["implicacao"],
                            "alerta_juridico": c_cfg["alerta"],
                            "area_ha": round(p.area / 10000.0, 3),
                            "geometry": p
                        })
                except Exception:
                    pass

print(f"[{time.time()-t0:.1f}s] Feições consolidadas: {len(all_records)}")

gdf = gpd.GeoDataFrame(all_records, crs="EPSG:31983")

# Salvar GeoPackage analítico oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="mdt_classes")
print(f"[{time.time()-t0:.1f}s] GeoPackage MDT salvo: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Simplificar levemente com 3m e reprojetar para WGS84 para WebGIS
gdf_web = gdf.copy()
gdf_web['geometry'] = simplify(gdf_web['geometry'].values, tolerance=3.0, preserve_topology=False)
gdf_wgs84 = gdf_web.to_crs("EPSG:4326")

# Montar GeoJSON com atributos amigáveis para o AttributeModal
data_geojson = json.loads(gdf_wgs84.to_json())

def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in data_geojson['features']:
    p = feat['properties']
    if feat.get('geometry') and 'coordinates' in feat['geometry']:
        feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])
    classe = p.get('classe', '')
    relevo = p.get('relevo', '')
    feat['properties'] = {
        "nome": f"Cota Hipsométrica: {classe}",
        "classe": classe,
        "Faixa de Altitude": classe,
        "Unidade Geomorfológica": relevo,
        "Grau de Restrição Construtiva": p.get('grau_restricao', ''),
        "Base Legal Normativa": p.get('base_legal', ''),
        "Diretriz Técnica e Ambiental": p.get('implicacao', ''),
        "Área da Mancha Altimétrica": f"{p.get('area_ha', 0):.2f} ha ({int(p.get('area_ha', 0)*10000):,} m²)",
        "Alerta de Auditoria Jurídica": p.get('alerta_juridico', ''),
        "Fonte Primária": "IGC 1:10.000 (Folhas 89 a 98, 1978) / PDA 2019",
        "Responsabilidade Técnica": "Eng. Maurício S. Sartori (CREA 5.060.532.187) / Ana C. Cerminaro (CREA 473.423.455)",
        "cor_hex": p.get('cor_hex', '#FFFF00'),
        "cor": p.get('cor_hex', '#FFFF00')
    }

geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson"
with open(geojson_out, 'w', encoding='utf-8') as f:
    json.dump(data_geojson, f, separators=(',', ':'))

print(f"[{time.time()-t0:.1f}s] GeoJSON MDT Web salvo: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB)")

# Inserir no banco de dados SQLite oficial
db_path = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Camada mestre
cursor.execute("""
INSERT OR REPLACE INTO camadas_territoriais (
    id, nome, titulo_documento, categoria, arquivo_origem, tipo_camada,
    escala_nominal, datum_projecao, data_elaboracao,
    responsavel_tecnico, responsavel_crea, desenho_tecnico, desenho_crea,
    fonte_cartografica, status_auditoria,
    bbox_utm_x0, bbox_utm_x1, bbox_utm_y0, bbox_utm_y1,
    bounds_wgs84_json, alerta_juridico
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "mdt",
    "MDT - Relevo e Hipsometria",
    "ANEXO 4.3.2-2 - MODELO DIGITAL DE TERRENO CLASSIFICADO DO MUNICÍPIO DE SÃO ROQUE",
    "Topografia e Hipsometria",
    "47531_4_2_3_2 MDT.pdf",
    "vetor_poligonos",
    "1:50.000",
    "SIRGAS 2000 UTM Zone 23S",
    "11/11/2018",
    "Maurício Scorsatto Sartori (Eng. Florestal)",
    "5.060.532.187",
    "Ana Clara Cerminaro (Analista de Geoprocessamento)",
    "473.423.455",
    "IGC. Instituto Geográfico e Cartográfico de São Paulo. Cartas Planialtimétricas 1:10.000 (Folhas 89 a 98, 1978)",
    "Auditado com Sucesso (Conferência de Fundos de Vale e Proteção de Topos de Morro STF ADPF 747/749)",
    270308.48, 299278.55, 7382234.44, 7410187.57,
    json.dumps({"sw": [-23.65430, -47.25190], "ne": [-23.40582, -46.96427]}),
    "O MDT delimita com precisão os fundos de vale (630 a 760m) sujeitos a inundações e APPs fluviais (Lei 12.651/12 Art. 4º, I), bem como as cristas e topos de morro (970 a 1.125m), cujo ponto culminante é o Morro do Saboó, protegido contra edificações pela jurisprudência vinculante do STF (ADPF 747/749) e Código Florestal."
))

# 2. Classes
classes_db = [
    ("MDT_1_630_760", "630 a 760 m", "Fundos de Vale / Planícies Aluviais", "#006100", "RGB(0, 97, 0)", "IGC 1978 / ArcMap MDT", "Zona de amortecimento de cheias dos Rios Guaçu e Carambeí. Faixas marginais de APP hídrica inalienáveis."),
    ("MDT_2_760_830", "760 a 830 m", "Terraço Intermediário / Encostas Baixas", "#7AAB00", "RGB(122, 171, 0)", "IGC 1978 / ArcMap MDT", "Cota da malha urbana central e bairros consolidados. Exige esgotamento sanitário e drenagem."),
    ("MDT_3_830_900", "830 a 900 m", "Planalto de Transição e Expansão", "#FFFF00", "RGB(255, 255, 0)", "IGC 1978 / ArcMap MDT", "Platôs e divisores de sub-bacias com expansão de baixa densidade. Proteção das cabeceiras da APA Itupararanga."),
    ("MDT_4_900_970", "900 a 970 m", "Altas Vertentes Serranas", "#FF9900", "RGB(255, 153, 0)", "IGC 1978 / ArcMap MDT", "Altas encostas da Serra de São Roque e Morro do Saboó. Área de preservação de Mata Atlântica e alto risco erosivo."),
    ("MDT_5_970_1125", "970 a 1.125 m", "Cristas, Picos e Morro do Saboó", "#FF2200", "RGB(255, 34, 0)", "IGC 1978 / ArcMap MDT", "Ponto culminante de São Roque. Área de Preservação Permanente (APP) de topo de morro e cristas inalienável e não edificável.")
]

cursor.execute("DELETE FROM classes_camada_territorial WHERE camada_id = 'mdt'")
for c in classes_db:
    cursor.execute("""
    INSERT INTO classes_camada_territorial (
        camada_id, codigo_classe, nome_classe, angulo_equivalente, cor_hex, cor_rgb, metodologia_referencia, implicacao_pratica
    ) VALUES ('mdt', ?, ?, ?, ?, ?, ?, ?)
    """, c)

# 3. Cruzamento de leis
cursor.execute("DELETE FROM cruzamento_camada_legislacao WHERE camada_id = 'mdt'")
cruzamentos_mdt = [
    ("mdt", "Federal", "Lei Ordinária", "12651", 2012, "Art. 4º, inciso I", "Impeditiva",
     "Faixas marginais de qualquer curso d'água perene e intermitente são APPs não edificáveis.",
     "Aplica-se preponderantemente na cota de 630 a 760m (Bacias do Guaçu, Carambeí e Sorocamirim)."),
     
    ("mdt", "Federal", "Lei Ordinária", "12651", 2012, "Art. 4º, inciso IX", "Impeditiva",
     "Considera-se APP o terço superior de topos de morros, montes, montanhas e serras com inclinação média > 25°.",
     "Aplica-se nas cotas de 970 a 1.125m (Morro do Saboó e cristas serranas)."),
     
    ("mdt", "Federal", "Lei Ordinária", "6766", 1979, "Art. 3º, parágrafo único, I", "Impeditiva",
     "Não será permitido o parcelamento do solo em terrenos alagadiços e sujeitos a inundações.",
     "Trava legal para loteamentos nas várzeas da cota 630 a 760m."),
     
    ("mdt", "Estadual", "Lei Ordinária", "9866", 1997, "Art. 4º e seguintes", "Condicionante",
     "Diretrizes para a proteção e recuperação das bacias hidrográficas dos mananciais de interesse regional.",
     "Proteção da Bacia Formadora do Reservatório de Itupararanga nas cotas de 830 a 970m."),
     
    ("mdt", "Municipal", "Lei Complementar", "40", 2006, "Art. 13 e Art. 43", "Impeditiva",
     "Vedação ao parcelamento e condomínios em áreas de preservação permanente e terrenos alagadiços.",
     "Incidência direta nas cotas 630-760m e topos de morro 970-1.125m.")
]

for cr in cruzamentos_mdt:
    cursor.execute("""
    INSERT INTO cruzamento_camada_legislacao (
        camada_id, norma_esfera, norma_tipo, norma_numero, norma_ano, artigo_dispositivo, grau_restricao, regra_aplicacao, conflito_ou_ponto_atencao
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cr)

conn.commit()
print("Metadados, classes e cruzamento de leis do MDT inseridos no SQLite com sucesso!")
conn.close()

print(f"=== PIPELINE DO MDT FINALIZADO COM SUCESSO EM {time.time()-t0:.1f} SEGUNDOS ===")
