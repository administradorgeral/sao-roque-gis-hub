import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from collections import Counter

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/1835_4_3_6_1 Pedológico.pdf')
page = doc[0]
objs = list(page.get_objects())

type_counts = Counter(type(p).__name__ for p in objs)
print("Object types in PDF:")
for t, cnt in type_counts.items():
    print(f"  {t}: {cnt}")

# If there are images, let's inspect them!
images = [p for p in objs if type(p).__name__ == 'PdfImage']
print(f"\nTotal images: {len(images)}")
for i, img in enumerate(images):
    w, h = img.get_px_size()
    left, bottom, right, top = img.get_bounds()
    print(f"  Image #{i}: size={w}x{h}, bounds=({left:.1f}, {bottom:.1f}, {right:.1f}, {top:.1f})")
