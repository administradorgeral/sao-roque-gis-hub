from PIL import Image
import numpy as np

img = Image.open('data/rbcv_cinturao_verde_regional.png')
# São Roque window: X from 400 to 460, Y from 1070 to 1120
crop_sr_real = img.crop((400, 1070, 460, 1120))
crop_sr_real.save('data/crop_sr_real.png')

arr = np.array(crop_sr_real)
red_mask = (arr[:, :, 0] > 180) & (arr[:, :, 1] < 70) & (arr[:, :, 2] < 70)
y_red, x_red = np.where(red_mask)
print(f"Red pixels at real São Roque window (400-460, 1070-1120): {len(x_red)}")
if len(x_red) > 0:
    mean_x = 400 + x_red.mean()
    mean_y = 1070 + y_red.mean()
    print(f"Centroid of real São Roque patch in image: ({mean_x:.1f}, {mean_y:.1f})")
    
    # Under proposed bounds:
    # new_lat_min = -25.35560, new_lat_max = -22.43879
    # new_lon_min = -47.55871, new_lon_max = -45.35875
    lon_sr = -47.55871 + (mean_x / 2222.0) * (-45.35875 - (-47.55871))
    lat_sr = -22.43879 - (mean_y / 2946.0) * (-22.43879 - (-25.35560))
    print(f"Mapped São Roque: Lat={lat_sr:.5f}, Lon={lon_sr:.5f}")
    print(f"Real São Roque:   Lat=-23.53250, Lon=-47.13530")
    print(f"Diff: dLat={lat_sr - (-23.53250):+.5f} ({ (lat_sr - (-23.53250))*110800 :+.0f}m), dLon={lon_sr - (-47.13530):+.5f} ({ (lon_sr - (-47.13530))*102100 :+.0f}m)")
