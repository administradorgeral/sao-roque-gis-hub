import numpy as np

# Ground truth UTM grid points
x_pts = np.array([202.57, 429.37, 656.18, 882.98, 1109.79, 1336.59, 1563.40])
x_utm = np.array([276000.0, 280000.0, 284000.0, 288000.0, 292000.0, 296000.0, 300000.0])

y_pts = np.array([206.12, 489.55, 773.22, 1056.65, 1340.08])
y_utm = np.array([7385000.0, 7390000.0, 7395000.0, 7400000.0, 7405000.0])

# Linear regression
slope_x, intercept_x = np.polyfit(x_pts, x_utm, 1)
pred_x = slope_x * x_pts + intercept_x
res_x = np.abs(pred_x - x_utm)

slope_y, intercept_y = np.polyfit(y_pts, y_utm, 1)
pred_y = slope_y * y_pts + intercept_y
res_y = np.abs(pred_y - y_utm)

print(f"X Affine: UTM_X = {slope_x:.6f} * X_pt + {intercept_x:.2f}")
print(f"Max residual X: {np.max(res_x):.4f} m ({np.max(res_x)*1000:.1f} mm)")

print(f"\nY Affine: UTM_Y = {slope_y:.6f} * Y_pt + {intercept_y:.2f}")
print(f"Max residual Y: {np.max(res_y):.4f} m ({np.max(res_y)*1000:.1f} mm)")
