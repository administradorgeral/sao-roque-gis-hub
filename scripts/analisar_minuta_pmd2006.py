import zipfile
import xml.etree.ElementTree as ET
import os
import hashlib
import json

kmz_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\minutaPMD2006 - Zoneamento.kmz"
with open(kmz_path, "rb") as f:
    kmz_bytes = f.read()

kmz_hash = hashlib.sha256(kmz_bytes).hexdigest()
print(f"KMZ Path: {kmz_path}")
print(f"KMZ Size: {len(kmz_bytes):,} bytes")
print(f"KMZ SHA-256: {kmz_hash}")

with zipfile.ZipFile(kmz_path, "r") as z:
    file_list = z.namelist()
    print("Arquivos no KMZ:", file_list)
    kml_name = [name for name in file_list if name.endswith(".kml")][0]
    kml_bytes = z.read(kml_name)

kml_hash = hashlib.sha256(kml_bytes).hexdigest()
print(f"Arquivo KML interno: {kml_name}")
print(f"KML Size: {len(kml_bytes):,} bytes")
print(f"KML SHA-256: {kml_hash}")

# Salvar KML descompactado em dados_oficiais/municipal/
out_kml_dir = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\municipal"
os.makedirs(out_kml_dir, exist_ok=True)
out_kml_path = os.path.join(out_kml_dir, "minutaPMD2006_Zoneamento.kml")
with open(out_kml_path, "wb") as f:
    f.write(kml_bytes)

# Salvar cópia do KMZ arquivado
out_kmz_path = os.path.join(out_kml_dir, "minutaPMD2006_Zoneamento.kmz")
with open(out_kmz_path, "wb") as f:
    f.write(kmz_bytes)

root = ET.fromstring(kml_bytes)
ns = ""
if root.tag.startswith("{"):
    ns = root.tag.split("}")[0] + "}"

def find_all(el, tag):
    return el.findall(f".//{ns}{tag}") if ns else el.findall(f".//{tag}")

def find(el, tag):
    return el.find(f"{ns}{tag}") if ns else el.find(tag)

doc_name_el = find(root, "Document")
doc_title = find(doc_name_el, "name").text if doc_name_el is not None and find(doc_name_el, "name") is not None else "Sem Título"
print(f"Título do Documento KML: {doc_title}")

placemarks = find_all(root, "Placemark")
print(f"Total de Placemarks: {len(placemarks)}")

zones = []
total_vertices = 0
for idx, p in enumerate(placemarks):
    name_el = find(p, "name")
    name = name_el.text.strip() if name_el is not None and name_el.text else f"Elemento_{idx+1}"
    
    desc_el = find(p, "description")
    desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""
    
    style_el = find(p, "styleUrl")
    style = style_el.text.strip() if style_el is not None and style_el.text else ""
    
    # Contagem de polígonos e vértices
    polys = find_all(p, "Polygon")
    p_vertices = 0
    for poly in polys:
        coords_el = find(poly, "coordinates")
        if coords_el is not None and coords_el.text:
            raw = coords_el.text.strip()
            pts = [pt for pt in raw.split() if pt.strip()]
            p_vertices += len(pts)
            
    total_vertices += p_vertices
    zones.append({
        "id": idx + 1,
        "name": name,
        "description": desc,
        "style": style,
        "polygons": len(polys),
        "vertices": p_vertices
    })

print(f"Total de vértices geodésicos: {total_vertices:,}")
print("\n--- Lista de Camadas / Zonas no arquivo da Minuta ---")
for z in zones:
    print(f"  [{z['id']:02d}] {z['name']} | Polígonos: {z['polygons']} | Vértices: {z['vertices']:,}")

# Comparação rápida com o arquivo aprovado PMD2006
pmd_kml_path = os.path.join(out_kml_dir, "PMD2006_Zoneamento.kml")
if os.path.exists(pmd_kml_path):
    with open(pmd_kml_path, "rb") as f:
        pmd_bytes = f.read()
    print(f"\nComparação com PMD2006_Zoneamento.kml:")
    print(f"  Tamanho Minuta: {len(kml_bytes):,} bytes | Tamanho Aprovado: {len(pmd_bytes):,} bytes")
    print(f"  Mesmo Hash: {kml_hash == hashlib.sha256(pmd_bytes).hexdigest()}")
