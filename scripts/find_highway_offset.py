import numpy as np
from PIL import Image

crop = Image.open('data/user_crop_cotia.png')
arr = np.array(crop)

# Let's find pixels of the red dots in the white strip:
# Red dots are distinct: R > 180, G < 50, B < 50
red_dots = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 50) & (arr[:, :, 2] < 50)
y_red, x_red = np.where(red_dots)

print(f"Red dot pixels in crop: {len(x_red)}")

# Let's find the centers of the red dots in the crop:
# Group adjacent red pixels to get centroids of the red squares:
from scipy.ndimage import label
labeled, num_features = label(red_dots)
print(f"Number of red squares detected: {num_features}")

centroids = []
for i in range(1, num_features + 1):
    ys, xs = np.where(labeled == i)
    if len(xs) > 5: # significant square
        centroids.append((xs.mean(), ys.mean()))

# Sort centroids by X (west to east)
centroids.sort(key=lambda c: c[0])
print("\nRed square centroids (x, y) relative to crop (400, 150):")
for c in centroids:
    print(f"  Absolute in screenshot: ({400 + c[0]:.1f}, {150 + c[1]:.1f})")

# Let's also find the Orange Raposo Tavares highway line:
# Orange on OSM: around (240-255, 120-170, 40-90)
# Let's inspect RGB values along vertical slices above the red squares:
print("\nSampling colors above the red squares to find the orange highway line:")
for c in centroids[1:5]:
    cx = int(c[0])
    cy = int(c[1])
    # Search upwards from cy for orange line (look up to 100 pixels above)
    found_y = None
    for y_test in range(cy - 10, max(0, cy - 120), -1):
        r, g, b = arr[y_test, cx, :3]
        # Orange highway color check
        if r > 210 and 90 < g < 180 and b < 80:
            found_y = y_test
            print(f"  Above red square at ({400+cx}, {150+cy}): orange line at ({400+cx}, {150+found_y}), diff_Y = {cy - found_y} px, color=({r},{g},{b})")
            break
