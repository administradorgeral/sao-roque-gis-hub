from PIL import Image
import numpy as np
import cv2

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png")
arr = np.array(img.convert('RGB'))

# Find red mask
red_mask = ((arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)).astype(np.uint8) * 255
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(red_mask)

# Find all dots near x in [450, 750] and y in [1000, 1300]:
dots = []
for i in range(1, num_labels):
    cx, cy = centroids[i]
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= 3 and 450 <= cx <= 750 and 1000 <= cy <= 1300:
        dots.append((cx, cy, area))

print(f"Dots found in Cotia/VG region: {len(dots)}")
# Print with py sorted
dots.sort(key=lambda d: d[1])
for d in dots:
    print(f"px_x={d[0]:.1f}, px_y={d[1]:.1f}, area={d[2]}")
