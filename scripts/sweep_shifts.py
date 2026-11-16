import math

# Baseline bounds currently in js/layers/rbcv_cinturao_verde.js:
base_sw_lat = -25.35882
base_sw_lon = -47.54622
base_ne_lat = -22.44569
base_ne_lon = -45.31257

# Let's test a sweep of (d_lat, d_lon) to find the sweet spot:
def project_mercator(lat, lon):
    r = 6378137.0
    x = r * math.radians(lon)
    lat_rad = math.radians(lat)
    y = r * math.log(math.tan(math.pi / 4 + lat_rad / 2))
    return x, y

def unproject_mercator(x, y):
    r = 6378137.0
    lon = math.degrees(x / r)
    lat = math.degrees(2 * math.atan(math.exp(y / r)) - math.pi / 2)
    return lat, lon

# Targets on OSM:
targets = [
    # (name, target_lat, target_lon, px_x, px_y)
    ("Cotia Center (Raposo Tavares)", -23.60389, -46.91889, 616.0, 1162.0),
    ("Vargem Grande Paulista", -23.60250, -47.02640, 507.0, 1164.0),
    ("Osasco Center", -23.53250, -46.79170, 745.0, 1055.0),
    ("Pico do Jaraguá", -23.45840, -46.76700, 764.0, 975.0),
    ("São Paulo Sé", -23.55040, -46.63400, 905.0, 1080.0),
    ("Guarulhos Center", -23.46280, -46.53330, 1010.0, 985.0)
]

print("Testing shifts:")
for d_lat in [0.010, 0.014, 0.018, 0.022]:
    for d_lon in [-0.010, -0.015, -0.020, -0.025]:
        sw_lat = base_sw_lat + d_lat
        ne_lat = base_ne_lat + d_lat
        sw_lon = base_sw_lon + d_lon
        ne_lon = base_ne_lon + d_lon
        
        sw_x, sw_y = project_mercator(sw_lat, sw_lon)
        ne_x, ne_y = project_mercator(ne_lat, ne_lon)
        
        total_err = 0
        for name, t_lat, t_lon, px, py in targets:
            mx = sw_x + (px / 2222.0) * (ne_x - sw_x)
            my = ne_y - (py / 2946.0) * (ne_y - sw_y)
            plat, plon = unproject_mercator(mx, my)
            err_m = math.sqrt(((plat - t_lat) * 110800)**2 + ((plon - t_lon) * 102000)**2)
            total_err += err_m
            
        avg_err = total_err / len(targets)
        print(f"d_lat={d_lat:+.3f}, d_lon={d_lon:+.3f} -> Avg Error: {avg_err:.0f} m")
