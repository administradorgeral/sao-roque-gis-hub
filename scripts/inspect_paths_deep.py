import pypdfium2 as pdfium
from collections import Counter

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\40537_4_3_3_1 Declividade.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
path_objs = [obj for obj in objs if obj.type == 2]

print(f"Total de PATHs: {len(path_objs)}")

# Vamos amostrar características de 50 caminhos dentro do mapa
sample_paths = []
stroke_colors = Counter()
fill_colors = Counter()

for p in path_objs[:5000]: # Amostra de 5000 paths
    # Em pypdfium2, vamos ver se temos acesso a stroke_color ou get_stroke_color
    try:
        sc = p.get_stroke_color()
        stroke_colors[str(sc)] += 1
    except Exception as e:
        pass
    try:
        fc = p.get_fill_color()
        fill_colors[str(fc)] += 1
    except Exception as e:
        pass

print("\nCores de Stroke mais comuns (amostra de 5000):")
for c, cnt in stroke_colors.most_common(10):
    print(f"  Stroke {c}: {cnt}")

print("\nCores de Fill mais comuns (amostra de 5000):")
for c, cnt in fill_colors.most_common(10):
    print(f"  Fill {c}: {cnt}")

doc.close()
