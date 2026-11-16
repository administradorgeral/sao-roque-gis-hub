import math

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

# Current bounds in js/layers/rbcv_cinturao_verde.js:
bounds = [[-25.35882, -47.54622], [-22.44569, -45.31257]]
sw_lat, sw_lon = bounds[0]
ne_lat, ne_lon = bounds[1]

sw_x, sw_y = project_mercator(sw_lat, sw_lon)
ne_x, ne_y = project_mercator(ne_lat, ne_lon)

print(f"Mercator Bounds:")
print(f"  SW: x={sw_x:.1f}, y={sw_y:.1f}")
print(f"  NE: x={ne_x:.1f}, y={ne_y:.1f}")

# In Leaflet, an image of (2222, 2946) is stretched linearly between (sw_x, ne_y) and (ne_x, sw_y) in Mercator coordinates!
# Let's verify:
# For pixel (px_x, px_y):
# merc_x = sw_x + (px_x / 2222.0) * (ne_x - sw_x)
# merc_y = ne_y - (px_y / 2946.0) * (ne_y - sw_y)
# Then lat, lon = unproject_mercator(merc_x, merc_y)

def pixel_to_latlon_in_leaflet(px_x, px_y):
    merc_x = sw_x + (px_x / 2222.0) * (ne_x - sw_x)
    merc_y = ne_y - (px_y / 2946.0) * (ne_y - sw_y)
    return unproject_mercator(merc_x, merc_y)

# Let's test key pixels:
# 1. Cotia cluster centroid (605, 1130):
lat_cotia, lon_cotia = pixel_to_latlon_in_leaflet(605, 1130)
print(f"Cotia dot (605, 1130) rendered in Leaflet at:")
print(f"  Lat: {lat_cotia:.5f}, Lon: {lon_cotia:.5f}")

# 2. Vargem Grande dot (532, 1189):
lat_vg, lon_vg = pixel_to_latlon_in_leaflet(532, 1189)
print(f"Vargem Grande dot (532, 1189) rendered in Leaflet at:")
print(f"  Lat: {lat_vg:.5f}, Lon: {lon_vg:.5f}")

# 3. São Paulo Sé centroid:
# Sé is around Lon -46.634. Let's find Sé dot in raster!
