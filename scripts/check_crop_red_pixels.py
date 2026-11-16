from PIL import Image
import numpy as np

img = Image.open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/cotia_crop.png")
arr = np.array(img.convert('RGB'))

# Find red dots: red is dominant (r > 180, g < 80, b < 80)
red_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)
y_indices, x_indices = np.where(red_mask)

print(f"Red pixels found: {len(x_indices)}")
if len(x_indices) > 0:
    print(f"Pixel X range in crop: {x_indices.min()} to {x_indices.max()}")
    print(f"Pixel Y range in crop: {y_indices.min()} to {y_indices.max()}")
    
    # Crop origin in points:
    # x0_pt = 155, y0_pt_top = 485
    # scale = 300 / 72
    scale = 300 / 72
    x_pt_min = 155 + x_indices.min() / scale
    x_pt_max = 155 + x_indices.max() / scale
    y_pt_max = 485 - y_indices.min() / scale
    y_pt_min = 485 - y_indices.max() / scale
    
    print(f"Red dots bounding box in PDF points: x in [{x_pt_min:.2f}, {x_pt_max:.2f}], y in [{y_pt_min:.2f}, {y_pt_max:.2f}]")
    
    # Geographic coordinates under grid ticks:
    lon_min = -47.0 + (x_pt_min - 157.92354) / 242.40544
    lon_max = -47.0 + (x_pt_max - 157.92354) / 242.40544
    lat_min = -24.0 + (y_pt_min - 363.83740) / 242.42817
    lat_max = -24.0 + (y_pt_max - 363.83740) / 242.42817
    
    print(f"Calculated Geographic Coordinates (from PDF grid ticks):")
    print(f"  Lon: {lon_min:.5f} to {lon_max:.5f}")
    print(f"  Lat: {lat_min:.5f} to {lat_max:.5f}")
