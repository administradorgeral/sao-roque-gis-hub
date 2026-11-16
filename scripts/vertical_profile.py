from PIL import Image
import numpy as np

crop = Image.open('data/user_crop_cotia.png')
arr = np.array(crop)

# Let's inspect along a vertical line at X = 205 (where we found a red dot at Y = 130)
print("Vertical line at X = 205:")
for y in range(40, 150):
    r, g, b = arr[y, 205, :3]
    # Check if this pixel is on the orange highway line
    # Orange highway: R is high (~240-255), G is medium (~140-180), B is low (~50-100)
    # Background is yellowish/orange due to layer opacity
    if r > 200 and 120 < g < 185 and b < 100:
        print(f"  y={y}: RGB=({r:3d}, {g:3d}, {b:3d}) [Possible Orange Line]")
    elif r > 200 and g < 100 and b < 100:
        print(f"  y={y}: RGB=({r:3d}, {g:3d}, {b:3d}) [RED DOT]")
