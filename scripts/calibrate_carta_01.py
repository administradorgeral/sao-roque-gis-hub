import numpy as np

# Ground Control Points: (x_pt, y_pt) on PDF Page vs (lon, lat) on OSM WGS84
# Let's inspect the exact coordinate correlation:

# Points:
# 1. Brasital / Centro:
#    PDF pt: (752.4, 843.9)
#    WGS84: (-47.1354, -23.5305)
# 2. Canguera:
#    PDF pt: (557.6, 404.3)
#    WGS84: (-47.1320, -23.6080)
# 3. São João Novo:
#    PDF pt: (1274.3, 839.1)
#    WGS84: (-47.0040, -23.5780)
# 4. Morro do Saboó:
#    PDF pt: (634.0, 1295.8)
#    WGS84: (-47.0910, -23.4860)

pts_pdf = np.array([
    [752.4, 843.9, 1.0],
    [557.6, 404.3, 1.0],
    [1274.3, 839.1, 1.0],
    [634.0, 1295.8, 1.0]
])

lons = np.array([-47.1354, -47.1320, -47.0040, -47.0910])
lats = np.array([-23.5305, -23.6080, -23.5780, -23.4860])

# Least squares fit: lon = A * x + B * y + C, lat = D * x + E * y + F
coeff_lon, _, _, _ = np.linalg.lstsq(pts_pdf, lons, rcond=None)
coeff_lat, _, _, _ = np.linalg.lstsq(pts_pdf, lats, rcond=None)

print(f"Affine Lon: {coeff_lon[0]:.8f} * x + {coeff_lon[1]:.8f} * y + {coeff_lon[2]:.8f}")
print(f"Affine Lat: {coeff_lat[0]:.8f} * x + {coeff_lat[1]:.8f} * y + {coeff_lat[2]:.8f}")

# Check residual errors on the points:
for i, name in enumerate(["Brasital", "Canguera", "São João Novo", "Saboó"]):
    x, y, _ = pts_pdf[i]
    pred_lon = coeff_lon[0] * x + coeff_lon[1] * y + coeff_lon[2]
    pred_lat = coeff_lat[0] * x + coeff_lat[1] * y + coeff_lat[2]
    d_lon = pred_lon - lons[i]
    d_lat = pred_lat - lats[i]
    err_m = np.sqrt((d_lat * 110800)**2 + (d_lon * 102000)**2)
    print(f"  {name}: err = {err_m:.1f} m (d_lat={d_lat:+.5f}, d_lon={d_lon:+.5f})")
