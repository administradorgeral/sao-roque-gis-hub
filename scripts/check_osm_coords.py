import json
import urllib.request
import urllib.parse

def geocode_osm(query):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'AntigravityGISResearch/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data:
                return float(data[0]['lat']), float(data[0]['lon']), data[0]['display_name']
    except Exception as e:
        return None, None, str(e)
    return None, None, "Not found"

points = [
    "Prefeitura Municipal de Cotia",
    "Terminal Metropolitano de Cotia",
    "Bairro Atalaia, Cotia",
    "Prefeitura Municipal de Vargem Grande Paulista",
    "Praça da Matriz, São Roque, SP",
    "Estação Osasco, SP",
    "Marco Zero da Sé, São Paulo"
]

for p in points:
    lat, lon, name = geocode_osm(p)
    print(f"{p}: Lat={lat}, Lon={lon}")
