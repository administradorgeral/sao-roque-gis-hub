from PIL import Image
import numpy as np

img = Image.open('data/rbcv_cinturao_verde_regional.png')
w, h = img.size
print(f"Image dimensions: {w} x {h}")

# In the PDF:
# x goes from 31.20 to 564.49 -> width = 533.29 pt
# y goes from 33.08 to 740.20 -> height = 707.12 pt
# Cotia on map:
# If Cotia is around -46.919 Lon, -23.604 Lat
# Let's find where the red dots are in the image!
arr = np.array(img)

# Red dots: High R, Low G, Low B
# Let's find pixels where R > 200 and G < 50 and B < 50
red_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 70) & (arr[:, :, 2] < 70)
y_indices, x_indices = np.where(red_mask)

print(f"Found {len(x_indices)} red pixels in the regional raster image.")

# Let's filter red pixels in the Cotia region (x in western quarter, y in upper half)
# Width is 2222, Height is 2946.
# x_ratio ~ (-46.92 - lon_min) / (lon_max - lon_min)
# lon_min ~ -47.52, lon_max ~ -45.32 -> span = 2.20 deg
# (-46.92 - (-47.52)) / 2.20 ~ 0.60 / 2.20 ~ 0.27 -> x ~ 0.27 * 2222 ~ 600 px
# lat_min ~ -25.36, lat_max ~ -22.45 -> span = 2.91 deg
# (-23.60 - (-25.36)) / 2.91 ~ 1.76 / 2.91 ~ 0.60 from south
# Since image y is from north (top): (1 - 0.60) * 2946 ~ 0.40 * 2946 ~ 1180 px

cotia_mask = (x_indices > 400) & (x_indices < 800) & (y_indices > 900) & (y_indices < 1400)
cx = x_indices[cotia_mask]
cy = y_indices[cotia_mask]

print(f"Red pixels in Cotia search window (x 400-800, y 900-1400): {len(cx)}")
if len(cx) > 0:
    print(f"  X range: {cx.min()} to {cx.max()}, mean: {cx.mean():.1f}")
    print(f"  Y range: {cy.min()} to {cy.max()}, mean: {cy.mean():.1f}")
