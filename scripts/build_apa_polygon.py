import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
from shapely.ops import split, unary_union

# 1. Carregar o limite norte (Linha da APA)
gdf_line = gpd.read_file("data/apa_itupararanga_limite_sao_roque.gpkg")
line = gdf_line.geometry.iloc[0]

# 2. Carregar o polígono completo do município de São Roque
gdf_mun = gpd.read_file("data/geomorfologico_sao_roque.gpkg")
mun_poly = unary_union(gdf_mun.geometry)

print(f"Área total do município: {mun_poly.area / 10000.0:.2f} ha")
print(f"Extensão da linha da APA: {line.length / 1000.0:.2f} km")

# Estender levemente as pontas da linha da APA para garantir interseção limpa com a borda municipal
coords = list(line.coords)
# Vetor inicial (oeste)
dx0 = coords[0][0] - coords[1][0]
dy0 = coords[0][1] - coords[1][1]
p0_ext = (coords[0][0] + dx0 * 5, coords[0][1] + dy0 * 5)

# Vetor final (leste)
dx1 = coords[-1][0] - coords[-2][0]
dy1 = coords[-1][1] - coords[-2][1]
p1_ext = (coords[-1][0] + dx1 * 5, coords[-1][1] + dy1 * 5)

extended_line = LineString([p0_ext] + coords + [p1_ext])

# Fatiar o polígono municipal pela linha divisória
parts = split(mun_poly, extended_line)
print(f"O fatiamento produziu {len(parts.geoms)} partes:")

south_parts = []
north_parts = []

for i, p in enumerate(parts.geoms):
    cent = p.centroid
    area_ha = p.area / 10000.0
    # Centroide do sul de São Roque tem Y < 7392000
    if cent.y < 7391000:
        south_parts.append(p)
        print(f"  Parte #{i} [SUL - APA]: {area_ha:.2f} ha, centroide=({cent.x:.1f}, {cent.y:.1f})")
    else:
        north_parts.append(p)
        print(f"  Parte #{i} [NORTE]: {area_ha:.2f} ha, centroide=({cent.x:.1f}, {cent.y:.1f})")

poly_apa_south = unary_union(south_parts)
print(f"\nÁrea total da APA Itupararanga em São Roque (Polígono Sul): {poly_apa_south.area / 10000.0:.2f} ha")
