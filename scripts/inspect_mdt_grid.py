import pypdfium2 as pdfium
import re

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

textpage = page.get_textpage()
num_chars = textpage.count_chars()
chars = []
for i in range(num_chars):
    ch = textpage.get_text_range(i, 1)
    if ch in '\r\n\t':
        continue
    box = textpage.get_charbox(i)
    chars.append({
        'char': ch,
        'left': box[0], 'bottom': box[1], 'right': box[2], 'top': box[3],
        'cx': (box[0] + box[2]) / 2, 'cy': (box[1] + box[3]) / 2
    })

print("--- COORDENADAS UTM Y (NORTHING) DETECTADAS NO MDT ---")
for target in ['7385000', '7390000', '7395000', '7400000', '7405000', '7410000']:
    for i in range(len(chars) - len(target) + 1):
        candidate = "".join([chars[i+j]['char'] for j in range(len(target))])
        if candidate == target:
            c_boxes = [chars[i+j] for j in range(len(target))]
            x0 = min(c['left'] for c in c_boxes)
            y0 = min(c['bottom'] for c in c_boxes)
            print(f"  UTM Y '{target}' @ x={x0:.1f}, y={y0:.1f}")

# Procurar retângulos de grande dimensão (Data Frame)
objs = list(page.get_objects())
print("\n--- OBJETOS GRANDES (DATA FRAME) ---")
for obj in objs:
    if obj.type == 2: # PATH
        b = obj.get_bounds()
        if b[2] - b[0] > 1000 and b[3] - b[1] > 1000:
            print(f"  Path Grande: bounds={b}, W={b[2]-b[0]:.2f}, H={b[3]-b[1]:.2f}")

doc.close()
