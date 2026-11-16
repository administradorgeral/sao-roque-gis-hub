import json
import sqlite3

# Verificar se temos o limite municipal em algum dos arquivos GeoJSON
paths = [
    r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\layers\zoneamento_pmd2006.js",
    r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\layers\zoneamento_minuta_pmd2006.js"
]

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"Arquivo {p}: {len(content)} caracteres")
    # Procurar bboxes
    if 'FeatureCollection' in content:
        print("  Contém FeatureCollection GeoJSON")

# Vamos ver os extremos de latitude e longitude das geometrias do zoneamento
import re
lons = []
lats = []
with open(paths[0], 'r', encoding='utf-8') as f:
    text = f.read()
    coords = re.findall(r"\[\s*(-47\.\d+)\s*,\s*(-23\.\d+)\s*\]", text)
    for c in coords:
        lons.append(float(c[0]))
        lats.append(float(c[1]))

if lons and lats:
    print(f"Extremos do Zoneamento Vigente (WGS84 / SIRGAS 2000):")
    print(f"  Oeste (Lon min): {min(lons):.5f}")
    print(f"  Leste (Lon max): {max(lons):.5f}")
    print(f"  Sul (Lat min):   {min(lats):.5f}")
    print(f"  Norte (Lat max): {max(lats):.5f}")

# Comparar com o bounding box do PDF que extraímos antes:
# SW: [-23.65803, -47.25178]
# NE: [-23.40215, -46.96443]
print("\nExtremos do Neatline do PDF de Declividade (SIRGAS 2000):")
print("  Oeste (Lon min): -47.25178")
print("  Leste (Lon max): -46.96443")
print("  Sul (Lat min):   -23.65803")
print("  Norte (Lat max): -23.40215")
