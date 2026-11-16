from PIL import Image
import numpy as np
import cv2

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png")
arr = np.array(img.convert('RGB'))

# Find red mask (urban dots)
red_mask = ((arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)).astype(np.uint8) * 255

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask)
print(f"Total red components: {num_labels - 1}")

# Let's find key components:
# 1. Westernmost red dot of Vargem Grande Paulista:
# In the image, Vargem Grande is around x in [500, 600], y in [1050, 1250]
vg_dots = []
cotia_dots = []

for i in range(1, num_labels):
    cx, cy = centroids[i]
    area = stats[i, cv2.CC_STAT_AREA]
    if area < 3:
        continue
    if 500 <= cx <= 600 and 1100 <= cy <= 1250:
        vg_dots.append((cx, cy, area))
    if 600 <= cx <= 750 and 1100 <= cy <= 1250:
        cotia_dots.append((cx, cy, area))

vg_dots.sort(key=lambda d: d[0])
cotia_dots.sort(key=lambda d: d[0])

print(f"Vargem Grande dots: {vg_dots[:5]}")
print(f"Cotia dots: {cotia_dots[:5]}")
