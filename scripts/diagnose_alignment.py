import geopandas as gpd
import json
from shapely.geometry import shape

print("=== DIAGNÓSTICO DE ALINHAMENTO ENTRE CAMADAS ===")

decliv_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"
mdt_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson"
hidro_web = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\hidrografia_sao_roque_web.geojson"

gdf_decliv = gpd.read_file(decliv_web)
gdf_mdt = gpd.read_file(mdt_web)
gdf_hidro = gpd.read_file(hidro_web)

b_dec = gdf_decliv.total_bounds # minx, miny, maxx, maxy
b_mdt = gdf_mdt.total_bounds
b_hidro = gdf_hidro.total_bounds

print(f"DECLIVIDADE (Padrão de Referência Aprovado):")
print(f"  Bounds WGS84: X=[{b_dec[0]:.6f}, {b_dec[2]:.6f}], Y=[{b_dec[1]:.6f}, {b_dec[3]:.6f}]")
print(f"  Centroide WGS84: X={(b_dec[0]+b_dec[2])/2:.6f}, Y={(b_dec[1]+b_dec[3])/2:.6f}")

print(f"\nMDT:")
print(f"  Bounds WGS84: X=[{b_mdt[0]:.6f}, {b_mdt[2]:.6f}], Y=[{b_mdt[1]:.6f}, {b_mdt[3]:.6f}]")
print(f"  Centroide WGS84: X={(b_mdt[0]+b_mdt[2])/2:.6f}, Y={(b_mdt[1]+b_mdt[3])/2:.6f}")

print(f"\nHIDROGRAFIA:")
print(f"  Bounds WGS84: X=[{b_hidro[0]:.6f}, {b_hidro[2]:.6f}], Y=[{b_hidro[1]:.6f}, {b_hidro[3]:.6f}]")
print(f"  Centroide WGS84: X={(b_hidro[0]+b_hidro[2])/2:.6f}, Y={(b_hidro[1]+b_hidro[3])/2:.6f}")

# Calcular o desvio do centroide em relação à Declividade
# 1 grau de lon em ~23.5S = ~102 km -> 1e-5 grau = ~1.02 m
# 1 grau de lat = ~111 km -> 1e-5 grau = ~1.11 m
c_dec_x = (b_dec[0]+b_dec[2])/2
c_dec_y = (b_dec[1]+b_dec[3])/2

c_mdt_x = (b_mdt[0]+b_mdt[2])/2
c_mdt_y = (b_mdt[1]+b_mdt[3])/2

c_hidro_x = (b_hidro[0]+b_hidro[2])/2
c_hidro_y = (b_hidro[1]+b_hidro[3])/2

print(f"\n--- DESVIOS EM RELAÇÃO À DECLIVIDADE ---")
dx_mdt_m = (c_mdt_x - c_dec_x) * 102000
dy_mdt_m = (c_mdt_y - c_dec_y) * 111000
print(f"MDT desvio do centroide:")
print(f"  Delta X: {c_mdt_x - c_dec_x:.6f}° (~{dx_mdt_m:+.1f} metros) {'(MAIS À ESQUERDA)' if dx_mdt_m < 0 else '(MAIS À DIREITA)'}")
print(f"  Delta Y: {c_mdt_y - c_dec_y:.6f}° (~{dy_mdt_m:+.1f} metros)")

dx_hidro_m = (c_hidro_x - c_dec_x) * 102000
dy_hidro_m = (c_hidro_y - c_dec_y) * 111000
print(f"\nHIDROGRAFIA desvio do centroide:")
print(f"  Delta X: {c_hidro_x - c_dec_x:.6f}° (~{dx_hidro_m:+.1f} metros) {'(MAIS À ESQUERDA)' if dx_hidro_m < 0 else '(MAIS À DIREITA)'}")
print(f"  Delta Y: {c_hidro_y - c_dec_y:.6f}° (~{dy_hidro_m:+.1f} metros)")

# Verificar se há feições espúrias à direita no MDT (legenda)
print("\n--- DETECÇÃO DE RETÂNGULOS DA LEGENDA NO MDT ---")
# Elementos com X > b_dec[2] + 0.01 (fora do limite leste da declividade)
east_spurious = gdf_mdt[gdf_mdt.geometry.bounds['maxx'] > b_dec[2]]
print(f"Feições do MDT além do limite leste de São Roque: {len(east_spurious)}")
for idx, row in east_spurious.iterrows():
    b = row.geometry.bounds
    print(f"  Feição {idx}: classe={row.get('classe')}, Bounds X=[{b[0]:.5f}, {b[2]:.5f}], Y=[{b[1]:.5f}, {b[3]:.5f}], area_ha={row.get('Área da Mancha Altimétrica')}")
