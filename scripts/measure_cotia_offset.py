import numpy as np
from PIL import Image

img_cotia = Image.open('data/inspect_cotia.png')
arr = np.array(img_cotia)

# Find red dots in crop_cotia
red_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 70) & (arr[:, :, 2] < 70)
y_red, x_red = np.where(red_mask)

# Also find white pixels (mancha urbana background)
white_mask = (arr[:, :, 0] > 240) & (arr[:, :, 1] > 240) & (arr[:, :, 2] > 240)
y_white, x_white = np.where(white_mask)

print(f"Red pixels in Cotia crop: {len(x_red)}")
print(f"White pixels in Cotia crop: {len(x_white)}")

# The expected Cotia center was at relative pixel (110, 118)
print(f"Expected Cotia center relative pixel: (109.9, 117.9)")

# What is the actual center of the Cotia white/red patch?
# Let's cluster or look at the western patch (Cotia) vs eastern patch (Carapicuíba / Osasco)
# In this 250x250 crop (x from 500 to 750):
# X < 180 is the Cotia patch!
cotia_patch = (x_white < 180)
if np.any(cotia_patch):
    cx_actual = x_white[cotia_patch].mean()
    cy_actual = y_white[cotia_patch].mean()
    print(f"Actual Cotia white patch center relative: ({cx_actual:.1f}, {cy_actual:.1f})")
    print(f"Absolute in image: ({500 + cx_actual:.1f}, {1050 + cy_actual:.1f})")
    print(f"Delta: dX = {cx_actual - 109.9:.1f} px, dY = {cy_actual - 117.9:.1f} px")
