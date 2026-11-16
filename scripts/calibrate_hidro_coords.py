import pypdfium2 as pdfium
import re

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\Hidro .pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()
n_chars = textpage.count_chars()

full_text = textpage.get_text_range()

# Encontrar posições de coordenadas UTM Y: 7385000, 7390000, 7395000, 7400000, 7405000, 7410000
# E UTM X: 275000, 280000, 285000, 290000, 295000 (ou com vírgula: 7385000,000000)

y_targets = [7385000, 7390000, 7395000, 7400000, 7405000, 7410000]
x_targets = [275000, 280000, 285000, 290000, 295000]

found_y = []
found_x = []

# Buscar no texto corrido
for y_val in y_targets:
    target_str = str(y_val)
    idx = 0
    while True:
        pos = full_text.find(target_str, idx)
        if pos == -1:
            break
        # Pegar a caixa desse número
        box_first = textpage.get_charbox(pos)
        box_last = textpage.get_charbox(pos + len(target_str) - 1)
        center_x = (box_first[0] + box_last[2]) / 2.0
        center_y = (box_first[1] + box_last[3]) / 2.0
        found_y.append({
            "utm": y_val,
            "pdf_x": center_x,
            "pdf_y": center_y,
            "box": (box_first[0], box_first[1], box_last[2], box_last[3])
        })
        idx = pos + len(target_str)

for x_val in x_targets:
    target_str = str(x_val)
    idx = 0
    while True:
        pos = full_text.find(target_str, idx)
        if pos == -1:
            break
        box_first = textpage.get_charbox(pos)
        box_last = textpage.get_charbox(pos + len(target_str) - 1)
        center_x = (box_first[0] + box_last[2]) / 2.0
        center_y = (box_first[1] + box_last[3]) / 2.0
        found_x.append({
            "utm": x_val,
            "pdf_x": center_x,
            "pdf_y": center_y,
            "box": (box_first[0], box_first[1], box_last[2], box_last[3])
        })
        idx = pos + len(target_str)

print("--- COORDENADAS UTM Y ENCONTRADAS ---")
for item in found_y:
    print(f"  UTM Y = {item['utm']}: PDF X={item['pdf_x']:.2f}, Y={item['pdf_y']:.2f}")

print("\n--- COORDENADAS UTM X ENCONTRADAS ---")
for item in found_x:
    print(f"  UTM X = {item['utm']}: PDF X={item['pdf_x']:.2f}, Y={item['pdf_y']:.2f}")

doc.close()
