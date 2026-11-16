import json
import math
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import transform
from pyproj import Transformer

transformer_wgs_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:31983", always_xy=True)
transformer_utm_to_wgs = Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

# 1. Carregar camada existente (Catarina)
with open('data/zona_protecao_aeroportuaria_catarina_web.geojson', 'r', encoding='utf-8') as f:
    catarina_data = json.load(f)

# Carregar território de São Roque
gdf_mun = gpd.read_file('data/territorio_municipal_sao_roque_web.geojson')
geom_mun_wgs = gdf_mun.geometry.iloc[0]

# Converter município para UTM
gdf_mun_utm = gdf_mun.to_crs(epsg=31983)
geom_mun_utm = gdf_mun_utm.geometry.iloc[0]

def create_circle_polygon(lon, lat, radius_meters, num_pts=36):
    # Projeta para UTM, aplica buffer, reprojeta para WGS84
    utm_x, utm_y = transformer_wgs_to_utm.transform(lon, lat)
    pt_utm = Point(utm_x, utm_y)
    poly_utm = pt_utm.buffer(radius_meters, resolution=num_pts//4)
    # Reprojetar para WGS84
    coords_wgs = [transformer_utm_to_wgs.transform(x, y) for x, y in poly_utm.exterior.coords]
    return Polygon(coords_wgs)

def create_pzph_corridor(lon, lat, radius_meters=1000, angle_deg=60, width_start=60, width_end=300):
    # Rampa de aproximação e subida de heliponto (setor leque)
    utm_x, utm_y = transformer_wgs_to_utm.transform(lon, lat)
    
    # Gerar dois funis opostos (aproximação e decolagem) ao longo do eixo angle_deg
    corridors = []
    for heading in [angle_deg, (angle_deg + 180) % 360]:
        rad = math.radians(heading)
        perp = rad + math.pi / 2
        
        # Ponto inicial do funil
        p0_l = (utm_x + (width_start / 2) * math.cos(perp), utm_y + (width_start / 2) * math.sin(perp))
        p0_r = (utm_x - (width_start / 2) * math.cos(perp), utm_y - (width_start / 2) * math.sin(perp))
        
        # Ponto final a radius_meters
        fx = utm_x + radius_meters * math.sin(rad)
        fy = utm_y + radius_meters * math.cos(rad)
        
        p1_l = (fx + (width_end / 2) * math.cos(perp), fy + (width_end / 2) * math.sin(perp))
        p1_r = (fx - (width_end / 2) * math.cos(perp), fy - (width_end / 2) * math.sin(perp))
        
        poly_utm = Polygon([p0_l, p1_l, p1_r, p0_r, p0_l])
        corridors.append(poly_utm)
        
    # Unir os dois funis com a área horizontal interna de 200m
    pt_utm = Point(utm_x, utm_y)
    inner_circle = pt_utm.buffer(200)
    union_utm = inner_circle.union(corridors[0]).union(corridors[1])
    
    # Reprojetar para WGS84
    if union_utm.geom_type == 'Polygon':
        coords_wgs = [transformer_utm_to_wgs.transform(x, y) for x, y in union_utm.exterior.coords]
        return Polygon(coords_wgs)
    else:
        polys = []
        for poly in union_utm.geoms:
            coords_wgs = [transformer_utm_to_wgs.transform(x, y) for x, y in poly.exterior.coords]
            polys.append(Polygon(coords_wgs))
        return MultiPolygon(polys)

# 2. Heliponto 1: Vila Don Patto (SWVD)
lon_vdp, lat_vdp = -47.1366142, -23.5630678
fato_vdp = create_circle_polygon(lon_vdp, lat_vdp, radius_meters=25)
pzph_vdp = create_pzph_corridor(lon_vdp, lat_vdp, radius_meters=1000, angle_deg=70)

# 3. Heliponto 2: Taxaquara Golf Club (SIZT)
lon_tax, lat_tax = -47.0880326, -23.5236937
fato_tax = create_circle_polygon(lon_tax, lat_tax, radius_meters=25)
pzph_tax = create_pzph_corridor(lon_tax, lat_tax, radius_meters=1000, angle_deg=45)

# 4. Heliponto 3: NÓR Hotel & Spa
lon_nor, lat_nor = -47.1148000, -23.5715000
fato_nor = create_circle_polygon(lon_nor, lat_nor, radius_meters=25)
pzph_nor = create_pzph_corridor(lon_nor, lat_nor, radius_meters=1000, angle_deg=110)

# 5. Superfície Horizontal Externa de Congonhas (SBSP / SHE Raio 45 km)
lon_cg, lat_cg = -46.6565, -23.6261
utm_cg_x, utm_cg_y = transformer_wgs_to_utm.transform(lon_cg, lat_cg)
pt_cg_utm = Point(utm_cg_x, utm_cg_y)
she_cg_utm = pt_cg_utm.buffer(45000) # Raio de 45.000 metros (45 km)

# Intersectar a SHE de Congonhas com o território de São Roque
she_sr_utm = she_cg_utm.intersection(geom_mun_utm)
area_she_ha = round(she_sr_utm.area / 10000.0, 2)
pct_she = round((she_sr_utm.area / geom_mun_utm.area) * 100.0, 2)

# Reprojetar para WGS84
coords_she_wgs = [transformer_utm_to_wgs.transform(x, y) for x, y in she_sr_utm.exterior.coords]
poly_she_cg = Polygon(coords_she_wgs)

# 6. Montar a lista completa de features
new_features = []

# Manter as 3 features do Catarina
for feat in catarina_data['features']:
    new_features.append(feat)

# Adicionar Heliponto Vila Don Patto
new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "PZPH_SWVD",
        "tipo_elemento": "Plano de Zona de Proteção de Heliponto (PZPH)",
        "nome": "PZPH - Heliponto Vila Don Patto",
        "indicativo_icao": "SWVD",
        "instalacao": "Heliponto Privado Homologado",
        "localizacao": "Estrada do Vinho, km 2,5 - Canguera / Roteiro do Vinho",
        "portaria_decea": "Portaria nº 176/DGCEA de 08/10/2014 (Processo 17990)",
        "esfera": "Federal (Comando da Aeronáutica / DECEA)",
        "base_legal": "Lei Federal nº 7.565/86 (CBA Arts. 43-46), RBAC 155 da ANAC, ICA 11-408",
        "dimensoes": "FATO 25m / Rampa de Aproximação e Subida 1.000m (8% a 12,5%)",
        "restricao_gabarito": "Servidão aeronáutica compulsória. Vedada edificação, galpão, antena ou poste que perfure as superfícies de aproximação.",
        "anuencia_previa": "Obrigatória aprovação prévia no SYSAGA/DECEA antes de alvará municipal.",
        "cor_hex": "#F97316",
        "cor_borda": "#C2410C",
        "descricao": "Zona de proteção com rampas de segurança para helicópteros atendendo ao complexo enogastronômico da Vila Don Patto."
    },
    "geometry": pzph_vdp.__geo_interface__
})

