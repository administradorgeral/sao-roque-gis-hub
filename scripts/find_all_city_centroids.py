from PIL import Image
import numpy as np

img = Image.open('data/rbcv_cinturao_verde_regional.png')
arr = np.array(img)
w, h = img.size

# Ground control points:
# Each city has a cluster of red dots / white background in the image:
# 1. Cotia: expected lon=-46.9189, lat=-23.6039
# 2. Vargem Grande Paulista: expected lon=-47.0264, lat=-23.6025
# 3. São Roque: expected lon=-47.1353, lat=-23.5325
# 4. Itapevi: expected lon=-46.9328, lat=-23.5489
# 5. Jandira: expected lon=-46.9028, lat=-23.5275
# 6. Barueri: expected lon=-46.8761, lat=-23.5111
# 7. Osasco: expected lon=-46.7917, lat=-23.5325
# 8. São Paulo (Sé / Central): expected lon=-46.6333, lat=-23.5505

cities = [
    ("Cotia", -46.9189, -23.6039, 580, 680, 1140, 1220),
    ("São Roque", -47.1353, -23.5325, 380, 440, 1080, 1140),
    ("Vargem Grande", -47.0264, -23.6025, 480, 560, 1150, 1220),
    ("Itapevi", -46.9328, -23.5489, 570, 640, 1090, 1150),
    ("Jandira", -46.9028, -23.5275, 610, 670, 1070, 1120),
    ("Barueri", -46.8761, -23.5111, 640, 710, 1050, 1100),
    ("Osasco", -46.7917, -23.5325, 730, 810, 1070, 1130)
]

gcps = []
print("Detected City Centroids in Regional Raster:")
for name, real_lon, real_lat, x0, x1, y0, y1 in cities:
    sub = arr[y0:y1, x0:x1]
    red = (sub[:, :, 0] > 180) & (sub[:, :, 1] < 70) & (sub[:, :, 2] < 70)
    ys, xs = np.where(red)
    if len(xs) > 0:
        px = x0 + xs.mean()
        py = y0 + ys.mean()
        print(f"  {name:15s}: Image Pixel=({px:6.1f}, {py:6.1f}) | Real=(Lon={real_lon:.4f}, Lat={real_lat:.4f}) | {len(xs)} red px")
        gcps.append((px, py, real_lon, real_lat))
    else:
        print(f"  {name:15s}: NO RED PIXELS in search window!")

# Now let's perform Least Squares Regression:
# lon = A * px + B
# lat = C * py + D
pxs = np.array([g[0] for g in gcps])
pys = np.array([g[1] for g in gcps])
lons = np.array([g[2] for g in gcps])
lats = np.array([g[3] for g in gcps])

# Solve for lon: [px, 1] * [A, B]^T = lon
M_lon = np.vstack([pxs, np.ones(len(pxs))]).T
A, B = np.linalg.lstsq(M_lon, lons, rcond=None)[0]

# Solve for lat: [py, 1] * [C, D]^T = lat
M_lat = np.vstack([pys, np.ones(len(pys))]).T
C, D = np.linalg.lstsq(M_lat, lats, rcond=None)[0]

print("\n=== LEAST SQUARES OPTIMAL CALIBRATION ===")
print(f"  Lon = {A:.8f} * px + ({B:.8f})")
print(f"  Lat = {C:.8f} * py + ({D:.8f})")

# Image width = 2222, height = 2946
# Image corners:
# Top-Left: px = 0, py = 0
# Bottom-Right: px = 2222, py = 2946
opt_lon_min = A * 0.0 + B
opt_lon_max = A * 2222.0 + B
opt_lat_max = C * 0.0 + D
opt_lat_min = C * 2946.0 + D

print(f"\nOPTIMAL LEAFLET BOUNDS:")
print(f"  rasterBounds: [[{opt_lat_min:.5f}, {opt_lon_min:.5f}], [{opt_lat_max:.5f}, {opt_lon_max:.5f}]]")

print("\nResiduals for each ground control point:")
for name, real_lon, real_lat, x0, x1, y0, y1 in cities:
    # find in gcps
    for g in gcps:
        if abs(g[2] - real_lon) < 0.001 and abs(g[3] - real_lat) < 0.001:
            pred_lon = A * g[0] + B
            pred_lat = C * g[1] + D
            err_m_x = (pred_lon - real_lon) * 102100
            err_m_y = (pred_lat - real_lat) * 110800
            dist = (err_m_x**2 + err_m_y**2)**0.5
            print(f"  {name:15s}: Error X = {err_m_x:+6.0f} m, Error Y = {err_m_y:+6.0f} m -> Total = {dist:5.0f} m")
