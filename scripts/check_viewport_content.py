from PIL import Image
import numpy as np

for num, name in [(5, 'maylasky'), (6, 'sao_joao_novo'), (7, 'canguera')]:
    src = f"C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/scripts/viewport_carta_0{num}.png"
    img = Image.open(src)
    arr = np.array(img.convert("RGB"))
    non_white = (arr[:, :, 0] < 240) | (arr[:, :, 1] < 240) | (arr[:, :, 2] < 240)
    rows = np.any(non_white, axis=1)
    cols = np.any(non_white, axis=0)
    if np.any(rows) and np.any(cols):
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        print(f"Carta {num} ({name}) content in viewport thumb ({img.width}x{img.height}):")
        print(f"  cols: [{cmin}, {cmax}] (width = {cmax - cmin})")
        print(f"  rows: [{rmin}, rmax: {rmax}] (height = {rmax - rmin})")
