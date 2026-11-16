import pypdfium2 as pdfium

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]
textpage = page.get_textpage()
full_text = textpage.get_text_range()

targets = ["46°0'0\"O", "47°0'0\"O", "23°0'0\"S", "24°0'0\"S", "25°0'0\"S"]

for target in targets:
    idx = 0
    while True:
        pos = full_text.find(target, idx)
        if pos == -1:
            break
        boxes = [textpage.get_charbox(pos + k) for k in range(len(target))]
        left = min(b[0] for b in boxes)
        bottom = min(b[1] for b in boxes)
        right = max(b[2] for b in boxes)
        top = max(b[3] for b in boxes)
        print(f"{target} at {pos}: left={left:.2f}, bottom={bottom:.2f}, right={right:.2f}, top={top:.2f}, center_x={(left+right)/2:.2f}, center_y={(bottom+top)/2:.2f}")
        idx = pos + len(target)

# Also let's inspect the page objects: lines, rectangles, neatline (border of the map frame)
import ctypes
import pypdfium2.raw as pdfium_c

objs = list(page.get_objects())
print(f"\nTotal page objects: {len(objs)}")

paths = []
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
fm, st = ctypes.c_int(), ctypes.c_int()

for i, p in enumerate(objs):
    if p.type == pdfium.raw.FPDF_PAGEOBJ_PATH:
        pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        n_segs = pdfium_c.FPDFPath_CountSegments(p.raw)
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        # Look for neatline / map frame: wide rectangle
        w = right.value - left.value
        h = top.value - bottom.value
        if w > 400 and h > 500:
            print(f"Large Path object #{i}: left={left.value:.2f}, bottom={bottom.value:.2f}, right={right.value:.2f}, top={top.value:.2f}, w={w:.2f}, h={h:.2f}, n_segs={n_segs}, fill={fm.value}, stroke={st.value}")
        # Look for tick marks
        elif (w < 10 and h < 2) or (h < 10 and w < 2):
            if left.value < 40 or right.value > 550 or bottom.value < 40 or top.value > 730:
                pass # print(f"Tick #{i}: ({left.value:.2f}, {bottom.value:.2f}) -> ({right.value:.2f}, {top.value:.2f})")
