import numpy as np
from PIL import Image

img = Image.open('data/rbcv_cinturao_verde_regional.png')
w, h = img.size
print(f"Regional image size: {w} x {h}")

# In the user screenshot at Cotia:
# The user clearly showed that Cotia's urban patch (white with red dots) is at:
# Lat ~ -23.6186, Lon ~ -46.9266
# While real Cotia center is at:
# Lat = -23.6039, Lon = -46.9189
# Difference at Cotia:
# Delta Lat = -23.6039 - (-23.6186) = +0.0147 deg (North)
# Delta Lon = -46.9189 - (-46.9266) = +0.0077 deg (West)

# Let's inspect São Roque in the image:
# Where is São Roque in the image?
# Expected px ~ 391, py ~ 1096
crop_sr = img.crop((300, 1000, 500, 1200))
crop_sr.save('data/inspect_sao_roque.png')

# In crop_sr, where is the red dot for São Roque?
arr_sr = np.array(crop_sr)
red_sr = (arr_sr[:, :, 0] > 180) & (arr_sr[:, :, 1] < 70) & (arr_sr[:, :, 2] < 70)
ys, xs = np.where(red_sr)
print(f"São Roque search window: found {len(xs)} red pixels")
if len(xs) > 0:
    print(f"  São Roque red patch center relative: ({xs.mean():.1f}, {ys.mean():.1f})")
    print(f"  Absolute in image: ({300 + xs.mean():.1f}, {1000 + ys.mean():.1f})")
