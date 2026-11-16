import numpy as np

x_pts = np.array([103.443, 386.890, 670.337, 953.785, 1237.232, 1520.680])
utm_x = np.array([275000.0, 280000.0, 285000.0, 290000.0, 295000.0, 300000.0])

y_pts = np.array([241.163, 524.593, 808.023, 1091.452, 1375.122])
utm_y = np.array([7385000.0, 7390000.0, 7395000.0, 7400000.0, 7405000.0])

poly_x = np.polyfit(x_pts, utm_x, 1)
pred_x = poly_x[0] * x_pts + poly_x[1]
res_x = np.abs(utm_x - pred_x)

poly_y = np.polyfit(y_pts, utm_y, 1)
pred_y = poly_y[0] * y_pts + poly_y[1]
res_y = np.abs(utm_y - pred_y)

print(f"X Affine: slope={poly_x[0]:.6f}, intercept={poly_x[1]:.2f}")
print(f"X Max residual: {np.max(res_x):.4f} meters, RMS: {np.sqrt(np.mean(res_x**2)):.4f} meters")

print(f"Y Affine: slope={poly_y[0]:.6f}, intercept={poly_y[1]:.2f}")
print(f"Y Max residual: {np.max(res_y):.4f} meters, RMS: {np.sqrt(np.mean(res_y**2)):.4f} meters")
