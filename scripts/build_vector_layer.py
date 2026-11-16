import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import time
import os
import json
from shapely.geometry import Polygon, MultiPolygon, mapping
from shapely import make_valid, simplify, unary_union
import geopandas as gpd
import pandas as pd

print("=== INICIANDO GERAÇÃO DA CAMADA VETORIAL NATIVA DE DECLIVIDADE ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]
print(f"[{time.time()-t0:.1f}s] Total de paths lidos: {len(path_objs)}")

classes_meta = {
    "#FFFF73": {
        "codigo": "CL_1_PLANO",
        "classe": "Plano (0 a 3%)",
        "cor_hex": "#FFFF73",
        "relevo": "Plano",
        "angulo": "0° a 1.7°",
        "restricao": "Livre",
        "base_legal": "Lei Federal 6.766/79 e LC Municipal 40/2006",
        "implicacao": "Apto para edificação e loteamento regular sem restrições topográficas."
    },
    "#FFFF00": {
        "codigo": "CL_2_SUAVE",
        "classe": "Suave ondulado (3 a 8%)",
        "cor_hex": "#FFFF00",
        "relevo": "Suave Ondulado",
        "angulo": "1.7° a 4.6°",
        "restricao": "Baixa",
        "base_legal": "LC Municipal 40/2006 Art. 32",
        "implicacao": "Apto para vias públicas e equipamentos comunitários. Controle padrão de escoamento superficial."
    },
    "#FFAA00": {
        "codigo": "CL_3_ONDULADO",
        "classe": "Ondulado (8 a 20%)",
        "cor_hex": "#FFAA00",
        "relevo": "Ondulado",
        "angulo": "4.6° a 11.3°",
        "restricao": "Média",
        "base_legal": "LC 40/2006 Art. 32 (vias com limite > 15% requerem projeto especial)",
        "implicacao": "Exige obras de terraplenagem contida e drenagem. Rampa viária máxima regular em São Roque é 15%."
    },
    "#FF5500": {
        "codigo": "CL_4_FORTE_ONDULADO",
        "classe": "Forte ondulado (20 a 45%)",
        "cor_hex": "#FF5500",
        "relevo": "Forte Ondulado",
        "angulo": "11.3° a 24.2°",
        "restricao": "Severa / Impeditiva acima de 30%",
        "base_legal": "Lei Federal 6.766/79 Art. 3º e LC Municipal 40/2006 Art. 13 e 43",
        "implicacao": "CRÍTICO: No trecho entre 30% e 45%, a legislação municipal e federal PROÍBE parcelamento do solo e condomínios."
    },
    "#E60000": {
        "codigo": "CL_5_MONTANHOSO",
        "classe": "Montanhoso (45 a 75%)",
        "cor_hex": "#E60000",
        "relevo": "Montanhoso",
        "angulo": "24.2° a 36.9° (ou > 45° / 100%)",
        "restricao": "Impeditiva / Risco Geotécnico",
        "base_legal": "Lei Federal 12.651/2012 Art. 4º, V e Lei 12.608/2012",
        "implicacao": "Risco gravíssimo de escorregamento. As encostas com rampa > 100% (> 45°) constituem APP inalienável."
    }
}

r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
x = ctypes.c_float()
y = ctypes.c_float()

scale_x = 17.636684
scale_y = 17.639795
x0_pt = 31.4408
y0_pt = 35.9703
utm_x0 = 270308.48
utm_y0 = 7382234.44

class_polys = {c: [] for c in classes_meta}

for p in path_objs:
    b_box = p.get_bounds()
    if b_box[0] < 30 or b_box[2] > 1675 or b_box[1] < 35 or b_box[3] > 1622:
        continue

    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    hex_col = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    
    if hex_col not in classes_meta:
        continue
        
    n_seg = pdfium_c.FPDFPath_CountSegments(p.raw)
    current_ring = []
    rings = []
    
    for s in range(n_seg):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, s)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x), ctypes.byref(y))
        seg_type = pdfium_c.FPDFPathSegment_GetType(seg)
        is_close = pdfium_c.FPDFPathSegment_GetClose(seg)
        
        utm_x = utm_x0 + (x.value - x0_pt) * scale_x
        utm_y = utm_y0 + (y.value - y0_pt) * scale_y
        
        if seg_type == 2:
            if len(current_ring) >= 3:
                rings.append(current_ring)
            current_ring = [(utm_x, utm_y)]
        else:
            current_ring.append((utm_x, utm_y))
            if is_close and len(current_ring) >= 3:
                rings.append(current_ring)
                current_ring = []
                
    if len(current_ring) >= 3:
        rings.append(current_ring)
        
    for ring in rings:
        if ring[0] != ring[-1]:
            ring.append(ring[0])
        try:
            poly = Polygon(ring)
            if poly.is_valid and poly.area > 50.0:
                class_polys[hex_col].append(poly)
            elif not poly.is_valid:
                fixed = make_valid(poly)
                if fixed.is_valid and fixed.area > 50.0:
                    class_polys[hex_col].append(fixed)
        except Exception:
            pass

