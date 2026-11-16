import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import numpy as np
import json
import os
import time
import sqlite3
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely import simplify
import geopandas as gpd

print("=== REGERANDO HIDROGRAFIA: PARSER COMPLETO DE SUBPATHS & DRAWMODE ESTRITO ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

# Parâmetros de calibração afim derivados diretamente das linhas de grade vetoriais cinzas (#6E6E6E)
# Grid X: 270.000 a 295.000 mE (Caminhos 4321 a 4336)
# Grid Y: 7.385.000 a 7.410.000 mN (Caminhos 4339 a 4354)
slope_x = 17.636158
intercept_x = 269093.76
slope_y = 17.638982
intercept_y = 7381212.50

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

def extract_polygons(geom):
    if geom.geom_type == 'Polygon':
        return geom
    elif geom.geom_type == 'MultiPolygon':
        return geom
    elif geom.geom_type == 'GeometryCollection':
        polys = []
        for g in geom.geoms:
            if g.geom_type == 'Polygon':
                polys.append(g)
            elif g.geom_type == 'MultiPolygon':
                polys.extend(g.geoms)
        if len(polys) == 1:
            return polys[0]
        elif len(polys) > 1:
            return MultiPolygon(polys)
    return None

r_val = ctypes.c_uint()
g_val = ctypes.c_uint()
b_val = ctypes.c_uint()
a_val = ctypes.c_uint()
x_val = ctypes.c_float()
y_val = ctypes.c_float()
fill_mode = ctypes.c_int()
stroke = ctypes.c_int()

all_records = []

for idx, p in enumerate(path_objs):
    b = p.get_bounds()
    # Filtrar elementos fora do mapa útil (moldura da Hidro é X <= 1697.12)
    if b[0] > 1697.0 or b[1] < 28.0 or b[3] > 1643.0:
        continue
    # Filtrar a própria moldura externa retangular
    if (b[2] - b[0]) > 1600 and (b[3] - b[1]) > 1550:
        continue
        
    pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fill_mode), ctypes.byref(stroke))
    fm = fill_mode.value
    st = stroke.value
    
    if pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
    else:
        f_hex = "NONE"
        
    if pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val)):
        s_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
    else:
        s_hex = "NONE"
        
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    if n_segs < 2:
        continue
        
    # Segmentar rigorosamente em subcaminhos separados respeitando FPDF_SEGMENT_MOVETO
    subpaths = []
    curr = []
    for i in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
        seg_type = pdfium_c.FPDFPathSegment_GetType(seg)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
        pt = pdf_to_utm(x_val.value, y_val.value)
        if seg_type == pdfium_c.FPDF_SEGMENT_MOVETO:
            if len(curr) >= 2:
                subpaths.append(curr)
            curr = [pt]
        else:
            curr.append(pt)
    if len(curr) >= 2:
        subpaths.append(curr)
        
    # 1. Represas, Lagos e Corpos d'Água Poligonais (fm in (1, 2) e f_hex == '#97DBF2')
    if fm in (1, 2) and f_hex == "#97DBF2":
        for sp in subpaths:
            if len(sp) >= 3:
                if sp[0] != sp[-1]:
                    sp.append(sp[0])
                if len(sp) >= 4:
                    try:
                        poly = Polygon(sp)
                        if not poly.is_valid:
                            poly = make_valid(poly)
                        clean_poly = extract_polygons(poly)
                        if clean_poly is not None and clean_poly.area >= 50.0: # >= 50 m²
                            all_records.append({
                                "codigo_classe": "HIDRO_REPRESA_LAGO",
                                "tipo": "Represa / Lago / Açude",
                                "classe": "Espelho d'Água / Reservatório",
                                "subtipo": "Corpo Hídrico Poligonal",
                                "cor_hex": "#00A2E8",
                                "fill_hex": "#00A2E8",
                                "area_m2": round(clean_poly.area, 1),
                                "area_ha": round(clean_poly.area / 10000.0, 3),
                                "extensao_m": 0.0,
                                "faixa_app": "30 a 100 metros (entorno de reservatório)",
                                "grau_restricao": "Impeditiva / APP de Reservatório",
                                "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, II e Lei nº 6.766/1979",
                                "implicacao": "Espelho d'água permanente ou reservatório de amortecimento/abastecimento. APP inalienável e non aedificandi.",
                                "alerta_juridico": "🚨 APP DE CORPO D'ÁGUA: Proibida a ocupação, aterramento ou parcelamento no entorno de represas e lagos (Lei Federal 12.651/12).",
                                "geometry": clean_poly
                            })
                    except Exception:
                        pass
                
    # 2. Cursos d'Água Lineares (st == 1, fm == 0 e cor azul/marinho)
    elif st == 1 and fm == 0 and s_hex in ("#0A93FC", "#4065EB"):
        is_main = (s_hex == "#4065EB")
        tipo_str = "Rio Principal / Calha de Drenagem" if is_main else "Córrego / Afluente / Drenagem Secundária"
        classe_str = "Rio Principal (Guaçu/Carambeí/Saboó)" if is_main else "Córrego / Drenagem Natural"
        cor = "#0055D4" if is_main else "#00B0FF"
        faixa = "30 a 50 metros" if is_main else "30 metros"
        for sp in subpaths:
            if len(sp) >= 2:
                try:
                    line = LineString(sp)
                    if line.length >= 15.0: # >= 15 metros
                        all_records.append({
                            "codigo_classe": "HIDRO_RIO_PRINCIPAL" if is_main else "HIDRO_CORREGO_SECUNDARIO",
                            "tipo": tipo_str,
                            "classe": classe_str,
                            "subtipo": "Curso d'Água Linear",
                            "cor_hex": cor,
                            "fill_hex": cor,
                            "area_m2": 0.0,
                            "area_ha": 0.0,
                            "extensao_m": round(line.length, 1),
                            "faixa_app": f"{faixa} de cada lado da calha",
                            "grau_restricao": "Impeditiva / Faixa Marginal de APP Hídrica",
                            "base_legal": "Lei Federal nº 12.651/2012 Art. 4º, I e Lei nº 6.766/1979 Art. 3º",
                            "implicacao": f"Calha natural de drenagem com faixa non aedificandi de {faixa} ao longo de ambas as margens.",
                            "alerta_juridico": f"💧 APP HÍDRICA ({faixa}): Faixa marginal de preservação permanente protegida pela Lei Federal 12.651/12 e Lei 6.766/79.",
                            "geometry": line
                        })
                except Exception:
                    pass