new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "FATO_SWVD",
        "tipo_elemento": "Área de Pouso e Decolagem de Helicópteros (FATO/TLOF)",
        "nome": "Heliponto Vila Don Patto (SWVD)",
        "indicativo_icao": "SWVD",
        "instalacao": "Piso / Área de Toque de Helicópteros",
        "localizacao": "Estrada do Vinho, km 2,5 - Canguera",
        "portaria_decea": "Portaria 176/DGCEA/2014",
        "esfera": "Federal / Privado Homologado",
        "base_legal": "RBAC 155 ANAC / ICA 11-408 DECEA",
        "dimensoes": "25m diâmetro",
        "cor_hex": "#EA580C",
        "cor_borda": "#9A3412",
        "descricao": "Área de toque e elevação (TLOF) homologada para pouso e decolagem de helicópteros civis e executivos."
    },
    "geometry": fato_vdp.__geo_interface__
})

# Adicionar Heliponto Taxaquara Golf Club
new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "PZPH_SIZT",
        "tipo_elemento": "Plano de Zona de Proteção de Heliponto (PZPH)",
        "nome": "PZPH - Heliponto Taxaquara Golf Club",
        "indicativo_icao": "SIZT",
        "instalacao": "Heliponto Privado Homologado",
        "localizacao": "Estrada Municipal Darcy Penteado - Condomínio Vila Darcy Penteado",
        "portaria_decea": "Portaria nº 394/ICA de 30/05/2018 (Processo 18926)",
        "esfera": "Federal (Comando da Aeronáutica / DECEA)",
        "base_legal": "Lei Federal nº 7.565/86 (CBA Arts. 43-46), RBAC 155 da ANAC, ICA 11-408",
        "dimensoes": "FATO 25m / Rampa de Aproximação 1.000m",
        "restricao_gabarito": "Gabarito restrito para imóveis residenciais, postes e árvores no cone de aproximação do heliponto.",
        "anuencia_previa": "Obrigatória consulta no SYSAGA para novas construções no entorno.",
        "cor_hex": "#F97316",
        "cor_borda": "#C2410C",
        "descricao": "Zona de proteção de heliponto do campo de golfe e condomínio rural Taxaquara."
    },
    "geometry": pzph_tax.__geo_interface__
})

