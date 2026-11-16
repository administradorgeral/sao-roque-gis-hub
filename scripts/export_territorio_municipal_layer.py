import zipfile
import json
import os
import time
import geopandas as gpd
from shapely.ops import unary_union
from shapely import force_2d

print("=== EXTRAÇÃO DO CONTORNO MUNICIPAL CONTÍNUO (IBGE 2022 / CD2022) ===")
t0 = time.time()

kmz_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/sao_roque_3550605_setores_CD2022.kmz"
temp_kml = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/temp_setores.kml"

with zipfile.ZipFile(kmz_path, 'r') as z:
    with open(temp_kml, 'wb') as f:
        f.write(z.read('doc.kml'))

print("1. KML extraído com sucesso. Lendo setores censitários...")
gdf_setores = gpd.read_file(temp_kml, engine="pyogrio")
print(f"Total de setores lidos: {len(gdf_setores)}")

print("2. Executando união espacial contínua (unary_union)...")
dissolved_geom = unary_union(gdf_setores.geometry)
dissolved_geom = force_2d(dissolved_geom)

# Criar GeoDataFrame em EPSG:4326
gdf_mun_wgs84 = gpd.GeoDataFrame([{'id': 1}], geometry=[dissolved_geom], crs="EPSG:4326")

# Projetar para UTM 23S para cálculos de área periciais
gdf_mun_utm = gdf_mun_wgs84.to_crs(epsg=31983)
poly_utm = gdf_mun_utm.geometry.iloc[0]

area_m2 = poly_utm.area
area_ha = round(area_m2 / 10000.0, 2)
area_km2 = round(area_ha / 100.0, 2)
perimetro_km = round(poly_utm.length / 1000.0, 2)

bounds_utm = poly_utm.bounds
bbox_utm_x0, bbox_utm_y0, bbox_utm_x1, bbox_utm_y1 = [round(b, 2) for b in bounds_utm]

bounds_wgs84 = gdf_mun_wgs84.geometry.iloc[0].bounds
minx, miny, maxx, maxy = bounds_wgs84
bounds_wgs84_json = f"[[{miny:.5f}, {minx:.5f}], [{maxy:.5f}, {maxx:.5f}]]"

print(f"Área Calculada: {area_ha} ha ({area_km2} km²)")
print(f"Perímetro Municipal: {perimetro_km} km")
print(f"BBox UTM 23S: [{bbox_utm_x0}, {bbox_utm_y0}, {bbox_utm_x1}, {bbox_utm_y1}]")

# Propriedades periciais de governança e Estância Turística
properties = {
    "codigo_classe": "TERRITORIO_MUNICIPAL",
    "codigo": "TERRITORIO_MUNICIPAL",
    "nome": "Município da Estância Turística de São Roque",
    "denominacao": "Território Municipal Oficial e Regime de Estância Turística",
    "codigo_ibge": "3550605",
    "regiao_metropolitana": "Região Metropolitana de Sorocaba (RMS) / Aglomeração Urbana de São Paulo",
    "regime_juridico": "Estância Turística do Estado de São Paulo",
    "lei_criacao_estancia": "Lei Estadual nº 6.899/1990",
    "fundamento_constitucional": "Constituição Estadual de 1989 (Art. 146 - DADETUR/FUMEST e Art. 180 - Política Urbana)",
    "lei_matriz_estancias": "Lei Complementar Estadual nº 1.261/2015 (PDTur, COMTUR, Ranqueamento Trienal)",
    "lei_organica": "Lei Orgânica do Município de São Roque (Lei nº 1.801/1990)",
    "plano_diretor_geral": "Lei Complementar Municipal nº 39/2006 (Plano Diretor Estratégico)",
    "plano_diretor_turismo": "Lei Complementar Municipal nº 140/2025 (Revisão Trienal do PDTur)",
    "conselho_turismo": "Lei Municipal nº 2.871/2004 (COMTUR Consultivo e Deliberativo)",
    "guia_turismo_obrigatorio": "Lei Municipal nº 4.872/2018 (Presença obrigatória de Guia Cadastur)",
    "area_ha": area_ha,
    "area_km2": area_km2,
    "perimetro_km": perimetro_km,
    "cor_hex": "#D4AF37",
    "cor_borda": "#1E293B",
    "fonte_cartografica": "IBGE - Censo Demográfico 2022 (Malha Setorial Contínua Dissolvida) / Cód. 3550605",
    "sistema_referencia": "SIRGAS 2000 UTM Zone 23S (EPSG:31983) / WGS84 (EPSG:4326)",
    "implicacao_pratica": "Território integral indivisível da Estância Turística. Base de incidência do Plano Diretor Estratégico (LC 39/06), repasses do Fundo de Melhoria das Estâncias (DADETUR), deliberações do COMTUR e instrumentos de governança tributária e urbana."
}

# Salvar GeoPackage oficial
gdf_out_utm = gpd.GeoDataFrame([properties], geometry=[poly_utm], crs="EPSG:31983")
gpkg_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg"
gdf_out_utm.to_file(gpkg_path, driver="GPKG")
print(f"Salvo GPKG em: {gpkg_path}")

# Salvar GeoJSON Web Otimizado
gdf_out_wgs84 = gpd.GeoDataFrame([properties], geometry=[gdf_mun_wgs84.geometry.iloc[0]], crs="EPSG:4326")
geojson_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque_web.geojson"

# Formatar GeoJSON com coordenadas arredondadas para 5 decimais (~1m)
geojson_dict = json.loads(gdf_out_wgs84.to_json())
def round_coords(geom):
    if geom['type'] == 'Polygon':
        geom['coordinates'] = [[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in geom['coordinates']]
    elif geom['type'] == 'MultiPolygon':
        geom['coordinates'] = [[[[round(coord[0], 5), round(coord[1], 5)] for coord in ring] for ring in poly] for poly in geom['coordinates']]

for f in geojson_dict['features']:
    round_coords(f['geometry'])

with open(geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_dict, f, ensure_ascii=False, indent=2)

print(f"Salvo GeoJSON Web em: {geojson_path} ({os.path.getsize(geojson_path)/1024:.1f} KB)")

# Limpar arquivo temporário
if os.path.exists(temp_kml):
    os.remove(temp_kml)

print(f"=== EXTRAÇÃO CONCLUÍDA EM {time.time()-t0:.2f}s ===")
