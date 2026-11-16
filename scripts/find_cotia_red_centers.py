from PIL import Image
import numpy as np
import cv2

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/cotia_crop.png")
arr = np.array(img.convert('RGB'))

# Find red mask
red_mask = ((arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)).astype(np.uint8) * 255

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask)
print(f"Total red components: {num_labels - 1}")

scale = 300 / 72
dots_geo = []

for i in range(1, num_labels):
    cx, cy = centroids[i]
    area = stats[i, cv2.CC_STAT_AREA]
    if area < 2:  # ignore 1-pixel noise
        continue
    x_pt = 155 + cx / scale
    y_pt = 485 - cy / scale
    lon = -47.0 + (x_pt - 157.92354) / 242.40544
    lat = -24.0 + (y_pt - 363.83740) / 242.42817
    dots_geo.append((lon, lat, cx, cy, x_pt, y_pt, area))

dots_geo.sort(key=lambda d: d[0])

print("Westernmost 15 red dots near Cotia / Vargem Grande (lon, lat):")
for d in dots_geo[:15]:
    print(f"Lon: {d[0]:.5f}, Lat: {d[1]:.5f} (area: {d[6]} px)")
