import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
fm, st = ctypes.c_int(), ctypes.c_int()

print("Scanning path objects for neatline / frame / tick marks...")
rectangles = []
lines = []

for idx, p in enumerate(page.get_objects()):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        w = right.value - left.value
        h = top.value - bottom.value
        
        # Check if it looks like the map frame (w > 400, h > 600)
        if w > 400 and h > 600:
            print(f"Candidate Frame/Neatline: left={left.value:.3f}, bottom={bottom.value:.3f}, right={right.value:.3f}, top={top.value:.3f}, w={w:.3f}, h={h:.3f}")
            rectangles.append((left.value, bottom.value, right.value, top.value))

        # Check for tick lines near 47°W (x ~ 153), 46°W (x ~ 395), 23°S (y ~ 606), 24°S (y ~ 363), 25°S (y ~ 121)
        if (abs(left.value - 153.05) < 5 or abs(left.value - 395.46) < 5) and (bottom.value < 40 or top.value > 730):
            print(f"X-Tick near {left.value:.3f}: b={bottom.value:.3f}, t={top.value:.3f}, w={w:.3f}, h={h:.3f}")
        if (abs(bottom.value - 606.06) < 5 or abs(bottom.value - 363.64) < 5 or abs(bottom.value - 121.21) < 5) and (left.value < 40 or right.value > 560):
            print(f"Y-Tick near {bottom.value:.3f}: l={left.value:.3f}, r={right.value:.3f}, w={w:.3f}, h={h:.3f}")
