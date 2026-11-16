import pypdfium2 as pdfium
from collections import Counter
from PIL import Image

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

# As primeiras 92 imagens correspondem às tiras do mapa principal
# A imagem 92 é o logo/brasão na legenda
map_strips = images[:92]
print(f"Total de tiras do mapa: {len(map_strips)}")

all_colors = Counter()

# Amostrar a cada 5 tiras
for idx in range(0, len(map_strips), 3):
    bm = map_strips[idx].get_bitmap()
    pil_img = bm.to_pil()
    colors = pil_img.getcolors(maxcolors=2000)
    if colors:
        for cnt, col in colors:
            all_colors[col] += cnt

print("\n--- PALETA EXATA DO MDT (CORES PREDOMINANTES EM TODAS AS TIRAS) ---")
for col, cnt in all_colors.most_common(20):
    hex_c = f"#{col[0]:02X}{col[1]:02X}{col[2]:02X}"
    print(f"  {hex_c} (RGB {col[0]}, {col[1]}, {col[2]}): {cnt:,} pixels")

doc.close()
