import pypdfium2 as pdfium
import numpy as np
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

print(f"Total tiras: {len(images)}")
for i in range(10):
    b = images[i].get_bounds()
    px = images[i].get_px_size()
    print(f"Tira {i:2d}: bounds Y=[{b[1]:.3f}, {b[3]:.3f}] (H_pt={b[3]-b[1]:.3f}), px_size={px}")

# Verificar se há sobreposição ou espaçamento entre as tiras
print("\nVerificando continuidade entre tiras consecutivas:")
for i in range(len(images)-1):
    b_curr = images[i].get_bounds()
    b_next = images[i+1].get_bounds()
    # Imagem i está acima da imagem i+1?
    # topo da próxima vs base da atual:
    diff = b_curr[1] - b_next[3]
    if abs(diff) > 0.001:
        print(f"Descontinuidade entre {i} e {i+1}: base atual={b_curr[1]:.4f}, topo prox={b_next[3]:.4f}, diff={diff:.4f} pt")

# Agora vamos verificar os pixels das bordas superior e inferior de cada tira
print("\nVerificando pixels nas bordas superior/inferior das tiras 10, 11, 12:")
for idx in [10, 11, 12]:
    bm = images[idx].get_bitmap()
    arr = bm.to_numpy() # shape (H, W, 4)
    # Linha 0 (topo) e Linha -1 (base)
    top_row = arr[0, :, :3]
    bottom_row = arr[-1, :, :3]
    # Quantos pixels não são brancos?
    non_white_top = np.sum(np.any(top_row < 250, axis=1))
    non_white_bottom = np.sum(np.any(bottom_row < 250, axis=1))
    print(f"Tira {idx} (H={arr.shape[0]}): Linha topo tem {non_white_top} px coloridos, Linha base tem {non_white_bottom} px coloridos")
    # Verificar se as linhas de borda têm brancos ou alpha
    print(f"  Linha topo cor média: {np.mean(top_row, axis=0)}, Linha base cor média: {np.mean(bottom_row, axis=0)}")

doc.close()
