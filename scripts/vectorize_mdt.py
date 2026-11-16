import pypdfium2 as pdfium
import numpy as np
import cv2
import time
from shapely.geometry import Polygon, MultiPolygon
from shapely import simplify, make_valid
import geopandas as gpd

print("Iniciando montagem da imagem de 300 DPI e extração vetorial dos contornos...")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

strip_bitmaps = []
for i in range(len(images)):
    bm = images[i].get_bitmap()
    arr = bm.to_numpy()
    strip_bitmaps.append(arr[:, :, :3]) # BGR

full_bgr = np.vstack(strip_bitmaps)
H, W, _ = full_bgr.shape
print(f"[{time.time()-t0:.1f}s] Imagem composta montada: {W}x{H} pixels (300 DPI).")

# Cores exatas do MDT em BGR:
# 1. 630-760m:   #006100 -> BGR (0, 97, 0)
# 2. 760-830m:   #7AAB00 -> BGR (0, 171, 122)
# 3. 830-900m:   #FFFF00 -> BGR (0, 255, 255)
# 4. 900-970m:   #FF9900 -> BGR (0, 153, 255)
# 5. 970-1125m:  #FF2200 -> BGR (0, 34, 255)

classes_cfg = [
    {
        "codigo": "MDT_1_630_760",
        "classe": "630 a 760 m",
        "relevo": "Fundos de Vale / Planícies Aluviais",
        "cor_hex": "#006100",
        "lower_bgr": np.array([0, 85, 0]),
        "upper_bgr": np.array([15, 110, 15]),
        "restricao": "Condicionante / Faixa de APP Hídrica",
        "base_legal": "Lei Federal 12.651/2012 Art. 4º, I e Lei 6.766/79 Art. 3º, I",
        "implicacao": "Várzeas e planícies de amortecimento de cheias dos Rios Guaçu e Carambeí. Faixas marginais de APP hídrica inalienáveis."
    },
    {
        "codigo": "MDT_2_760_830",
        "classe": "760 a 830 m",
        "relevo": "Terraço Intermediário / Encostas Baixas",
        "cor_hex": "#7AAB00",
        "lower_bgr": np.array([0, 160, 110]),
        "upper_bgr": np.array([15, 185, 135]),
        "restricao": "Urbana Consolidada / Controle de Drenagem",
        "base_legal": "LC Municipal 39/2006 e LC 40/2006",
        "implicacao": "Cota da malha urbana central e bairros consolidados. Exige conexão à infraestrutura sanitária e controle de drenagem superficial."
    },
    {
        "codigo": "MDT_3_830_900",
        "classe": "830 a 900 m",
        "relevo": "Planalto de Transição e Expansão",
        "cor_hex": "#FFFF00",
        "lower_bgr": np.array([0, 245, 245]),
        "upper_bgr": np.array([20, 255, 255]),
        "restricao": "Média / Amortecimento de Bacias",
        "base_legal": "LC 40/2006 e Lei Estadual 9.866/1997",
        "implicacao": "Platôs e divisores de sub-bacias com expansão de baixa densidade. Proteção das cabeceiras da APA Itupararanga."
    },
    {
        "codigo": "MDT_4_900_970",
        "classe": "900 a 970 m",
        "relevo": "Altas Vertentes Serranas",
        "cor_hex": "#FF9900",
        "lower_bgr": np.array([0, 140, 245]),
        "upper_bgr": np.array([15, 165, 255]),
        "restricao": "Severa / Prevenção Geotécnica",
        "base_legal": "Lei Federal 12.608/2012 e Lei Federal 11.428/2006",
        "implicacao": "Altas encostas da Serra de São Roque e Morro do Saboó. Área de preservação de Mata Atlântica e alto risco erosivo."
    },
    {
        "codigo": "MDT_5_970_1125",
        "classe": "970 a 1.125 m",
        "relevo": "Cristas, Picos e Morro do Saboó",
        "cor_hex": "#FF2200",
        "lower_bgr": np.array([0, 25, 245]),
        "upper_bgr": np.array([15, 45, 255]),
        "restricao": "Impeditiva / APP de Topo de Morro",
        "base_legal": "Lei Federal 12.651/2012 Art. 4º, IX, STF ADPF 747/749",
        "implicacao": "Ponto culminante de São Roque. Área de Preservação Permanente (APP) de topo de morro e cristas inalienável e não edificável."
    }
]

# Geometria do frame em pontos e coordenadas UTM
# x_pt = 32.40084 + px * 0.24000625
# y_pt = 1619.67346 - py * (1582.98312 / H)
# Em UTM:
# utm_x = 270308.48 + (x_pt - 31.4408) * 17.636684
# utm_y = 7382234.44 + (y_pt - 35.9703) * 17.639795

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

all_features = []

for c_cfg in classes_cfg:
    t_c = time.time()
    print(f"Processando classe '{c_cfg['classe']}' ({c_cfg['relevo']})...")
    mask = cv2.inRange(full_bgr, c_cfg['lower_bgr'], c_cfg['upper_bgr'])
    
    # Encontrar contornos com hierarquia para incluir buracos (islands)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    print(f"  Contornos brutos: {len(contours)} em {time.time()-t_c:.2f}s")
    
    # Processar contornos externos
    valid_polys = []
    if hierarchy is not None:
        hier = hierarchy[0]
        for idx, (cnt, h_info) in enumerate(zip(contours, hier)):
            # h_info: [next, prev, child, parent]
            # Se parent == -1, é contorno externo
            if h_info[3] == -1:
                if len(cnt) < 3 or cv2.contourArea(cnt) < 50: # filtrar ruídos < 50 px (~900 m²)
                    continue
                
                # Vértices externos
                ext_pts = [px_to_utm(pt[0][0], pt[0][1]) for pt in cnt]
                if ext_pts[0] != ext_pts[-1]:
                    ext_pts.append(ext_pts[0])
                    
                # Buracos internos (filhos)
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
                    if p.area >= 1000.0: # >= 0.1 ha
                        valid_polys.append(p)
                except Exception:
                    pass
                    
    print(f"  Polígonos válidos consolidados: {len(valid_polys)}")
    for p in valid_polys:
        all_features.append({
            "codigo_classe": c_cfg["codigo"],
            "classe": c_cfg["classe"],
            "relevo": c_cfg["relevo"],
            "cor_hex": c_cfg["cor_hex"],
            "cor": c_cfg["cor_hex"],
            "grau_restricao": c_cfg["restricao"],
            "base_legal": c_cfg["base_legal"],
            "implicacao": c_cfg["implicacao"],
            "area_ha": round(p.area / 10000.0, 3),
            "geometry": p
        })

print(f"[{time.time()-t0:.1f}s] Total de feições vetoriais do MDT: {len(all_features)}")

doc.close()
