import numpy as np

# Pontos de calibração exatos das linhas de grade #6E6E6E do mapa AHS
pts_x = np.array([43.92, 853.68, 1663.67, 2473.67])
utm_x = np.array([270000.0, 280000.0, 290000.0, 300000.0])

pts_y = np.array([733.51, 1543.52])
utm_y = np.array([7390000.0, 7400000.0])

# Regressão linear X
slope_x, intercept_x = np.polyfit(pts_x, utm_x, 1)
pred_x = slope_x * pts_x + intercept_x
res_x = utm_x - pred_x

print("=== REGRESSÃO AFFINE X (AHS) ===")
print(f"UTM_X = {slope_x:.6f} * X_pt + {intercept_x:.2f}")
for px, ux, rx in zip(pts_x, utm_x, res_x):
    print(f"  X_pt={px:.2f} -> UTM_X={ux:.1f} (Resíduo: {rx*1000:.1f} mm)")

# Regressão linear Y
slope_y, intercept_y = np.polyfit(pts_y, utm_y, 1)
pred_y = slope_y * pts_y + intercept_y
res_y = utm_y - pred_y

print("\n=== REGRESSÃO AFFINE Y (AHS) ===")
print(f"UTM_Y = {slope_y:.6f} * Y_pt + {intercept_y:.2f}")
for py, uy, ry in zip(pts_y, utm_y, res_y):
    print(f"  Y_pt={py:.2f} -> UTM_Y={uy:.1f} (Resíduo: {ry*1000:.1f} mm)")
