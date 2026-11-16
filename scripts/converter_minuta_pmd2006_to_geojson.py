import xml.etree.ElementTree as ET
import json
import os
import hashlib

kml_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\municipal\minutaPMD2006_Zoneamento.kml"

with open(kml_path, "r", encoding="utf-8", errors="ignore") as f:
    kml_content = f.read()

root = ET.fromstring(kml_content)
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# 1. Mapear Styles e cores
styles = {}
for style in root.findall(".//kml:Style", ns):
    sid = style.attrib.get("id")
    if not sid:
        continue
    poly_color = style.find(".//kml:PolyStyle/kml:color", ns)
    line_color = style.find(".//kml:LineStyle/kml:color", ns)
    
    # KML colors are aabbggrr -> convert to #rrggbb and opacity
    hex_fill = "#7c3aed"
    opacity = 0.55
    if poly_color is not None and poly_color.text:
        c = poly_color.text.strip().lower()
        if len(c) == 8:
            a = int(c[0:2], 16) / 255.0
            b = c[2:4]
            g = c[4:6]
            r = c[6:8]
            hex_fill = f"#{r}{g}{b}"
            opacity = round(a, 2)
    
    styles[f"#{sid}"] = {
        "fillColor": hex_fill,
        "opacity": opacity
    }

print(f"Total de estilos mapeados: {len(styles)}")
for sid, s in list(styles.items())[:10]:
    print(f"  Estilo {sid}: cor {s['fillColor']}, opacidade {s['opacity']}")

# 2. Extrair Placemarks e construir Features GeoJSON
features = []
total_vertices = 0

placemarks = root.findall(".//kml:Placemark", ns)
print(f"\nTotal de Placemarks no KML: {len(placemarks)}")

for idx, p in enumerate(placemarks):
    p_id = p.attrib.get("id", f"pm_{idx+1}")
    name_el = p.find("kml:name", ns)
    name = name_el.text.strip() if name_el is not None and name_el.text else f"Minuta_{idx+1}"
    
    style_el = p.find("kml:styleUrl", ns)
    style_ref = style_el.text.strip() if style_el is not None and style_el.text else ""
    style_data = styles.get(style_ref, {"fillColor": "#3b82f6", "opacity": 0.55})
    
    # Extrair ExtendedData
    props = {
        "fid": idx + 1,
        "id_kml": p_id,
        "nome": name,
        "camada": "Minuta do Plano Diretor 2006",
        "esfera": "Municipal",
        "orgao": "Prefeitura da Estância Turística de São Roque",
        "origem": "minutaPMD2006 - Zoneamento.kmz",
        "cor": style_data["fillColor"],
        "opacidade_sugerida": style_data["opacity"],
        "status_juridico": "Minuta Prévia de Zoneamento (Estudo Técnico PMD 2006)"
    }
    
    ext_data = p.find("kml:ExtendedData", ns)
    if ext_data is not None:
        for d in ext_data.findall("kml:Data", ns):
            d_name = d.attrib.get("name")
            val_el = d.find("kml:value", ns)
            val = val_el.text.strip() if val_el is not None and val_el.text else ""
            if d_name:
                if d_name == "area":
                    try:
                        props["area_m2"] = round(float(val), 2)
                        props["area_ha"] = round(float(val) / 10000.0, 2)
                    except:
                        props["area_m2"] = val
                elif d_name == "perimetro":
                    try:
                        props["perimetro_km"] = round(float(val), 2)
                    except:
                        props["perimetro"] = val
                elif d_name == "zoneamento":
                    props["sigla_zoneamento"] = val
                elif d_name not in ["geom"]:
                    props[d_name] = val

    # Extrair Polígonos
    polys = p.findall(".//kml:Polygon", ns)
    geo_polygons = []
    
    for poly in polys:
        rings = []
        # Outer boundary
        outer = poly.find(".//kml:outerBoundaryIs//kml:coordinates", ns)
        if outer is not None and outer.text:
            pts_str = [pt for pt in outer.text.strip().split() if pt.strip()]
            outer_ring = []
            for pt in pts_str:
                parts = [float(c) for c in pt.split(",") if c.strip()]
                if len(parts) >= 2:
                    outer_ring.append([parts[0], parts[1]])
            if len(outer_ring) >= 3:
                rings.append(outer_ring)
                total_vertices += len(outer_ring)
                
        # Inner boundaries (buracos/ilhas)
        for inner in poly.findall(".//kml:innerBoundaryIs//kml:coordinates", ns):
            if inner.text:
                pts_str = [pt for pt in inner.text.strip().split() if pt.strip()]
                inner_ring = []
                for pt in pts_str:
                    parts = [float(c) for c in pt.split(",") if c.strip()]
                    if len(parts) >= 2:
                        inner_ring.append([parts[0], parts[1]])
                if len(inner_ring) >= 3:
                    rings.append(inner_ring)
                    total_vertices += len(inner_ring)
                    
        if rings:
            geo_polygons.append(rings)
            
    if not geo_polygons:
        continue
        
    if len(geo_polygons) == 1:
        geometry = {
            "type": "Polygon",
            "coordinates": geo_polygons[0]
        }
    else:
        geometry = {
            "type": "MultiPolygon",
            "coordinates": geo_polygons
        }
        
    features.append({
        "type": "Feature",
        "id": idx + 1,
        "properties": props,
        "geometry": geometry
    })

geojson_obj = {
    "type": "FeatureCollection",
    "name": "pmsr_zoneamento_minuta_pmd2006",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "features": features
}

out_geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\pmsr_zoneamento_minuta_pmd2006.geojson"
with open(out_geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson_obj, f, ensure_ascii=False, indent=2)

geojson_size = os.path.getsize(out_geojson_path)
with open(out_geojson_path, "rb") as f:
    geojson_hash = hashlib.sha256(f.read()).hexdigest()

print(f"\n[SUCESSO] GeoJSON gerado: {out_geojson_path}")
print(f"Total de Feições (Zonas/Polígonos): {len(features)}")
print(f"Total de Vértices Geodésicos: {total_vertices:,}")
print(f"Tamanho do arquivo: {geojson_size:,} bytes ({geojson_size / (1024*1024):.2f} MB)")
print(f"SHA-256 do GeoJSON: {geojson_hash}")

# Listar resumo das feições
print("\n--- Feições da Minuta PMD 2006 ---")
for f in features:
    p = f["properties"]
    area_str = f"{p.get('area_ha', 'N/A')} ha" if 'area_ha' in p else "N/A"
    print(f"  [{p['fid']:02d}] {p['nome']} ({p.get('sigla_zoneamento', '')}) - Área: {area_str} - Cor: {p['cor']}")
