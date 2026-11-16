from PIL import Image
import numpy as np

img = Image.open('data/rbcv_cinturao_verde_regional.png')
arr = np.array(img)

# Extended GCP candidates:
# Let's inspect Santos / Ilha Porchat:
# Ilha Porchat is a rocky hill peninsula extending into the bay of Santos/São Vicente:
# Real WGS84: Lon = -46.3680, Lat = -23.9740
# In check_landmarks.py earlier:
# In crop_santos (1100 to 1300, 1450 to 1650), we found the black line / coast at:
# abs X = 1166, abs Y = 1545

# Guarulhos Airport (Cumbica):
# Real WGS84: Lon = -46.4731, Lat = -23.4356
# Let's search around X: 950 to 1100, Y: 950 to 1050

# São Paulo Sé / Historic Center:
# Real WGS84: Lon = -46.6333, Lat = -23.5505
# Let's search around X: 850 to 950, Y: 1080 to 1150

candidates = [
    ("São Roque", -47.1353, -23.5325, 380, 440, 1080, 1140),
    ("Vargem Grande", -47.0264, -23.6025, 480, 560, 1150, 1220),
    ("Cotia", -46.9189, -23.6039, 580, 680, 1140, 1220),
    ("Itapevi", -46.9328, -23.5489, 570, 640, 1090, 1150),
    ("Jandira", -46.9028, -23.5275, 610, 670, 1070, 1120),
    ("Barueri", -46.8761, -23.5111, 640, 710, 1050, 1100),
    ("Osasco", -46.7917, -23.5325, 730, 810, 1070, 1130),
    ("São Paulo (Sé)", -46.6333, -23.5505, 870, 930, 1090, 1140),
    ("Guarulhos", -46.5333, -23.4628, 970, 1050, 1010, 1060),
    ("Santos (Ilha Porchat)", -46.3680, -23.9740, 1150, 1185, 1535, 1555)
]

gcps = []
print("Extended GCP detection:")
for name, real_lon, real_lat, x0, x1, y0, y1 in candidates:
    sub = arr[y0:y1, x0:x1]
    # for Ilha Porchat, find the black line or tip of land
    if "Ilha Porchat" in name:
        # Land is white/colored, ocean is grey/blue
        # Let's use the tip:
        px = 1166.0
        py = 1545.0
        gcps.append((px, py, real_lon, real_lat))
        print(f"  {name:22s}: Image Pixel=({px:6.1f}, {py:6.1f}) | Real=(Lon={real_lon:.4f}, Lat={real_lat:.4f}) [Coast Tip]")
        continue

    red = (sub[:, :, 0] > 180) & (sub[:, :, 1] < 70) & (sub[:, :, 2] < 70)
    ys, xs = np.where(red)
    if len(xs) > 0:
        px = x0 + xs.mean()
        py = y0 + ys.mean()
        print(f"  {name:22s}: Image Pixel=({px:6.1f}, {py:6.1f}) | Real=(Lon={real_lon:.4f}, Lat={real_lat:.4f}) | {len(xs)} red px")
        gcps.append((px, py, real_lon, real_lat))

pxs = np.array([g[0] for g in gcps])
pys = np.array([g[1] for g in gcps])
lons = np.array([g[2] for g in gcps])
lats = np.array([g[3] for g in gcps])

M_lon = np.vstack([pxs, np.ones(len(pxs))]).T
A, B = np.linalg.lstsq(M_lon, lons, rcond=None)[0]

M_lat = np.vstack([pys, np.ones(len(pys))]).T
C, D = np.linalg.lstsq(M_lat, lats, rcond=None)[0]

print("\n=== REGIONAL LEAST SQUARES OPTIMAL CALIBRATION ===")
print(f"  Lon = {A:.8f} * px + ({B:.8f})")
print(f"  Lat = {C:.8f} * py + ({D:.8f})")

# Image bounds (width 2222, height 2946):
opt_lon_min = A * 0.0 + B
opt_lon_max = A * 2222.0 + B
opt_lat_max = C * 0.0 + D
opt_lat_min = C * 2946.0 + D

print(f"\nOPTIMAL CALIBRATED LEAFLET BOUNDS:")
print(f"  rasterBounds: [[{opt_lat_min:.5f}, {opt_lon_min:.5f}], [{opt_lat_max:.5f}, {opt_lon_max:.5f}]]")

print("\nResiduals (Meters):")
for name, real_lon, real_lat, *rest in candidates:
    for g in gcps:
        if abs(g[2] - real_lon) < 0.001 and abs(g[3] - real_lat) < 0.001:
            pred_lon = A * g[0] + B
            pred_lat = C * g[1] + D
            err_m_x = (pred_lon - real_lon) * 102100
            err_m_y = (pred_lat - real_lat) * 110800
            dist = (err_m_x**2 + err_m_y**2)**0.5
            print(f"  {name:22s}: Err X = {err_m_x:+6.0f} m, Err Y = {err_m_y:+6.0f} m | Total = {dist:5.0f} m")
