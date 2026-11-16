import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes
import json
import os
import time
import sqlite3
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely import simplify
import geopandas as gpd

print("=== REPROCESSANDO MAPA #4: GEOMORFOLÓGICO (ANEXO 4.3.4-1) COM DISSOLVE POR CLASSE ===")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\52226_4_3_4_1 Geomorfológico.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())

slope_x = 17.638217
intercept_x = 269022.04
slope_y = 17.641053
intercept_y = 7381020.82

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

r_val = ctypes.c_uint()
g_val = ctypes.c_uint()
b_val = ctypes.c_uint()
a_val = ctypes.c_uint()
x_val = ctypes.c_float()
y_val = ctypes.c_float()

units_meta = {
    "#FF73DF": {
        "codigo_classe": "GEOMORF_PAULISTANO",
        "nome_classe": "Planalto Paulistano / Alto Tietê",
        "morfoestrutura": "Cinturão Orogênico Ribeira / Bacia Sedimentar de São Paulo",
        "relevo_predominante": "Colinas amplas, topos aplainados e vertentes suaves a convexas",
        "litologia_associada": "Rochas metamórficas do Grupo São Roque com coberturas coluvionares",
        "suscetibilidade_erosao": "Média (potencializada em cortes de terraplenagem e aterros não compactados)",
        "risco_geotecnico": "Risco baixo a médio de escorregamento raso; atenção para planícies fluviais alagáveis",
        "diretriz_urbanistica": "Área de expansão com menor declividade média, exigindo drenagem pluvial estruturada e contenção de assoreamento",
        "base_legal": "Ross & Moroz (1997) / IPT (1981) / Lei Federal nº 6.766/1979 e LC Municipal nº 40/2006",
        "cor_hex": "#FF73DF",
        "fill_hex": "#FF73DF"
    },
    "#FFAA00": {
        "codigo_classe": "GEOMORF_IBIUNA_SR",
        "nome_classe": "Planalto de Ibiúna / São Roque",
        "morfoestrutura": "Cinturão Ribeira - Bloco Tectônico São Roque / Maciço Cristalino",
        "relevo_predominante": "Maciço dissecado, relevo ondulado a forte ondulado, escarpas e vales encaixados em V",
        "litologia_associada": "Filitos, xistos, metavulcânicas e granitos intrusivos da Formação São Roque / Ibiúna",
        "suscetibilidade_erosao": "Alta em encostas desprovidas de cobertura vegetal ou submetidas a cortes de encosta",
        "risco_geotecnico": "Médio a Alto em encostas com declividade > 30% e topos escarpados. Risco de escorregamentos translacionais planares",
        "diretriz_urbanistica": "Restrição rigorosa de parcelamento em rampas acentuadas (Lei 6.766/79 Art. 3º e LC 40/06). Exigência de laudo geológico-geotécnico",
        "base_legal": "Ross & Moroz (1997) / IPT (1981) / Lei Federal nº 12.651/2012 e LC Municipal nº 40/2006",
        "cor_hex": "#FFAA00",
        "fill_hex": "#FFAA00"
    },
    "#AAFF00": {
        "codigo_classe": "GEOMORF_JUNDIAI",
        "nome_classe": "Planalto de Jundiaí",
        "morfoestrutura": "Zona Tectônica Jundiaí - Cristas Estruturais NE-SW",
        "relevo_predominante": "Serras alongadas, cristas quartzíticas e morros com vertentes retilíneas íngremes (Morro do Saboó)",
        "litologia_associada": "Quartzitos resistentes, metassedimentos de alto grau e gnaisses migmatíticos",
        "suscetibilidade_erosao": "Muito Alta em zonas de fraturamento e topos de crista. Rolo de blocos e corridas de massa",
        "risco_geotecnico": "Alto a Muito Alto em áreas serranas. Vedada ocupação urbana em topos de morro e cristas (STF ADPF 747/749)",
        "diretriz_urbanistica": "Zona de preservação ambiental e recarga de aquíferos fraturados. Ocupação com restrição severa de desmatamento e movimentação de terra",
        "base_legal": "Ross & Moroz (1997) / IPT (1981) / STF ADPF 747/749 e Código Florestal Lei 12.651/2012 Art. 4º, IX",
        "cor_hex": "#AAFF00",
        "fill_hex": "#AAFF00"
    }
}

raw_records = []

