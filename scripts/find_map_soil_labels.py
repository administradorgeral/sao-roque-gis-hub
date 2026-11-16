import pypdfium2 as pdfium

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/1835_4_3_6_1 Pedológico.pdf')
tp = doc[0].get_textpage()

slope_x, intercept_x = 17.636295, 272427.45
slope_y, intercept_y = 17.636560, 7381364.75

def pdf_to_utm(px, py):
    return (slope_x * px + intercept_x, slope_y * py + intercept_y)

map_labels = []

# Search text inside the neatline / map area
for i in range(tp.count_chars()):
    b = tp.get_charbox(i)
    if 50 <= b[0] <= 1650 and 50 <= b[1] <= 1600:
        txt = tp.get_text_range(i, 8)
        if any(txt.startswith(prefix) for prefix in ['PVA', 'LVA', 'CH', 'RL', 'GX']):
            u_x, u_y = pdf_to_utm(b[0], b[1])
            map_labels.append((txt.strip(), b[0], b[1], u_x, u_y))

print(f"Found {len(map_labels)} soil unit label instances in map:")
# de-duplicate nearby labels
seen = set()
unique_labels = []
for l in map_labels:
    key = (l[0], round(l[1]/10)*10, round(l[2]/10)*10)
    if key not in seen:
        seen.add(key)
        unique_labels.append(l)

for u in unique_labels:
    print(f"  Label '{u[0]}' at PDF=({u[1]:.1f}, {u[2]:.1f}) -> UTM=({u[3]:.1f}E, {u[4]:.1f}N)")
