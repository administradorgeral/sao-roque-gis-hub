import json

# Reference bounds of Carta 1 (Macro):
x1_min, x1_max = 329.58, 1512.58
y1_min, y1_max = 142.18, 1573.34
lon_min, lon_max = -47.20889, -46.99093
lat_min, lat_max = -23.65394, -23.41153

def pt_to_wgs84(x1, y1):
    lon = lon_min + ((x1 - x1_min) / (x1_max - x1_min)) * (lon_max - lon_min)
    lat = lat_min + ((y1 - y1_min) / (y1_max - y1_min)) * (lat_max - lat_min)
    return lat, lon

# For each sheet, let's see its drawing viewport in PDF points.
# The drawing viewport in Carta 5, 6, 7 is the neatline/frame or the content area:
# In all sheets, the left boundary is x=134.0 pt and right is x=1820.4 pt
# Bottom boundary is y=73.9 pt and top is y=1609.3 pt.
# But let's check if we want to crop the full map viewport [134.0, 1820.4] x [73.9, 1609.3]
# OR a tight bounding box around the district.

# Notice: If we crop the full map viewport [134.0, 1820.4] x [73.9, 1609.3]:
# Width = 1686.4 pt, Height = 1535.4 pt
# With transparency applied, all white background outside the district becomes 100% transparent!
# That means the user can zoom in on the district and see the detailed high-res vectors/roads/bairros
# seamlessly overlaid on OpenStreetMap without any white rectangle!

sheets = {
    5: {"name": "Maylasky", "code": "maylasky", "dx": -1716.6, "dy": 72.6, "vp": [134.0, 1820.4, 73.9, 1609.3]},
    6: {"name": "Sao Joao Novo", "code": "sao_joao_novo", "dx": -1917.5, "dy": -1419.0, "vp": [134.0, 1820.4, 73.9, 1609.3]},
    7: {"name": "Canguera", "code": "canguera", "dx": 415.5, "dy": -74.6, "vp": [134.0, 1820.4, 73.9, 1609.3]}
}

for num, s in sheets.items():
    vx0, vx1, vy0, vy1 = s["vp"]
    # Convert viewport corners to Carta 1 coordinates:
    # x1 = (x_N - dx) / 2.0
    # y1 = (y_N - dy) / 2.0
    c1_x0 = (vx0 - s["dx"]) / 2.0
    c1_x1 = (vx1 - s["dx"]) / 2.0
    c1_y0 = (vy0 - s["dy"]) / 2.0
    c1_y1 = (vy1 - s["dy"]) / 2.0
    
    lat0, lon0 = pt_to_wgs84(c1_x0, c1_y0)
    lat1, lon1 = pt_to_wgs84(c1_x1, c1_y1)
    
    print(f"=== CARTA {num}: {s['name']} ===")
    print(f"  Viewport PDF pt: x=[{vx0:.1f}, {vx1:.1f}], y=[{vy0:.1f}, {vy1:.1f}]")
    print(f"  Carta 1 equiv:   x=[{c1_x0:.2f}, {c1_x1:.2f}], y=[{c1_y0:.2f}, {c1_y1:.2f}]")
    print(f"  WGS84 Bounds:    [[{lat0:.5f}, {lon0:.5f}], [{lat1:.5f}, {lon1:.5f}]]")
