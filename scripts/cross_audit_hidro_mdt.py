import geopandas as gpd

gdf_mdt = gpd.read_file(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson")
gdf_hidro = gpd.read_file(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\hidrografia_sao_roque_web.geojson")

# Pegar os fundos de vale do MDT (630 a 760m e 760 a 830m)
vales = gdf_mdt[gdf_mdt['classe'].isin(['630 a 760 m', '760 a 830 m'])]
vales_union = vales.geometry.unary_union

# Pegar as linhas de rios da hidrografia
rios = gdf_hidro[gdf_hidro['Tipo de Feição'].str.contains('Rio|Córrego', na=False)]

# Verificar quantas feições de rios intersectam ou estão dentro dos fundos de vale
intersectam = rios.geometry.intersects(vales_union)
pct = (intersectam.sum() / len(rios)) * 100.0

print(f"=== CONFERÊNCIA CRUZADA ESPACIAL (HIDROGRAFIA x MDT) ===")
print(f"Total de trechos de rios/córregos: {len(rios)}")
print(f"Trechos que fluem exatamente dentro dos fundos de vale do MDT: {intersectam.sum()} ({pct:.1f}%)")
