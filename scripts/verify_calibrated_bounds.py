import math

# Current bounds in js/layers/rbcv_cinturao_verde.js:
# rasterBounds: [[-25.35882, -47.54622], [-22.44569, -45.31257]]

# Required shift:
# In Image 2, Cotia highway strip is at Lat ~ -23.618, should be at -23.6035 -> d_lat = +0.0145
# Cotia strip is at Lon ~ -46.930, should be at -46.942 -> d_lon = -0.0120

# Let's test a range of fine-tuned shifts and check landmarks:
current_sw_lat = -25.35882
current_sw_lon = -47.54622
current_ne_lat = -22.44569
current_ne_lon = -45.31257

d_lat = +0.0145
d_lon = -0.0125

new_sw_lat = current_sw_lat + d_lat
new_ne_lat = current_ne_lat + d_lat
new_sw_lon = current_sw_lon + d_lon
new_ne_lon = current_ne_lon + d_lon

print("Optimal Calibrated rasterBounds:")
print(f"  [[{new_sw_lat:.5f}, {new_sw_lon:.5f}], [{new_ne_lat:.5f}, {new_ne_lon:.5f}]]")

# Let's verify Leaflet projection:
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

sw_x, sw_y = project_mercator(new_sw_lat, new_sw_lon)
ne_x, ne_y = project_mercator(new_ne_lat, new_ne_lon)

def pt(px_x, px_y):
    mx = sw_x + (px_x / 2222.0) * (ne_x - sw_x)
    my = ne_y - (px_y / 2946.0) * (ne_y - sw_y)
    return unproject_mercator(mx, my)

# Check Cotia strip center (px = 610, py = 1112):
lat_cotia, lon_cotia = pt(610, 1112)
print(f"\nCotia strip center on Raposo Tavares:")
print(f"  Placed: Lat={lat_cotia:.5f}, Lon={lon_cotia:.5f}")
print(f"  Target: Lat=-23.60350, Lon=-46.94000")

# Check Vargem Grande dot (px = 532, py = 1189):
lat_vg, lon_vg = pt(532, 1189)
print(f"\nVargem Grande dot:")
print(f"  Placed: Lat={lat_vg:.5f}, Lon={lon_vg:.5f}")
print(f"  Target: Lat=-23.61400, Lon=-47.02500")

# Check Osasco center (px = 745, py = 1055):
lat_os, lon_os = pt(745, 1055)
print(f"\nOsasco center:")
print(f"  Placed: Lat={lat_os:.5f}, Lon={lon_os:.5f}")
print(f"  Target: Lat=-23.53250, Lon=-46.79170")

# Check Pico do Jaraguá (px = 764, py = 1026):
lat_jar, lon_jar = pt(764, 1026)
print(f"\nPico do Jaraguá:")
print(f"  Placed: Lat={lat_jar:.5f}, Lon={lon_jar:.5f}")
print(f"  Target: Lat=-23.45840, Lon=-46.76700")

# Check São Paulo Sé (px = 905, py = 1080):
lat_se, lon_se = pt(905, 1080)
print(f"\nSão Paulo Sé:")
print(f"  Placed: Lat={lat_se:.5f}, Lon={lon_se:.5f}")
print(f"  Target: Lat=-23.55040, Lon=-46.63400")
