import pypdfium2 as pdfium
from PIL import Image
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3]

# Testar imagens 0, 20, 45, 70
for idx in [0, 20, 45, 70]:
    bm = images[idx].get_bitmap()
    pil_img = bm.to_pil()
    colors = pil_img.getcolors(maxcolors=1000)
    print(f"\nImagem {idx} (bounds={images[idx].get_bounds()}):")
    if colors:
        print(f"  Total cores únicas: {len(colors)}")
        top_c = sorted(colors, key=lambda x: -x[0])[:5]
        for cnt, col in top_c:
            print(f"    Cor {col}: {cnt} px ({cnt*100/(pil_img.size[0]*pil_img.size[1]):.1f}%)")
    else:
        print(f"  Mais de 1000 cores únicas (gradiente ou foto contínua)")

doc.close()
