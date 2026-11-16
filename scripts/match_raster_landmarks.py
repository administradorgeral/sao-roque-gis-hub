from PIL import Image
import numpy as np
import cv2

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png")
arr = np.array(img.convert('RGB'))

# Find red mask
red_mask = ((arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)).astype(np.uint8) * 255
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask)

# Find all centroids with area >= 4
all_dots = []
for i in range(1, num_labels):
    cx, cy = centroids[i]
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= 4:
        all_dots.append((cx, cy, area))

print(f"Filtered dots: {len(all_dots)}")

# Known Landmarks on OpenStreetMap:
# 1. Cotia Center (Raposo Tavares / Av. Prof. Manoel José Pedroso):
#    Real OSM: Lat = -23.60389, Lon = -46.91889
# 2. Vargem Grande Paulista Center (Praça da Matriz / Raposo Tavares):
#    Real OSM: Lat = -23.60250, Lon = -47.02640
# 3. Barueri Center:
#    Real OSM: Lat = -23.51110, Lon = -46.87610
# 4. Osasco Center:
#    Real OSM: Lat = -23.53250, Lon = -46.79170
# 5. São Paulo Sé (Marco Zero):
#    Real OSM: Lat = -23.55039, Lon = -46.63395
# 6. Guarulhos Center:
#    Real OSM: Lat = -23.46280, Lon = -46.53330
# 7. Santos (Praça Mauá):
#    Real OSM: Lat = -23.93500, Lon = -46.32800

# Let's inspect the dots near each landmark:
landmarks = {
    "Vargem Grande": (-47.02640, -23.60250),
    "Cotia": (-46.91889, -23.60389),
    "Barueri": (-46.87610, -23.51110),
    "Osasco": (-46.79170, -23.53250),
    "São Paulo Sé": (-46.63395, -23.55039),
    "Guarulhos": (-46.53330, -23.46280),
    "Santos": (-46.32800, -23.93500)
}

print("\nRaster dimensions: 2222 x 2946")
