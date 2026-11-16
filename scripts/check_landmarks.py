import numpy as np
from PIL import Image

img = Image.open('data/rbcv_cinturao_verde_regional.png')
print("Image size:", img.size)

# Width = 2222, Height = 2946
# Formula in process_rbcv_exact.py:
# x_min = 31.201 pt, x_max = 564.493 pt -> delta_x = 533.292 pt
# y_min = 33.079 pt, y_max = 740.201 pt -> delta_y = 707.122 pt
# scale = 300 / 72 = 4.16666667
# x_pixels = round(delta_x * scale) = 2222
# y_pixels = round(delta_y * scale) = 2946

# Our Leaflet bounds were:
# lat_min = -25.36436, lat_max = -22.44755
# lon_min = -47.52275, lon_max = -45.32279

# Under this formula, any pixel (px, py) in the image maps to:
def pixel_to_geo(px, py):
    lon = -47.52275 + (px / 2222.0) * (-45.32279 - (-47.52275))
    lat = -22.44755 - (py / 2946.0) * (-22.44755 - (-25.36436))
    return lon, lat

def geo_to_pixel(lon, lat):
    px = (lon - (-47.52275)) / (-45.32279 - (-47.52275)) * 2222.0
    py = (lat - (-22.44755)) / (-25.36436 - (-22.44755)) * 2946.0
    return px, py

# Let's test known landmarks:
landmarks = {
    "Praça da Sé (São Paulo)": (-46.6333, -23.5505),
    "Aeroporto de Congonhas": (-46.6565, -23.6261),
    "Pico do Jaraguá": (-46.7667, -23.4583),
    "Cotia Centro": (-46.9189, -23.6039),
    "São Roque Centro": (-47.1353, -23.5325),
    "Santos (Ponta da Praia)": (-46.3000, -23.9850),
    "Ilha Porchat (São Vicente)": (-46.3680, -23.9740)
}

print("\nExpected pixel positions of known landmarks in image:")
for name, (lon, lat) in landmarks.items():
    px, py = geo_to_pixel(lon, lat)
    print(f"  {name:25s}: Lon={lon:.4f}, Lat={lat:.4f} -> Pixel ({px:6.1f}, {py:6.1f})")
