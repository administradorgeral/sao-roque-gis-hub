import urllib.request
import urllib.parse
import json

queries = [
    'Vila Don Patto, Sao Roque',
    'Estrada do Vinho, Sao Roque',
    'Taxaquara, Sao Roque',
    'Taxaquara Golf Club',
    'NOR Hotel Sao Roque',
    'NÓR Hotel & Spa, São Roque',
    'Hotel & Spa São Roque',
    'Estrada do Vinho 2500, São Roque',
    'Estrada Taxaquara, São Roque'
]

for q in queries:
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(q)}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'SaoRoqueGIS/1.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data:
                print(f"FOUND: {q}")
                print(f"  Lat: {data[0]['lat']}, Lon: {data[0]['lon']}")
                print(f"  Name: {data[0]['display_name'][:80]}")
            else:
                print(f"NOT FOUND: {q}")
    except Exception as e:
        print(f"ERROR: {q} -> {e}")
