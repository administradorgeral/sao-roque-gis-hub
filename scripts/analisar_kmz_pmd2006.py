import zipfile
import xml.etree.ElementTree as ET
import os

kmz_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\PMD2006 - Zoneamento.kmz"
with zipfile.ZipFile(kmz_path, "r") as z:
    kml_bytes = z.read("doc.kml")

# Salvar o KML descompactado em dados_oficiais/municipal/
out_kml_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\municipal"
os.makedirs(out_kml_dir, exist_ok=True)
out_kml_path = os.path.join(out_kml_dir, "PMD2006_Zoneamento.kml")
with open(out_kml_path, "wb") as f:
    f.write(kml_bytes)
print(f"KML extraído para {out_kml_path} ({len(kml_bytes)} bytes)")

root = ET.fromstring(kml_bytes)
# Tenta com e sem namespace
ns_map = {"kml": "http://www.opengis.net/kml/2.2"}
placemarks = root.findall(".//kml:Placemark", ns_map)
if not placemarks:
    placemarks = root.findall(".//Placemark")

print(f"Total de Placemarks encontrados: {len(placemarks)}")

zone_counts = {}
for p in placemarks:
    name_el = p.find("kml:name", ns_map) if "kml" in root.tag else p.find("name")
    name_val = name_el.text if name_el is not None else "Sem nome"
    zone_counts[name_val] = zone_counts.get(name_val, 0) + 1

print("\n--- Zonas e Entidades no KMZ ---")
for zone, count in sorted(zone_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {zone}: {count} polígono(s)")
