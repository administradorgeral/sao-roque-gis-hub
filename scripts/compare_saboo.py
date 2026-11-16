import geopandas as gpd
from shapely.geometry import Point

# Carregar Declividade e MDT
gdf_dec = gpd.read_file(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson")
gdf_mdt = gpd.read_file(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson")

# Saboó em Declividade: maior polígono vermelho (#E60000)
saboo_dec = gdf_dec[gdf_dec['cor_hex'] == '#E60000'].sort_values(by='geometry', key=lambda x: x.apply(lambda g: g.area), ascending=False).iloc[0]
c_saboo_dec = saboo_dec.geometry.centroid

# Saboó em MDT: maior polígono vermelho (#FF2200, 970 a 1.125m)
saboo_mdt = gdf_mdt[gdf_mdt['classe'] == '970 a 1.125 m'].sort_values(by='geometry', key=lambda x: x.apply(lambda g: g.area), ascending=False).iloc[0]
c_saboo_mdt = saboo_mdt.geometry.centroid

print("=== COMPARAÇÃO DO CENTROIDE DO MORRO DO SABOÓ ===")
print(f"Saboó na Declividade (Referência): Lon = {c_saboo_dec.x:.6f}, Lat = {c_saboo_dec.y:.6f}")
print(f"Saboó no MDT (Atual):             Lon = {c_saboo_mdt.x:.6f}, Lat = {c_saboo_mdt.y:.6f}")

dx_deg = c_saboo_mdt.x - c_saboo_dec.x
dy_deg = c_saboo_mdt.y - c_saboo_dec.y
dx_m = dx_deg * 102000
dy_m = dy_deg * 111000

print(f"\nDeslocamento do Saboó no MDT em relação à Declividade:")
print(f"  Delta X (Leste-Oeste): {dx_deg:.6f}° = {dx_m:+.1f} metros {'(DESLOCADO PARA A ESQUERDA/OESTE)' if dx_m < 0 else '(DESLOCADO PARA A DIREITA/LESTE)'}")
print(f"  Delta Y (Norte-Sul):   {dy_deg:.6f}° = {dy_m:+.1f} metros")
