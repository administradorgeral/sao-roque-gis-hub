import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
import json

print("=== PROCESSAMENTO DOS DISTRITOS E SETORES CENSITÁRIOS (CENSO 2022) ===")

kml_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/scratch_kml/doc.kml"
gdf = gpd.read_file(kml_path, engine="pyogrio")

# Garantir 2D
gdf["geometry"] = gdf["geometry"].apply(lambda geom: make_valid(geom))
print(f"Total de setores carregados: {len(gdf)}")

# 1. Exportar Setores Censitários
print("1. Gerando camada de Setores Censitários (188 setores)...")
setores_features = []
dist_colors = {
    "São Roque": "#2563EB",
    "Canguera": "#059669",
    "Mailasqui": "#D97706",
    "São João Novo": "#7C3AED"
}

for _, row in gdf.iterrows():
    dist = row.get("NM_DIST", "São Roque")
    sit = row.get("SITUACAO", "Urbana")
    cor = dist_colors.get(dist, "#3B82F6")
    area_km2 = float(row.get("AREA_KM2", 0.0))
    area_ha = round(area_km2 * 100.0, 2)
    
    setores_features.append({
        "type": "Feature",
        "properties": {
            "cd_setor": str(row["CD_SETOR"]),
            "distrito": dist,
            "situacao": sit,
            "area_km2": round(area_km2, 4),
            "area_ha": area_ha,
            "municipio": "São Roque (3550605)",
            "fonte": "IBGE - Censo Demográfico 2022",
            "cor_hex": cor
        },
        "geometry": json.loads(gpd.GeoSeries([row["geometry"]]).to_json())["features"][0]["geometry"]
    })

fc_setores = {
    "type": "FeatureCollection",
    "name": "setores_censitarios_sao_roque_cd2022",
    "features": setores_features
}

setores_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/setores_censitarios_sao_roque_web.geojson"
with open(setores_out, "w", encoding="utf-8") as f:
    json.dump(fc_setores, f, ensure_ascii=False)
print(f"  GeoJSON Setores salvo: {setores_out}")

# 2. Dissolver por Distrito
print("\n2. Dissolvendo setores por Distrito Oficial...")
distritos_data = []

# Área oficial municipal
mun_gdf = gpd.read_file("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/territorio_municipal_sao_roque.gpkg")
mun_area_ha = mun_gdf.geometry.iloc[0].area / 10000.0

# Converter setores para UTM para cálculo preciso de área
gdf_utm = gdf.to_crs(epsg=31983)

for dist, group in gdf_utm.groupby("NM_DIST"):
    poly_dist_utm = unary_union(group.geometry)
    area_ha = round(poly_dist_utm.area / 10000.0, 2)
    area_km2 = round(area_ha / 100.0, 2)
    pct = round((area_ha / mun_area_ha) * 100.0, 2)
    n_setores = len(group)
    n_urbanos = len(group[group["SITUACAO"] == "Urbana"])
    n_rurais = len(group[group["SITUACAO"] == "Rural"])
    
    # Reprojetar para WGS84 para WebGIS
    poly_wgs = gpd.GeoSeries([poly_dist_utm], crs="EPSG:31983").to_crs(epsg=4326).iloc[0]
    
    cor = dist_colors.get(dist, "#2563EB")
    
    distritos_data.append({
        "type": "Feature",
        "properties": {
            "distrito": dist,
            "nome": f"Distrito de {dist}",
            "codigo_distrito": str(group["CD_DIST"].iloc[0]),
            "municipio": "Estância Turística de São Roque",
            "codigo_ibge": "3550605",
            "total_setores": n_setores,
            "setores_urbanos": n_urbanos,
            "setores_rurais": n_rurais,
            "area_ha": area_ha,
            "area_km2": area_km2,
            "porcentagem_municipio": pct,
            "cor_hex": cor,
            "fonte": "IBGE Censo 2022 / Lei Orgânica Municipal nº 1.801/90"
        },
        "geometry": json.loads(gpd.GeoSeries([poly_wgs]).to_json())["features"][0]["geometry"]
    })

fc_distritos = {
    "type": "FeatureCollection",
    "name": "distritos_oficiais_sao_roque",
    "features": distritos_data
}

distritos_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/distritos_sao_roque_web.geojson"
with open(distritos_out, "w", encoding="utf-8") as f:
    json.dump(fc_distritos, f, ensure_ascii=False)
print(f"  GeoJSON Distritos salvo: {distritos_out}")

# Salvar também GPKG
gdf_dist_utm = gpd.GeoDataFrame([
    {**d["properties"], "geometry": unary_union(gdf_utm[gdf_utm["NM_DIST"] == d["properties"]["distrito"]].geometry)}
    for d in distritos_data
], crs="EPSG:31983")

gpkg_dist_out = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/distritos_sao_roque.gpkg"
gdf_dist_utm.to_file(gpkg_dist_out, driver="GPKG")
print(f"  GPKG Distritos salvo: {gpkg_dist_out}")

print("\n=== RESUMO DOS 4 DISTRITOS DE SÃO ROQUE ===")
for d in distritos_data:
    p = d["properties"]
    print(f"  > {p['nome']}: {p['area_ha']:,.2f} ha ({p['porcentagem_municipio']}%) | {p['total_setores']} setores ({p['setores_urbanos']} urb / {p['setores_rurais']} rur)")