doc.close()
print(f"[{time.time()-t0:.1f}s] Feições totais extraídas com rigor absoluto: {len(all_records)}")

gdf = gpd.GeoDataFrame(all_records, crs="EPSG:31983")

# Salvar GeoPackage analítico oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\hidrografia_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="hidrografia_rede")
print(f"[{time.time()-t0:.1f}s] GeoPackage Hidrografia atualizado: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Simplificar para entrega WebGIS com Douglas-Peucker de 2.0m (mantendo curvas suaves)
gdf_web = gdf.copy()
gdf_web['geometry'] = simplify(gdf_web['geometry'].values, tolerance=2.0, preserve_topology=False)
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
    feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])
    p = feat['properties']
    tipo = p.get('tipo', '')
    classe = p.get('classe', '')
    ext_m = p.get('extensao_m', 0.0)
    area_ha = p.get('area_ha', 0.0)
    dim_str = f"{ext_m:.1f} metros de extensão" if ext_m > 0 else f"{area_ha:.2f} ha ({int(area_ha*10000):,} m²)"
    
    feat['properties'] = {
        "nome": f"{tipo}",
        "classe": classe,
        "Tipo de Feição": tipo,
        "Classificação Hídrica": p.get('subtipo', ''),
        "Dimensão / Extensão": dim_str,
        "Faixa de APP Legal": p.get('faixa_app', ''),
        "Grau de Restrição Construtiva": p.get('grau_restricao', ''),
        "Base Legal Normativa": p.get('base_legal', ''),
        "Diretriz Técnica e Ambiental": p.get('implicacao', ''),
        "Alerta de Auditoria Jurídica": p.get('alerta_juridico', ''),
        "Fonte Primária": "IGC 1:10.000 (1978) / SABESP (2017) / PDA 2019",
        "Responsabilidade Técnica": "Eng. Maurício S. Sartori (CREA 5.060.532.187) / Ana C. Cerminaro (CREA 473.423.455)",
        "cor_hex": p.get('cor_hex', '#00A2E8'),
        "cor": p.get('cor_hex', '#00A2E8')
    }
    clean_features.append(feat)

data_geojson['features'] = clean_features

geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\hidrografia_sao_roque_web.geojson"
with open(geojson_out, "w", encoding="utf-8") as f:
    json.dump(data_geojson, f, ensure_ascii=False)

print(f"[{time.time()-t0:.1f}s] GeoJSON Web atualizado: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB, {len(clean_features)} feições)")

# Obter bounding box real dos dados
total_bounds = gdf.total_bounds
bounds_wgs84 = gdf_wgs84.total_bounds
print(f"Bounding Box UTM 23S: [{total_bounds[0]:.2f}, {total_bounds[1]:.2f}, {total_bounds[2]:.2f}, {total_bounds[3]:.2f}]")
print(f"Bounding Box WGS84:   [{bounds_wgs84[1]:.5f}, {bounds_wgs84[0]:.5f}], [{bounds_wgs84[3]:.5f}, {bounds_wgs84[2]:.5f}]")

# Sincronizar banco de dados SQLite Oficial
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

wgs_json = json.dumps([[round(bounds_wgs84[1], 5), round(bounds_wgs84[0], 5)], [round(bounds_wgs84[3], 5), round(bounds_wgs84[2], 5)]])

c.execute("""
UPDATE camadas_territoriais SET
    bbox_utm_x0 = ?,
    bbox_utm_x1 = ?,
    bbox_utm_y0 = ?,
    bbox_utm_y1 = ?,
    bounds_wgs84_json = ?,
    status_auditoria = 'Auditado e Calibrado (Parser Rigoroso de Subpaths MOVETO e DrawMode Estrito)'
WHERE id = 'hidrografia'
""", (round(total_bounds[0], 2), round(total_bounds[2], 2), round(total_bounds[1], 2), round(total_bounds[3], 2), wgs_json))

conn.commit()
conn.close()

print(f"[{time.time()-t0:.1f}s] Banco de dados sao_roque_geodados.db sincronizado com sucesso!")
print("=== CALIBRAÇÃO E EXPORTAÇÃO CONCLUÍDAS COM SUCESSO! ===")
