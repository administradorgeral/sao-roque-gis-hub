# Let's calculate the required shift (d_lat, d_lon) to align the overlay with OpenStreetMap
#
# Ground Truth in OSM:
# 1. Cotia Center (Praça da Matriz / Raposo Tavares km 34):
#    osm_lat = -23.6039, osm_lon = -46.9189
# 2. Vargem Grande Paulista Center (Raposo Tavares km 44):
#    osm_lat = -23.6025, osm_lon = -47.0264
# 3. São Roque Center:
#    osm_lat = -23.5325, osm_lon = -47.1353
# 4. Barueri Center:
#    osm_lat = -23.5111, osm_lon = -46.8761
# 5. Osasco Center:
#    osm_lat = -23.5325, osm_lon = -46.7917

# In our current rbcv_cinturao_verde_regional.png:
# Pixel of Cotia white strip center: (625.9, 1123.1)
# Under current rasterBounds = [[-25.36436, -47.52275], [-22.44755, -45.32279]]:
lon_current = -47.52275 + (625.9 / 2222.0) * (-45.32279 - (-47.52275))
lat_current = -22.44755 - (1123.1 / 2946.0) * (-22.44755 - (-25.36436))

print(f"Current mapped position of Cotia patch in overlay:")
print(f"  Lat: {lat_current:.5f}, Lon: {lon_current:.5f}")
print(f"Real Cotia on OSM:")
print(f"  Lat: -23.60390, Lon: -46.91890")

# Offset:
# Real - Current:
d_lat = -23.60390 - lat_current
d_lon = -46.91890 - lon_current

print(f"\nRequired Shift to match Cotia exactly:")
print(f"  d_lat: {d_lat:+.5f} degrees (~{d_lat * 110800:+.0f} meters) [positive means NORTH / UP]")
print(f"  d_lon: {d_lon:+.5f} degrees (~{d_lon * 111320 * 0.916:+.0f} meters) [positive means EAST / RIGHT, negative means WEST / LEFT]")

# Let's see what the new bounds would be if we apply this shift:
new_lat_min = -25.36436 + d_lat
new_lat_max = -22.44755 + d_lat
new_lon_min = -47.52275 + d_lon
new_lon_max = -45.32279 + d_lon

print(f"\nAdjusted rasterBounds:")
print(f"  [[{new_lat_min:.5f}, {new_lon_min:.5f}], [{new_lat_max:.5f}, {new_lon_max:.5f}]]")
