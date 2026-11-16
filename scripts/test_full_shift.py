import numpy as np

# Proposed shift to eliminate the remaining offset:
shift_lat = +0.00876
shift_lon = -0.03596

# New bounds:
new_lat_min = -25.36436 + shift_lat # -25.35560
new_lat_max = -22.44755 + shift_lat # -22.43879
new_lon_min = -47.52275 + shift_lon # -47.55871
new_lon_max = -45.32279 + shift_lon # -45.35875

print(f"Proposed new bounds:")
print(f"  [[{new_lat_min:.5f}, {new_lon_min:.5f}], [{new_lat_max:.5f}, {new_lon_max:.5f}]]")

def map_pixel_to_geo(px, py):
    lon = new_lon_min + (px / 2222.0) * (new_lon_max - new_lon_min)
    lat = new_lat_max - (py / 2946.0) * (new_lat_max - new_lat_min)
    return lat, lon

# Landmarks to test:
# 1. Cotia (centroid 646.2, 1176.8)
lat_cotia, lon_cotia = map_pixel_to_geo(646.2, 1176.8)
print(f"\n1. Cotia Patch:")
print(f"   Mapped: Lat={lat_cotia:.5f}, Lon={lon_cotia:.5f}")
print(f"   Real:   Lat=-23.60390, Lon=-46.91890")
print(f"   Diff:   dLat={lat_cotia - (-23.60390):+.5f} deg ({ (lat_cotia - (-23.60390))*110800 :+.0f}m), dLon={lon_cotia - (-46.91890):+.5f} deg ({ (lon_cotia - (-46.91890))*102100 :+.0f}m)")

# 2. São Roque (centroid 375.8, 1095.5)
lat_sr, lon_sr = map_pixel_to_geo(375.8, 1095.5)
print(f"\n2. São Roque Patch:")
print(f"   Mapped: Lat={lat_sr:.5f}, Lon={lon_sr:.5f}")
print(f"   Real:   Lat=-23.53250, Lon=-47.13530")
print(f"   Diff:   dLat={lat_sr - (-23.53250):+.5f} deg ({ (lat_sr - (-23.53250))*110800 :+.0f}m), dLon={lon_sr - (-47.13530):+.5f} deg ({ (lon_sr - (-47.13530))*102100 :+.0f}m)")
