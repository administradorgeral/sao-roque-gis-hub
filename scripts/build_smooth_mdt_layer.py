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

print("=== REGERANDO CAMADA MDT COM CALIBRAÇÃO AFIM RIGOROSA E RECORTE DE LEGENDA ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

scale = 3.5
pw = float(page.get_width()) # 2384.248779296875
ph = float(page.get_height()) # 1683.751220703125
pil_img = page.render(scale=scale).to_pil()
full_bgr = np.array(pil_img)[:, :, [2, 1, 0]]
H, W, _ = full_bgr.shape
print(f"[{time.time()-t0:.1f}s] Imagem contínua gerada: {W}x{H} pixels.")

# Parâmetros de calibração afim rigorosos para MDT (calibrados nos 7 ticks UTM do PDF)
slope_x = 17.640225
intercept_x = 270233.84
slope_y = 17.641051
intercept_y = 7381324.25

# Limites do Neatline do MDT em pontos: [31.4408, 35.9703, 1674.0437, 1620.6335]
# Em pixels (escala 3.5):
px_min = int(31.4408 * scale)
px_max = int(1674.0437 * scale)
py_min = int((ph - 1620.6335) * scale) # topo no espaço de imagem
py_max = int((ph - 35.9703) * scale)   # base no espaço de imagem

print(f"Área útil da moldura em pixels: X=[{px_min}, {px_max}], Y=[{py_min}, {py_max}]")

def px_to_utm(px, py):
    x_pt = px / scale
    y_pt = (H - py) / scale
    utm_x = slope_x * x_pt + intercept_x
    utm_y = slope_y * y_pt + intercept_y
    return (utm_x, utm_y)

classes_cfg = [
    {
        "codigo": "MDT_1_630_760",
        "classe": "630 a 760 m",
        "relevo": "Fundos de Vale / Planícies Aluviais",
        "cor_hex": "#006100",
        "lower_bgr": np.array([0, 80, 0]),
        "upper_bgr": np.array([20, 115, 20]),
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
        "lower_bgr": np.array([0, 150, 100]),
        "upper_bgr": np.array([25, 190, 140]),
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
        "lower_bgr": np.array([0, 235, 235]),
        "upper_bgr": np.array([30, 255, 255]),
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
        "lower_bgr": np.array([0, 130, 235]),
        "upper_bgr": np.array([30, 175, 255]),
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
        "lower_bgr": np.array([0, 15, 235]),
        "upper_bgr": np.array([25, 50, 255]),
        "restricao": "Impeditiva / APP de Topo de Morro",
        "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, IX, STF ADPF 747/749",
        "implicacao": "Ponto culminante de São Roque. Área de Preservação Permanente (APP) de topo de morro e cristas inalienável e não edificável.",
        "alerta": "🚨 TOPO DE MORRO E CRISTAS (APP): O STF (ADPF 747/749) e o Código Florestal vedam ocupações e loteamentos comerciais em topos de morro e cristas."
    }
]

all_records = []
k_morph = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

for c_cfg in classes_cfg:
    mask = cv2.inRange(full_bgr, c_cfg['lower_bgr'], c_cfg['upper_bgr'])
    
    # 1. RECORTAR ESTREITAMENTE À MOLDURA ÚTIL (ELIMINANDO OS RETÂNGULOS DA LEGENDA)
    # Qualquer pixel fora de [px_min, px_max] e [py_min, py_max] é ZERADO
    mask[:, :px_min] = 0
    mask[:, px_max:] = 0
    mask[:py_min, :] = 0
    mask[py_max:, :] = 0
    
    # 2. Suavização anti-persiana contínua
    m_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_morph)
    m_smooth = cv2.medianBlur(m_clean, 5)
    
    contours, hierarchy = cv2.findContours(m_smooth, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    
    cls_added = 0
    if hierarchy is not None:
        hier = hierarchy[0]
        for idx, (cnt, h_info) in enumerate(zip(contours, hier)):
            if h_info[3] == -1: # Contorno externo
                if len(cnt) < 3 or cv2.contourArea(cnt) < 50:
                    continue
                
                ext_pts = [px_to_utm(pt[0][0], pt[0][1]) for pt in cnt]
                if ext_pts[0] != ext_pts[-1]:
                    ext_pts.append(ext_pts[0])
                    
                holes = []
                child_idx = h_info[2]
                while child_idx != -1:
                    child_cnt = contours[child_idx]
                    if len(child_cnt) >= 3 and cv2.contourArea(child_cnt) >= 50:
                        hole_pts = [px_to_utm(pt[0][0], pt[0][1]) for pt in child_cnt]
                        if hole_pts[0] != hole_pts[-1]:
                            hole_pts.append(hole_pts[0])
                        holes.append(hole_pts)
                    child_idx = hier[child_idx][0]
                    
                try:
                    p = Polygon(shell=ext_pts, holes=holes if holes else None)
                    if not p.is_valid:
                        p = make_valid(p)
                    
                    polys_to_add = []
                    if p.geom_type == 'Polygon':
                        polys_to_add.append(p)
                    elif p.geom_type == 'MultiPolygon':
                        polys_to_add.extend(p.geoms)
                    elif p.geom_type == 'GeometryCollection':
                        for g in p.geoms:
                            if g.geom_type in ('Polygon', 'MultiPolygon'):
                                if g.geom_type == 'Polygon':
                                    polys_to_add.append(g)
                                else:
                                    polys_to_add.extend(g.geoms)
                                    
                    for poly in polys_to_add:
                        if poly.area >= 1000.0: # >= 1000 m² (0.1 ha)
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
                                "area_ha": round(poly.area / 10000.0, 3),
                                "geometry": poly
                            })
                            cls_added += 1
                except Exception:
                    pass
    print(f"[{time.time()-t0:.1f}s] Classe {c_cfg['classe']:10s}: {cls_added} manchas válidas.")

doc.close()
print(f"[{time.time()-t0:.1f}s] Total de manchas consolidadas: {len(all_records)}")

gdf = gpd.GeoDataFrame(all_records, crs="EPSG:31983")

# Salvar GeoPackage analítico oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="mdt_classes")
print(f"[{time.time()-t0:.1f}s] GeoPackage MDT atualizado: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Simplificar para WebGIS com tolerância Douglas-Peucker de 4.0m
gdf_web = gdf.copy()
gdf_web['geometry'] = simplify(gdf_web['geometry'].values, tolerance=4.0, preserve_topology=False)
gdf_wgs84 = gdf_web.to_crs("EPSG:4326")

data_geojson = json.loads(gdf_wgs84.to_json())

def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

clean_features = []
for feat in data_geojson['features']:
    if not feat.get('geometry') or 'coordinates' not in feat['geometry']:
        continue
    if feat['geometry']['type'] not in ('Polygon', 'MultiPolygon'):
        continue
    feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])
    p = feat['properties']
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
    clean_features.append(feat)

data_geojson['features'] = clean_features

geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson"
with open(geojson_out, "w", encoding="utf-8") as f:
    json.dump(data_geojson, f, ensure_ascii=False)

print(f"[{time.time()-t0:.1f}s] GeoJSON Web atualizado: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB, {len(clean_features)} feições)")
