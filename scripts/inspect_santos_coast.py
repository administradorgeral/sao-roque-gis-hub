from PIL import Image
import numpy as np

# In check_landmarks.py earlier:
# Santos (Ponta da Praia) expected pixel was (1235.0, 1552.8)
# Ilha Porchat expected pixel was (1166.3, 1541.7)
# In save_inspection_crops.py, we cropped: (1100, 1450, 1300, 1650) -> 200 x 200 px
img_santos = Image.open('data/inspect_santos.png')
arr = np.array(img_santos)

print("Santos crop size:", img_santos.size)
# Let's save an annotated or high-contrast version showing where water meets land
# Water is typically bluish: B > R and B > G, or high B
# Land in RBCV is green (Zonas-Núcleo), orange (Transição), or yellow (Amortecimento)

# Let's find the southern edge of the landmass in this crop (where land ends and ocean begins)
# In crop coordinates (x from 0 to 200, y from 0 to 200)
# Absolute X in image = x + 1100, Absolute Y in image = y + 1450

# Let's inspect along a column at x = 66 (which is absolute X = 1166.3, expected Ilha Porchat):
print("\nVertical slice at x = 66 (expected Ilha Porchat Lon -46.368):")
for y in range(80, 120, 2):
    r, g, b = arr[y, 66, :3]
    print(f"  y_rel={y} (abs Y={1450+y}): RGB=({r:3d}, {g:3d}, {b:3d})")

print("\nVertical slice at x = 135 (expected Ponta da Praia Lon -46.300):")
for y in range(90, 130, 2):
    r, g, b = arr[y, 135, :3]
    print(f"  y_rel={y} (abs Y={1450+y}): RGB=({r:3d}, {g:3d}, {b:3d})")
