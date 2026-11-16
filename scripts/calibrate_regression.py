import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

# Vamos achar os cruzamentos de grid no interior do mapa (cruzes de grid de 5km em 5km)
# No ArcMap, o grid de 5km costuma ter cruzes ou linhas inteiras com cor cinza ou preta
grid_crosses = []
for p in path_objs:
    b = p.get_bounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    # Se for uma cruzeta pequena (w entre 4 e 15 pt, h entre 4 e 15 pt)
    if 4 < w < 15 and 4 < h < 15 and b[0] < 1650:
        grid_crosses.append(((b[0]+b[2])/2, (b[1]+b[3])/2))

print(f"Cruzetas de grid encontradas: {len(grid_crosses)}")
for c in sorted(grid_crosses)[:15]:
    print(f"  Grid cross: X={c[0]:.2f}, Y={c[1]:.2f}")

# E as coordenadas dos textos UTM:
# Vamos usar os centros dos textos das coordenadas Y e X para calcular a regressão linear
# Y: 7385000, 7390000, 7395000, 7400000, 7405000, 7410000
# X: 270000, 275000, 280000, 285000, 290000, 295000
import numpy as np

# Posições dos textos no eixo X:
# "270000" começa em 28.77
# "275000" começa em 312.22
# "280000" começa em 595.91
# "285000" começa em 879.37
# "290000" começa em 1162.82
# "295000" começa em 1446.27
x_pdf = np.array([28.77, 312.22, 595.91, 879.37, 1162.82, 1446.27])
x_utm = np.array([270000.0, 275000.0, 280000.0, 285000.0, 290000.0, 295000.0])

slope_x, intercept_x = np.polyfit(x_pdf, x_utm, 1)
print(f"\nRegressão X: UTM_X = {slope_x:.6f} * PDF_X + {intercept_x:.2f}")
print(f"  Erro máximo em X: {np.max(np.abs(x_utm - (slope_x * x_pdf + intercept_x))):.4f} metros")

# Posições dos textos no eixo Y:
y_pdf = np.array([205.49, 488.92, 772.35, 1055.77, 1339.20, 1622.87])
y_utm = np.array([7385000.0, 7390000.0, 7395000.0, 7400000.0, 7405000.0, 7410000.0])

slope_y, intercept_y = np.polyfit(y_pdf, y_utm, 1)
print(f"\nRegressão Y: UTM_Y = {slope_y:.6f} * PDF_Y + {intercept_y:.2f}")
print(f"  Erro máximo em Y: {np.max(np.abs(y_utm - (slope_y * y_pdf + intercept_y))):.4f} metros")

doc.close()
