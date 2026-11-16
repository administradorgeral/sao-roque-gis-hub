import pypdfium2 as pdfium

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

# Render page at 300 DPI (scale = 300 / 72 = 4.1667)
scale = 300 / 72
bitmap = page.render(scale=scale)
img = bitmap.to_pil()
page_h = 841.49292

# Let's crop around Cotia:
# In points: x in [160, 210], y in [440, 480]
# Remember in PIL: pixel_y = (page_h - y) * scale
x0 = int(round(155 * scale))
x1 = int(round(220 * scale))
y0 = int(round((page_h - 485) * scale))
y1 = int(round((page_h - 435) * scale))

crop = img.crop((x0, y0, x1, y1))
crop.save("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/cotia_crop.png")
print("Saved cotia_crop.png:", crop.size)
