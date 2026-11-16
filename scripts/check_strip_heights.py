import geopandas as gpd
import numpy as np

print("=== INSPECIONANDO GEOMETRIAS DE DECLIVIDADE E MDT ===")

for name, path in [
    ("DECLIVIDADE", r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\declividade_sao_roque_web.geojson"),
    ("MDT", r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\mdt_sao_roque_web.geojson")
]:
    gdf = gpd.read_file(path)
    print(f"\n--- {name} ---")
    print(f"Total de feições: {len(gdf)}")
    
    # Calcular altura média dos bounding boxes das feições
    heights = []
    widths = []
    for geom in gdf.geometry:
        if geom and not geom.is_empty:
            b = geom.bounds # minx, miny, maxx, maxy
            heights.append(b[3] - b[1])
            widths.append(b[2] - b[0])
            
    print(f"Altura média (graus): {np.mean(heights):.6f} (~{np.mean(heights)*111000:.1f} metros)")
    print(f"Altura mediana: {np.median(heights):.6f} (~{np.median(heights)*111000:.1f} metros)")
    print(f"Largura média: {np.mean(widths):.6f} (~{np.mean(widths)*111000:.1f} metros)")
    
    # Verificar se as alturas estão concentradas em múltiplos de 18.48 pt (~325 metros)
    # Lembra que a altura de cada tira do PDF é 18.48 pt = ~325 metros no solo!
    h_m = np.array(heights) * 111000
    strip_height_m = 18.48 * 17.636684
    print(f"Altura de UMA TIRA DO PDF no solo: {strip_height_m:.1f} metros")
    near_strip = np.sum(np.abs(h_m - strip_height_m) < 30)
    print(f"Feições com altura exatamente igual à altura de uma tira do PDF: {near_strip} ({near_strip*100/len(gdf):.1f}%)")
