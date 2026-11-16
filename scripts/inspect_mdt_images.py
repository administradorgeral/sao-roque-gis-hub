import pypdfium2 as pdfium
from collections import Counter
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

print(f"Total de imagens no MDT: {len(images)}")
print(f"Dimensões imagem 0: {images[0].get_px_size()}, bounds={images[0].get_bounds()}")
print(f"Dimensões imagem 45: {images[45].get_px_size()}, bounds={images[45].get_bounds()}")
print(f"Dimensões imagem 92: {images[92].get_px_size()}, bounds={images[92].get_bounds()}")

# Extrair cores da imagem 45 (faixa central do município)
bm = images[45].get_bitmap()
pil_img = bm.to_pil()
colors = pil_img.getcolors(maxcolors=1000)
print(f"\nCores na imagem 45 (centro de São Roque):")
if colors:
    for cnt, col in sorted(colors, key=lambda x: -x[0])[:10]:
        print(f"  RGB {col}: {cnt} px ({cnt*100/(pil_img.size[0]*pil_img.size[1]):.1f}%)")

# Vamos ver as classes da legenda no texto:
# 630 - 760 m
# 760 - 830 m
# 830 - 900 m
# 900 - 970 m
# 970 - 1.125 m

# Vamos ver as cores dos retângulos da legenda na barra lateral
# Procurar paths perto de x=1750 a 1850 e y=600 a 1100
legend_paths = []
for p in objs:
    if p.type == 2:
        b = p.get_bounds()
        if b[0] >= 1700 and b[2] <= 1850 and b[1] >= 500 and b[3] <= 1100:
            legend_paths.append(p)

print(f"\nPaths encontrados na região da legenda: {len(legend_paths)}")
import ctypes
import pypdfium2.raw as pdfium_c
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
for idx, lp in enumerate(legend_paths):
    pdfium_c.FPDFPageObj_GetFillColor(lp.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
    hex_c = f"#{r.value:02X}{g.value:02X}{b.value:02X}"
    bounds = lp.get_bounds()
    print(f"  Legenda Box {idx}: Cor={hex_c} (RGB {r.value},{g.value},{b.value}), bounds={bounds}")

doc.close()
