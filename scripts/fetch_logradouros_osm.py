import urllib.request
import urllib.parse
import json
import time

print("=== CONSULTA DE LOGRADOUROS E RUAS DE SÃO ROQUE (OPENSTREETMAP 2024/2026) ===")

overpass_url = "https://overpass-api.de/api/interpreter"
# Query por bounding box do município de São Roque:
# south=-23.655, west=-47.210, north=-23.410, east=-46.990
query = """
[out:json][timeout:45];
(
  way["highway"]["name"](-23.655,-47.210,-23.410,-46.990);
);
out geom tags;
"""

data = urllib.parse.urlencode({"data": query}).encode("utf-8")
req = urllib.request.Request(
    overpass_url, 
    data=data, 
    headers={"User-Agent": "SaoRoqueGIS/2.0 (Inteligencia Territorial)"}
)

t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=50) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        elements = result.get("elements", [])
        print(f"Sucesso! Recebidos {len(elements)} trechos de vias em {time.time()-t0:.2f}s.")
        
        # Converter para GeoJSON
        features = []
        unique_names = set()
        
        for el in elements:
            geometry = el.get("geometry")
            tags = el.get("tags", {})
            name = tags.get("name")
            if not geometry or len(geometry) < 2 or not name:
                continue
                
            coords = [[pt["lon"], pt["lat"]] for pt in geometry]
            unique_names.add(name)
            
            features.append({
                "type": "Feature",
                "properties": {
                    "id": el.get("id"),
                    "nome": name,
                    "tipo_via": tags.get("highway", "residencial"),
                    "superficie": tags.get("surface", "pavimentada"),
                    "velocidade_max": tags.get("maxspeed"),
                    "bairro": tags.get("addr:suburb") or tags.get("place"),
                    "ref": tags.get("ref"),
                    "oneway": tags.get("oneway") == "yes",
                    "municipio": "São Roque"
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": coords
                }
            })
            
        print(f"Total de logradouros únicos encontrados: {len(unique_names)}")
        print("Amostra dos logradouros:")
        for nm in sorted(list(unique_names))[:15]:
            print(f"  - {nm}")
            
        fc = {
            "type": "FeatureCollection",
            "name": "logradouros_sao_roque_osm",
            "features": features
        }
        
        out_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/logradouros_sao_roque_web.geojson"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(fc, f, ensure_ascii=False)
            
        print(f"\nGeoJSON de Logradouros salvo com sucesso: {out_path} ({len(features)} trechos de vias)")
        
except Exception as e:
    print(f"Erro na consulta Overpass: {e}")
