from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\renders_png\debug_title_block.png")
arr = np.array(img.convert('RGB'))

# Find colored boxes / swatches in this crop:
# Count colors that are not white (255, 255, 255) and not black (0, 0, 0)
colors = {}
for y in range(0, arr.shape[0], 5):
    for x in range(0, arr.shape[1], 5):
        c = tuple(arr[y, x])
        if c not in [(255, 255, 255), (0, 0, 0)]:
            colors[c] = colors.get(c, 0) + 1

print("Colors in title block area:")
for c, cnt in sorted(colors.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  RGB{c} (#{c[0]:02X}{c[1]:02X}{c[2]:02X}): {cnt}")
