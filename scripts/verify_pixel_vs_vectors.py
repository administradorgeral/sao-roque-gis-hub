import pypdfium2 as pdfium
import numpy as np

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa Fragilidade Potencial.pdf')
page = doc[0]

# Render a patch at scale 2.0 (144 dpi)
# In PDF coords: center of map is x: 600..900, y: 700..1000
# In PIL coords: x: 600*2 = 1200..1800, y: (1684-1000)*2 = 1368..1968
pix = page.render(scale=2.0)
img = pix.to_pil()
patch = img.crop((1200, 1368, 1800, 1968))
patch.save('scripts/patch_visible.png')

arr = np.array(patch)
# Find counts of target colors (allowing small tolerance +- 2)
# Colors:
# Dark Green: (0, 97, 0)
# Dark Red: (168, 0, 0)
# Light Green: (122, 171, 0)
# Yellow: (255, 255, 0)
# Bright Red: (255, 0, 0)

targets = {
    'Muito Fraca (#006100)': [0, 97, 0],
    'Muito Forte (#A80000)': [168, 0, 0],
    'Fraca (#7AAB00)': [122, 171, 0],
    'Média (#FFFF00)': [255, 255, 0],
    'Forte (#FF0000)': [255, 0, 0],
}

total_matched = 0
for name, (tr, tg, tb) in targets.items():
    mask = (np.abs(arr[:,:,0] - tr) <= 5) & (np.abs(arr[:,:,1] - tg) <= 5) & (np.abs(arr[:,:,2] - tb) <= 5)
    cnt = np.sum(mask)
    total_matched += cnt
    print(f'{name}: {cnt} pixels')

print(f'Total matched pixels: {total_matched} out of {patch.width * patch.height} ({total_matched/(patch.width*patch.height)*100:.1f}%)')
