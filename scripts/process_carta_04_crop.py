from PIL import Image
import numpy as np
import os

scale = 150 / 72  # 2.0833333333333335 px / pt

# Viewport bounds of Carta 04 (Sede) in PDF points:
# x in [833.36, 1821.80] pt
# y in [244.92, 1609.54] pt

# In image coordinates (image height = 3509 px, corresponding to 1684 pt):
x0 = int(round(833.36 * scale))
x1 = int(round(1821.80 * scale))
y0 = int(round((1684 - 1609.54) * scale))
y1 = int(round((1684 - 244.92) * scale))

print(f"Crop window Carta 04 (Sede): x=[{x0}, {x1}], y=[{y0}, {y1}] (width={x1-x0} px, height={y1-y0} px)")

src_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_04_zoneamento_consolidacao_urbana_sede.png"
dst_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\data\carta_04_sede_mapa.png"

img = Image.open(src_path).convert("RGBA")
cropped = img.crop((x0, y0, x1, y1))

data = np.array(cropped)
r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]

# Background white threshold (r > 238, g > 238, b > 238)
white_mask = (r > 238) & (g > 238) & (b > 238)
data[white_mask, 3] = 0

# Slight edge smoothing
near_white = (r > 230) & (g > 230) & (b > 230) & (~white_mask)
data[near_white, 3] = 100

out_img = Image.fromarray(data, mode="RGBA")
out_img.save(dst_path, optimize=True)

size_mb = os.path.getsize(dst_path) / (1024 * 1024)
print(f"Processado {dst_path}: {out_img.width}x{out_img.height} px, {size_mb:.2f} MB (Transparência aplicada: {np.sum(white_mask)} pixels transparentes)")
