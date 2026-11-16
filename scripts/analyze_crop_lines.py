import numpy as np
from PIL import Image

img = Image.open(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\crop_mdt_pdf.png")
arr = np.array(img)
print("Crop shape:", arr.shape)

# Verificar se há linhas horizontais (scanlines) na renderização nativa do PDF
# Calcular a variância ou diferença linha a linha
diffs = []
for y in range(arr.shape[0]-1):
    row_curr = arr[y, :, :3].astype(float)
    row_next = arr[y+1, :, :3].astype(float)
    d = np.mean(np.abs(row_curr - row_next))
    diffs.append(d)

print(f"Média das diferenças linha-a-linha: {np.mean(diffs):.2f}")
print(f"Máxima diferença linha-a-linha: {np.max(diffs):.2f}")

# Contar quantas linhas têm pico de descontinuidade
threshold = 15.0
spikes = [i for i, d in enumerate(diffs) if d > threshold]
print(f"Picos de descontinuidade (> {threshold}): {len(spikes)} em {arr.shape[0]} linhas")
for s in spikes[:10]:
    print(f"  Pico na linha Y={s}: diff={diffs[s]:.2f}")
