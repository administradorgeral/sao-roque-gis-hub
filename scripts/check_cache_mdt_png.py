from PIL import Image
import numpy as np

img_path = r"C:\Users\admin\Downloads\Mapas São Roque-20261112T033114Z-1-001\Mapas São Roque\scripts\.cache\mdt.png"
img = Image.open(img_path)
print(f"MDT.png: size={img.size}, mode={img.mode}")

arr = np.array(img)
# Verificar se o fundo é transparente (alpha == 0)
if arr.shape[2] == 4:
    alpha = arr[:, :, 3]
    print(f"Pixels transparentes (alpha == 0): {np.sum(alpha == 0):,} ({np.sum(alpha == 0)*100/(arr.shape[0]*arr.shape[1]):.1f}%)")
    print(f"Pixels opacos (alpha == 255): {np.sum(alpha == 255):,} ({np.sum(alpha == 255)*100/(arr.shape[0]*arr.shape[1]):.1f}%)")
