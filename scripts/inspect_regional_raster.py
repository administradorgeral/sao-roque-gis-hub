from PIL import Image
import numpy as np

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/rbcv_cinturao_verde_regional.png")
print("RBCV Regional Raster size:", img.size)
# img.size is (width, height)
w, h = img.size
print(f"Width: {w}, Height: {h}")

# Let's inspect where the Cotia patch is in this image:
# Cotia is roughly 25-30% from the left, and 35-45% from the top.
# Let's crop x in [500, 750], y in [1000, 1300]
crop = img.crop((500, 1000, 750, 1300))
crop.save("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/regional_cotia_crop.png")
print("Saved regional_cotia_crop.png")