new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "FATO_SIZT",
        "tipo_elemento": "Área de Pouso e Decolagem de Helicópteros (FATO/TLOF)",
        "nome": "Heliponto Taxaquara Golf Club (SIZT)",
        "indicativo_icao": "SIZT",
        "instalacao": "Piso / Área de Toque de Helicópteros",
        "localizacao": "Estrada Darcy Penteado - Bairro Taxaquara",
        "portaria_decea": "Portaria 394/ICA/2018",
        "esfera": "Federal / Privado Homologado",
        "base_legal": "RBAC 155 ANAC / ICA 11-408 DECEA",
        "dimensoes": "25m diâmetro",
        "cor_hex": "#EA580C",
        "cor_borda": "#9A3412",
        "descricao": "Heliponto privado homologado no Taxaquara Golf Club."
    },
    "geometry": fato_tax.__geo_interface__
})

# Adicionar Heliponto NÓR Hotel & Spa
new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "PZPH_NOR",
        "tipo_elemento": "Plano de Zona de Proteção de Heliponto (PZPH)",
        "nome": "PZPH - Heliponto NÓR Hotel & Spa",
        "indicativo_icao": "NÓR (Portaria 1465)",
        "instalacao": "Heliponto Privado Homologado",
        "localizacao": "Estrada do Pessegueiro, 1000 - Bairro Gabriel Piza",
        "portaria_decea": "Portaria nº 1465/SAGA de 15/06/2023 (Processo 25568)",
        "esfera": "Federal (Comando da Aeronáutica / DECEA)",
        "base_legal": "Lei Federal nº 7.565/86 (CBA Arts. 43-46), RBAC 155 da ANAC, ICA 11-408",
        "dimensoes": "FATO 25m / Rampa de Aproximação 1.000m",
        "restricao_gabarito": "Proteção do funil de aproximação e subida de helicópteros executivos conectando a capital ao resort.",
        "anuencia_previa": "Exigência de parecer do DECEA para construções elevadas e linhas de energia no cone.",
        "cor_hex": "#F97316",
        "cor_borda": "#C2410C",
        "descricao": "Zona de proteção do heliponto mais recente de São Roque, atendendo ao hotel boutique NÓR Hotel & Spa."
    },
    "geometry": pzph_nor.__geo_interface__
})