doc.close()
print(f"[{time.time()-t0:.1f}s] Polígonos extraídos do PDF. Iniciando união e simplificação por classe...")

records = []
for hex_col, meta in classes_meta.items():
    t_c = time.time()
    raw_list = class_polys[hex_col]
    print(f"Processando classe '{meta['classe']}' ({len(raw_list)} polígonos)...")
    
    # União em blocos para velocidade e robustez
    # Simplificação de 1.5 metros (1:50.000)
    simplified_list = [simplify(p, tolerance=1.5, preserve_topology=True) for p in raw_list]
    merged = unary_union(simplified_list)
    
    if not merged.is_valid:
        merged = make_valid(merged)
        
    area_ha = merged.area / 10000.0
    print(f"  União concluída em {time.time()-t_c:.1f}s | Área: {area_ha:.2f} ha")
    
    # Separar polígonos individuais para melhor inspeção no WebGIS
    if merged.geom_type == 'MultiPolygon':
        geoms = list(merged.geoms)
    elif merged.geom_type == 'Polygon':
        geoms = [merged]
    else:
        geoms = [g for g in getattr(merged, 'geoms', []) if g.geom_type in ['Polygon', 'MultiPolygon']]
        
    # Filtrar polígonos muito insignificantes gerados por artefatos de fatiamento
    for g in geoms:
        if g.area >= 100.0: # >= 100 m²
            records.append({
                "codigo_classe": meta["codigo"],
                "classe": meta["classe"],
                "relevo": meta["relevo"],
                "angulo_equivalente": meta["angulo"],
                "cor_hex": meta["cor_hex"],
                "grau_restricao": meta["restricao"],
                "base_legal": meta["base_legal"],
                "implicacao": meta["implicacao"],
                "area_ha": round(g.area / 10000.0, 3),
                "geometry": g
            })

print(f"[{time.time()-t0:.1f}s] Total de feições vetoriais consolidadas: {len(records)}")

# Criar GeoDataFrame no CRS oficial SIRGAS 2000 UTM 23S (EPSG: 31983)
gdf = gpd.GeoDataFrame(records, crs="EPSG:31983")

# Salvar GeoPackage oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="declividade_classes")
print(f"GeoPackage salvo com sucesso em: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Reprojetar para WGS84 (EPSG: 4326) para o Leaflet / WebGIS
gdf_wgs84 = gdf.to_crs("EPSG:4326")

# Arredondar coordenadas para 5 casas decimais (~1m precisão) para deixar GeoJSON leve
geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque.geojson"
gdf_wgs84.to_file(geojson_out, driver="GeoJSON")
print(f"GeoJSON salvo com sucesso em: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB)")

print(f"=== PROCESSO COMPLETO EM {time.time()-t0:.1f} SEGUNDOS ===")
