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

def test_bounds(bounds, name):
    sw_lat, sw_lon = bounds[0]
    ne_lat, ne_lon = bounds[1]
    sw_x, sw_y = project_mercator(sw_lat, sw_lon)
    ne_x, ne_y = project_mercator(ne_lat, ne_lon)
    
    # Cotia pixel in image: px = 605, py = 1130 (or what is Cotia pixel in the 2222x2946 image?)
    # Let's test several pixels:
    # Cotia: px = 605, py = 1130
    # Tijuco Preto: px = 532, py = 1189
    
    def pt(px_x, px_y):
        mx = sw_x + (px_x / 2222.0) * (ne_x - sw_x)
        my = ne_y - (px_y / 2946.0) * (ne_y - sw_y)
        return unproject_mercator(mx, my)
        
    print(f"\n--- {name} ---")
    print(f"Bounds: {bounds}")
    lat_c, lon_c = pt(605, 1130)
    print(f"Cotia dot:        Lat={lat_c:.5f}, Lon={lon_c:.5f}")
    lat_t, lon_t = pt(532, 1189)
    print(f"Tijuco Preto dot: Lat={lat_t:.5f}, Lon={lon_t:.5f}")

# 1. Old original bounds (from grid ticks):
test_bounds([[-25.36436, -47.52275], [-22.44755, -45.32279]], "1. Grid Ticks Bounds (Initial)")

# 2. Previous turn bounds (from reprocess_rbcv_gcp.py):
test_bounds([[-25.35882, -47.54622], [-22.44569, -45.31257]], "2. GCP Reprocessed Bounds (Previous Turn)")