new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "FATO_NOR",
        "tipo_elemento": "Área de Pouso e Decolagem de Helicópteros (FATO/TLOF)",
        "nome": "Heliponto NÓR Hotel & Spa",
        "indicativo_icao": "NÓR (DECEA 2023)",
        "instalacao": "Piso / Área de Toque de Helicópteros",
        "localizacao": "Estrada do Pessegueiro, 1000 - Gabriel Piza",
        "portaria_decea": "Portaria 1465/SAGA/2023",
        "esfera": "Federal / Privado Homologado",
        "base_legal": "RBAC 155 ANAC / ICA 11-408 DECEA",
        "dimensoes": "25m diâmetro",
        "cor_hex": "#EA580C",
        "cor_borda": "#9A3412",
        "descricao": "Área de pouso e decolagem de helicópteros executivos no NÓR Hotel & Spa."
    },
    "geometry": fato_nor.__geo_interface__
})

# Adicionar Congonhas (SBSP / SHE)
new_features.append({
    "type": "Feature",
    "properties": {
        "codigo": "SHE_SBSP_CONGONHAS",
        "tipo_elemento": "Superfície Horizontal Externa (SHE) & TMA São Paulo",
        "nome": "Superfície Horizontal Externa de Congonhas (SBSP / Raio 45 km) e TMA-SP",
        "indicativo_icao": "SBSP",
        "instalacao": "Área de Manobra Externa e Proteção de Auxílios à Navegação Aérea (PZANA)",
        "localizacao": "Setor Leste de São Roque (Divisa Cotia/Itapevi e Serras do Saboó e Cruzeiro)",
        "portaria_decea": "Portaria nº 28/ICA de 14/07/2015 (Processo 18751)",
        "esfera": "Federal (Comando da Aeronáutica / DECEA / ANAC)",
        "base_legal": "Código Brasileiro de Aeronáutica (Lei 7.565/86 Art. 44 e 45), ICA 11-408, ICA 63-19",
        "dimensoes": f"Raio de 45 km a partir de SBSP · {area_she_ha:,.2f} ha em São Roque ({pct_she}% do município)",
        "restricao_gabarito": "Restrição de altura e sinalização obrigatória para torres de telecomunicação, linhas de transmissão e parques eólicos nos cumes mais altos para não interferir nas trajetórias IFR e auxílios de rádio da TMA-SP.",
        "anuencia_previa": "Obrigatório processo de OPEA (Objeto Projetado no Espaço Aéreo) junto ao IV COMAR / DECEA para estruturas elevadas.",
        "cor_hex": "#8B5CF6",
        "cor_borda": "#6D28D9",
        "descricao": "Projeção da área de segurança e manobra externa do Aeroporto de Congonhas (SBSP) e corredores IFR da Terminal São Paulo sobre as serras de São Roque."
    },
    "geometry": poly_she_cg.__geo_interface__
})

# Salvar GeoJSON enriquecido
output_geojson = {
    "type": "FeatureCollection",
    "features": new_features
}

with open('data/zona_protecao_aeroportuaria_catarina_web.geojson', 'w', encoding='utf-8') as f:
    json.dump(output_geojson, f, ensure_ascii=False, indent=2)

print(f"Sucesso! Geradas {len(new_features)} features na camada aeroportuária e de helipontos.")
print(f"  - Aeroporto Catarina (Pista, Cone, ASA 20km)")
print(f"  - Heliponto Vila Don Patto (SWVD - FATO + PZPH 1.000m)")
print(f"  - Heliponto Taxaquara Golf Club (SIZT - FATO + PZPH 1.000m)")
print(f"  - Heliponto NÓR Hotel & Spa (Portaria 1465/SAGA - FATO + PZPH 1.000m)")
print(f"  - Superfície Horizontal Externa de Congonhas (SBSP 45km): {area_she_ha} ha ({pct_she}%)")
