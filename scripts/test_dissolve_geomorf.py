import geopandas as gpd

gdf = gpd.read_file(r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\geomorfologico_sao_roque.gpkg')
print("Total rows:", len(gdf))
for idx, r in gdf.iterrows():
    print(f"Row {idx}: {r['codigo_classe']} | {r['Unidade Geomorfológica']} | area: {r['area_ha']} ha")

# Dissolve by codigo_classe
dissolved = gdf.dissolve(by='codigo_classe', as_index=False, aggfunc='first')
print("\nAfter dissolve total rows:", len(dissolved))
for idx, r in dissolved.iterrows():
    area_ha = r.geometry.area / 10000.0
    print(f"Dissolved {idx}: {r['codigo_classe']} | {r['Unidade Geomorfológica']} | geom_type={r.geometry.geom_type} | area: {area_ha:.2f} ha")
