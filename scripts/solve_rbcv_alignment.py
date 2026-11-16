import numpy as np

# Let's determine the exact affine transformation that aligns the PDF raster / vectors
# with OpenStreetMap ground truth!

# We have Ground Truth on OpenStreetMap:
# 1. Cotia Center (Raposo Tavares km 34 / Praça da Matriz):
#    Lat = -23.60389, Lon = -46.91889
# 2. Vargem Grande Paulista Center (Praça da Matriz / Raposo Tavares km 43):
#    Lat = -23.60250, Lon = -47.02640
# 3. São Roque Praça da Matriz:
#    Lat = -23.53050, Lon = -47.13542
# 4. Barueri Center:
#    Lat = -23.51110, Lon = -46.87610
# 5. Osasco Center:
#    Lat = -23.53250, Lon = -46.79170
# 6. São Paulo Sé (Marco Zero):
#    Lat = -23.55039, Lon = -46.63395
# 7. Guarulhos Center:
#    Lat = -23.46280, Lon = -46.53330
# 8. Santos (Praça Mauá):
#    Lat = -23.93500, Lon = -46.32800
# 9. Pico do Jaraguá (peak):
#    Lat = -23.45843, Lon = -46.76703
# 10. Cantareira (Núcleo Pedra Grande):
#    Lat = -23.43500, Lon = -46.63000

print("Analyzing alignment parameters...")
