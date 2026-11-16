import numpy as np

# X coordinates and UTM Easting
x_pts = np.array([129.123, 346.089, 563.055, 780.020, 996.986, 1213.952, 1430.677, 1647.643])
utm_x = np.array([276000.0, 280000.0, 284000.0, 288000.0, 292000.0, 296000.0, 300000.0, 304000.0])

# Y coordinates and UTM Northing
y_pts = np.array([265.402, 536.592, 807.783, 1078.973, 1349.923])
utm_y = np.array([7385000.0, 7390000.0, 7395000.0, 7400000.0, 7405000.0])

# Linear regression for X
poly_x = np.polyfit(x_pts, utm_x, 1)
pred_x = poly_x[0] * x_pts + poly_x[1]
res_x = np.abs(utm_x - pred_x)

# Linear regression for Y
poly_y = np.polyfit(y_pts, utm_y, 1)
pred_y = poly_y[0] * y_pts + poly_y[1]
res_y = np.abs(utm_y - pred_y)

print(f"X Affine: slope={poly_x[0]:.6f}, intercept={poly_x[1]:.2f}")
print(f"X Max residual: {np.max(res_x):.4f} meters, RMS: {np.sqrt(np.mean(res_x**2)):.4f} meters")

print(f"Y Affine: slope={poly_y[0]:.6f}, intercept={poly_y[1]:.2f}")
print(f"Y Max residual: {np.max(res_y):.4f} meters, RMS: {np.sqrt(np.mean(res_y**2)):.4f} meters")
