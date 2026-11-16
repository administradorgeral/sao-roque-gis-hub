import math
import numpy as np

# Ground Truth landmarks on OpenStreetMap:
# Format: (name, osm_lon, osm_lat, raster_px_x, raster_px_y)
# Let's find the exact raster pixel for these well-known landmarks!

landmarks = [
    # 1. Cotia Center (Raposo Tavares km 34 / Av. Prof. Manoel José Pedroso):
    ("Cotia", -46.91889, -23.60389, 605.0, 1130.0),
    # 2. Vargem Grande Paulista / Tijuco Preto:
    ("Tijuco Preto", -46.98859, -23.64013, 532.0, 1189.0),
    # 3. Barueri Center:
    ("Barueri", -46.87610, -23.51110, 650.0, 1025.0),
    # 4. Osasco Center:
    ("Osasco", -46.79170, -23.53250, 745.0, 1055.0),
    # 5. São Paulo Sé (Marco Zero):
    ("São Paulo Sé", -46.63395, -23.55039, 905.0, 1080.0),
    # 6. Pico do Jaraguá:
    ("Pico do Jaraguá", -46.76703, -23.45843, 765.0, 975.0),
    # 7. Guarulhos Center:
    ("Guarulhos", -46.53330, -23.46280, 1010.0, 985.0),
    # 8. Santos Praça Mauá (Baixada Santista):
    ("Santos", -46.32800, -23.93500, 1220.0, 1500.0)
]

# Let's verify the raster pixel coordinates in rbcv_cinturao_verde_regional.png!
