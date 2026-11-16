import xml.etree.ElementTree as ET
import json
import os

kml_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\dados_oficiais\municipal\PMD2006_Zoneamento.kml"

with open(kml_path, "r", encoding="utf-8") as f:
    kml_content = f.read()

root = ET.fromstring(kml_content)
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Mapa de cores oficiais de zoneamento urbano para visualização clean
CORES_ZONEAMENTO = {
    "Central": {"cor": "#7c3aed", "sigla": "ZC", "nome_completo": "Zona Central"},
    "Densidade Alta": {"cor": "#dc2626", "sigla": "ZDA", "nome_completo": "Zona de Densidade Alta"},
    "Densidade Media": {"cor": "#ea580c", "sigla": "ZDM", "nome_completo": "Zona de Densidade Média"},
    "Densidade Baixa": {"cor": "#ca8a04", "sigla": "ZDB", "nome_completo": "Zona de Densidade Baixa"},
    "Consolidação urbana": {"cor": "#2563eb", "sigla": "ZCU", "nome_completo": "Zona de Consolidação Urbana"},
    "Industrial": {"cor": "#475569", "sigla": "ZI", "nome_completo": "Zona Industrial"},
    "Preservação": {"cor": "#15803d", "sigla": "ZP", "nome_completo": "Zona de Preservação"},
    "Rural": {"cor": "#65a30d", "sigla": "ZR", "nome_completo": "Zona Rural"},
    "ZUCAer": {"cor": "#0891b2", "sigla": "ZUCAER", "nome_completo": "Zona de Uso Controlado Aeroportuário"},
    "ZUE-Desenvolvimento Turistico": {"cor": "#059669", "sigla": "ZUE-DT", "nome_completo": "ZUE - Desenvolvimento Turístico (Roteiro do Vinho)"},
    "ZUE-Desenvolvimento Econômico": {"cor": "#d97706", "sigla": "ZUE-DE", "nome_completo": "ZUE - Desenvolvimento Econômico (Eixo Raposo)"},
    "ZUE-Ocupação Estratégica": {"cor": "#9333ea", "sigla": "ZUE-OE", "nome_completo": "ZUE - Ocupação Estratégica"},
    "ZUE-Chacaras de SJN": {"cor": "#14b8a6", "sigla": "ZUE-CSJN", "nome_completo": "ZUE - Chácaras de São João Novo"},
    "ZUE-Chacaras em Manancial": {"cor": "#0284c7", "sigla": "ZUE-CM", "nome_completo": "ZUE - Chácaras em Área de Manancial"}
}

def parse_coordinates_text(coord_str):
    coords = []
    for point_str in coord_str.strip().split():
        parts = point_str.split(",")
        if len(parts) >= 2:
            lng = float(parts[0])
            lat = float(parts[1])
            coords.append([lng, lat])
    return coords

features = []
placemarks = root.findall(".//kml:Placemark", ns)

total_coords = 0

for idx, p in enumerate(placemarks):
    name_el = p.find("kml:name", ns)
    name = name_el.text.strip() if name_el is not None and name_el.text else f"Zona_{idx+1}"
    
    desc_el = p.find("kml:description", ns)
    desc = desc_el.text.strip() if desc_el is not None and desc_el.text else ""

    info_cor = CORES_ZONEAMENTO.get(name, {"cor": "#3b82f6", "sigla": name[:6].upper(), "nome_completo": name})

    # Busca polígonos
    polygons = p.findall(".//kml:Polygon", ns)
    
    for poly in polygons:
        outer = poly.find(".//kml:outerBoundaryIs//kml:coordinates", ns)
        if outer is not None and outer.text:
            outer_coords = parse_coordinates_text(outer.text)
            if len(outer_coords) < 3:
                continue
            
            # Fecha o anel se necessário
            if outer_coords[0] != outer_coords[-1]:
                outer_coords.append(outer_coords[0])

            inners_coords = []
            for inner in poly.findall(".//kml:innerBoundaryIs//kml:coordinates", ns):
                if inner.text:
                    hole = parse_coordinates_text(inner.text)
                    if len(hole) >= 3:
                        if hole[0] != hole[-1]:
                            hole.append(hole[0])
                        inners_coords.append(hole)

            total_coords += len(outer_coords)

            feat = {
                "type": "Feature",
                "id": f"pmd2006_{name.lower().replace(' ', '_')}_{idx}",
                "properties": {
                    "zona": name,
                    "sigla": info_cor["sigla"],
                    "denominacao": info_cor["nome_completo"],
                    "lei_regulamentadora": "Lei Complementar Municipal nº 40/2006 (Plano Diretor)",
                    "esfera": "Municipal",
                    "orgao_gestor": "Prefeitura da Estância Turística de São Roque",
                    "fonte_oficial": "PMD 2006 - Zoneamento (Prefeitura Municipal de São Roque)",
                    "cor": info_cor["cor"],
                    "descricao": desc or f"Zona oficial delimitada pela LC 40/2006 - {name}"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [outer_coords] + inners_coords
                }
            }
            features.append(feat)

geojson = {
    "type": "FeatureCollection",
    "name": "PMD2006_Zoneamento_Sao_Roque",
    "crs": {
        "type": "name",
        "properties": {
            "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
        }
    },
    "metadata": {
        "orgao": "Prefeitura da Estância Turística de São Roque",
        "plano_diretor": "Lei Complementar nº 40/2006",
        "total_feicoes": len(features),
        "total_vertices": total_coords,
        "arquivo_fonte": "PMD2006 - Zoneamento.kmz"
    },
    "features": features
}

out_geojson_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\pmsr_zoneamento_pmd2006.geojson"
with open(out_geojson_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(features)} feições de zoneamento exportadas.")
print(f"Total de vértices geodésicos: {total_coords}")
print(f"GeoJSON salvo em: {out_geojson_path}")
