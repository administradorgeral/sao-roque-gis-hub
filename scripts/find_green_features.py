from PIL import Image
import numpy as np
import cv2

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png")
arr = np.array(img.convert('RGB'))
w, h = img.size

# Let's find:
# 1. Pico do Jaraguá green enclave:
# In the original map, Pico do Jaraguá is a green polygon (#38A800) surrounded by yellow/white
# Let's find green pixels: #38A800 is roughly (56, 168, 0)
green_mask = (abs(arr[:, :, 0] - 56) < 25) & (abs(arr[:, :, 1] - 168) < 25) & (abs(arr[:, :, 2] - 0) < 25)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(green_mask.astype(np.uint8))

print(f"Total green components: {num_labels - 1}")
green_patches = []
for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= 20:
        cx, cy = centroids[i]
        green_patches.append((cx, cy, area))

# Let's find Jaraguá (an isolated green patch in the northwest of São Paulo):
# Around x in [700, 850], y in [900, 1050]
jaragua_cands = [p for p in green_patches if 700 <= p[0] <= 850 and 900 <= p[1] <= 1050]
print(f"Jaraguá candidates: {jaragua_cands}")

# Let's find Cantareira (large green patch in north):
cantareira_cands = [p for p in green_patches if 800 <= p[0] <= 1100 and 700 <= p[1] <= 950 and p[2] > 1000]
print(f"Cantareira candidates: {cantareira_cands}")
