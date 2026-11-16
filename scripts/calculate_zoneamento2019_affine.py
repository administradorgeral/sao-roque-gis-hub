import numpy as np

x_pts = np.array([216.49, 499.93, 783.38, 1066.83, 1350.28, 1633.96])
x_utm = np.array([275000.0, 280000.0, 285000.0, 290000.0, 295000.0, 300000.0])

y_pts = np.array([194.60, 478.03, 761.46, 1044.89, 1328.32, 1611.99])
y_utm = np.array([7385000.0, 7390000.0, 7395000.0, 7400000.0, 7405000.0, 7410000.0])

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
