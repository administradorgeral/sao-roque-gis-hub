from PIL import Image
import numpy as np

img = Image.open('data/rbcv_cinturao_verde_regional.png')
# Crop around Cotia: X from 550 to 700, Y from 1130 to 1250
crop_real_cotia = img.crop((550, 1130, 700, 1250))
crop_real_cotia.save('data/crop_real_cotia.png')

arr = np.array(crop_real_cotia)
# Find white pixels (mancha urbana) and red pixels
red_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 70) & (arr[:, :, 2] < 70)
white_mask = (arr[:, :, 0] > 230) & (arr[:, :, 1] > 230) & (arr[:, :, 2] > 230)

y_red, x_red = np.where(red_mask)
y_white, x_white = np.where(white_mask)

print(f"In real Cotia window (X 550-700, Y 1130-1250):")
print(f"  Red pixels: {len(x_red)}")
print(f"  White pixels: {len(x_white)}")

if len(x_red) > 0:
    mean_x_abs = 550 + x_red.mean()
    mean_y_abs = 1130 + y_red.mean()
    print(f"  Red dots centroid in image: ({mean_x_abs:.1f}, {mean_y_abs:.1f})")
    
    # What (lat, lon) does this map to under current rasterBounds:
    # rasterBounds: [[-25.36436, -47.52275], [-22.44755, -45.32279]]
    cur_lon = -47.52275 + (mean_x_abs / 2222.0) * (-45.32279 - (-47.52275))
    cur_lat = -22.44755 - (mean_y_abs / 2946.0) * (-22.44755 - (-25.36436))
    print(f"  Maps to: Lat={cur_lat:.5f}, Lon={cur_lon:.5f}")
    print(f"  Real Cotia: Lat=-23.60390, Lon=-46.91890")
    print(f"  Error: Delta Lat = {cur_lat - (-23.60390):+.5f} deg, Delta Lon = {cur_lon - (-46.91890):+.5f} deg")
