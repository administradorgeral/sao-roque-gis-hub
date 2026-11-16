from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\crop_mdt_pdf.png")
arr = np.array(img)

# Amostrar um patch de 300x300 no centro
patch = arr[400:700, 400:700, :3]
patch_img = Image.fromarray(patch)
patch_img.save(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\mdt_patch.png")

# Verificar se as cores mudam bruscamente em linhas horizontais
for y in range(0, 100, 10):
    row = patch[y, 100:150]
    print(f"Linha {y}: RGB média = {np.mean(row, axis=0)}")
