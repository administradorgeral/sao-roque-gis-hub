from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\carta_01_macrozoneamento_municipal.png")
w, h = img.size
print(f"Dimensões do PNG: {w} x {h}")

# The title block is in the bottom right corner:
# In points: x in [1700, 2384], y in [0, 500]
# In image coordinates:
# scale = 150 / 72 = 2.0833
# x_img = x_pt * scale
# y_img = (1684 - y_pt) * scale
# Title block in image:
# x_img in [3540, 4967]
# y_img in [2460, 3509]

tb_crop = img.crop((3400, 2300, 4967, 3509))
tb_crop.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_title_block.png")
print("Salvo: debug_title_block.png")

# Now let's check what is directly above the title block:
# y_img in [1200, 2400], x_img in [3400, 4967]
above_tb_crop = img.crop((3400, 1000, 4967, 2400))
above_tb_crop.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_above_tb.png")
print("Salvo: debug_above_tb.png")

# Check bottom center: x in [1500, 3500], y in [2700, 3509]
bot_mid_crop = img.crop((1500, 2700, 3500, 3509))
bot_mid_crop.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_bot_mid.png")
print("Salvo: debug_bot_mid.png")