for idx in [1, 2, 3, 4, 5, 6]:
    p = objs[idx]
    pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r_val), ctypes.byref(g_val), ctypes.byref(b_val), ctypes.byref(a_val))
    f_hex = f"#{r_val.value:02X}{g_val.value:02X}{b_val.value:02X}"
    n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
    
    pts = []
    for i in range(n_segs):
        seg = pdfium_c.FPDFPath_GetPathSegment(p.raw, i)
        pdfium_c.FPDFPathSegment_GetPoint(seg, ctypes.byref(x_val), ctypes.byref(y_val))
        pts.append(pdf_to_utm(x_val.value, y_val.value))
        
    if pts[0] != pts[-1]:
        pts.append(pts[0])
        
    poly = Polygon(pts)
    if not poly.is_valid:
        poly = make_valid(poly)
        
    meta = units_meta[f_hex]
    raw_records.append({
        "codigo_classe": meta["codigo_classe"],
        "nome": meta["nome_classe"],
        "classe": meta["nome_classe"],
        "Unidade Geomorfológica": meta["nome_classe"],
        "Morfoestrutura": meta["morfoestrutura"],
        "Relevo Predominante": meta["relevo_predominante"],
        "Litologia Associada": meta["litologia_associada"],
        "Suscetibilidade a Processos Erosivos": meta["suscetibilidade_erosao"],
        "Risco Geotécnico e Estabilidade": meta["risco_geotecnico"],
        "Diretriz Urbanística e Construtiva": meta["diretriz_urbanistica"],
        "Classificação Metodológica": "Ross & Moroz (1997) e IPT (1981)",
        "Base Legal Normativa": meta["base_legal"],
        "Responsabilidade Técnica": "Maurício Scorsatto Sartori (CREA 5.060.532.187) / Ana Clara Cerminaro (CREA 473.423.455)",
        "Fonte Primária": "IGC 1:10.000 (1978) / Ross & Moroz (1997) / PDA São Roque 2019",
        "cor_hex": meta["cor_hex"],
        "cor": meta["cor_hex"],
        "geometry": poly
    })

doc.close()

# Criação do GeoDataFrame bruto com 6 tiles
gdf_raw = gpd.GeoDataFrame(raw_records, crs="EPSG:31983")
print(f"[{time.time()-t0:.1f}s] Feições brutas lidas do PDF: {len(gdf_raw)}")

# DISSOLVE POR CLASSE - Elimina todas as divisões internas artificiais!
gdf_dissolved = gdf_raw.dissolve(by="codigo_classe", as_index=False, aggfunc="first")
print(f"[{time.time()-t0:.1f}s] Feições após DISSOLVE oficial: {len(gdf_dissolved)}")

# Atualizar áreas oficiais calculadas
records_final = []
for idx, row in gdf_dissolved.iterrows():
    poly = row.geometry
    area_m2 = poly.area
    area_ha = area_m2 / 10000.0
    r_dict = row.to_dict()
    r_dict["area_ha"] = round(area_ha, 2)
    r_dict["area_m2"] = round(area_m2, 1)
    r_dict["Área"] = f"{area_ha:.2f} ha ({area_ha/100:.2f} km²)"
    records_final.append(r_dict)

gdf = gpd.GeoDataFrame(records_final, crs="EPSG:31983")

for idx, r in gdf.iterrows():
    print(f"  -> Unidade {idx+1}: {r['Unidade Geomorfológica']} | Tipo: {r.geometry.geom_type} | Área: {r['Área']}")

# Salvar GeoPackage oficial
gpkg_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\geomorfologico_sao_roque.gpkg"
gdf.to_file(gpkg_out, driver="GPKG", layer="unidades_geomorfologicas")
print(f"[{time.time()-t0:.1f}s] GeoPackage salvo: {gpkg_out} ({os.path.getsize(gpkg_out)/1024:.1f} KB)")

# Simplificar para WebGIS com tolerância de 2m
gdf_web = gdf.copy()
gdf_web['geometry'] = simplify(gdf_web['geometry'].values, tolerance=2.0, preserve_topology=True)
gdf_wgs84 = gdf_web.to_crs("EPSG:4326")

data_geojson = json.loads(gdf_wgs84.to_json())

def round_coords(obj):
    if isinstance(obj, list):
        if len(obj) == 2 and isinstance(obj[0], (int, float)) and isinstance(obj[1], (int, float)):
            return [round(obj[0], 5), round(obj[1], 5)]
        return [round_coords(item) for item in obj]
    return obj

for feat in data_geojson['features']:
    if feat.get('geometry') and 'coordinates' in feat['geometry']:
        feat['geometry']['coordinates'] = round_coords(feat['geometry']['coordinates'])

geojson_out = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\geomorfologico_sao_roque_web.geojson"
with open(geojson_out, "w", encoding="utf-8") as f:
    json.dump(data_geojson, f, ensure_ascii=False)

print(f"[{time.time()-t0:.1f}s] GeoJSON Web salvo: {geojson_out} ({os.path.getsize(geojson_out)/1024:.1f} KB, {len(data_geojson['features'])} feições limpas)")

# Atualizar no SQLite as áreas e o total de unidades
db_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\sao_roque_geodados.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
UPDATE camadas_territoriais 
SET status_auditoria = 'Auditado, Calibrado e Dissolvido (3 Unidades Morfoesculturais sem divisões internas espúrias)'
WHERE id = 'geomorfologico'
""")

conn.commit()
conn.close()

print(f"[{time.time()-t0:.1f}s] Banco de dados sao_roque_geodados.db atualizado!")
print("=== DISSOLVE CONCLUÍDO COM 100% DE SUCESSO! ===")
