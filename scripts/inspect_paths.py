import pypdfium2 as pdfium
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
print(f"Total de objetos: {len(objs)}")

type_counts = Counter(obj.type for obj in objs)
# Em PDFium: 1=TEXT, 2=PATH, 3=IMAGE, 4=SHADING, 5=FORM
type_names = {1: 'TEXT', 2: 'PATH', 3: 'IMAGE', 4: 'SHADING', 5: 'FORM'}
for t, c in type_counts.items():
    print(f"Tipo {t} ({type_names.get(t, 'UNKNOWN')}): {c} objetos")

# Vamos ver os caminhos (PATHS): quantos estão dentro do Data Frame do mapa?
# Data Frame: x in [31.4, 1674.0], y in [36.0, 1620.6]
paths_in_map = 0
paths_outside = 0
for obj in objs:
    if obj.type == 2: # PATH
        b = obj.get_bounds()
        if b[0] >= 30 and b[2] <= 1680 and b[1] >= 35 and b[3] <= 1625:
            paths_in_map += 1
        else:
            paths_outside += 1

print(f"Paths dentro do mapa: {paths_in_map}, paths fora: {paths_outside}")

# Vamos ver as imagens (IMAGE)
images = [obj for obj in objs if obj.type == 3]
print(f"Total de imagens: {len(images)}")
for i, img in enumerate(images[:10]):
    b = img.get_bounds()
    print(f"Imagem {i}: bounds={b}, px_size={img.get_px_size()}")

doc.close()
