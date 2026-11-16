import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf")
page = doc[0]

# In the PDF, Cotia is west of São Paulo.
# São Paulo Sé is around Lon -46.633 -> x ~ 157.92 + (-46.633 - (-47.0)) * 242.405 = 246.8
# Cotia is around Lon -46.919 -> x ~ 157.92 + (-46.919 - (-47.0)) * 242.405 = 177.5
# Cotia Lat is around -23.604 -> y ~ 363.84 + (-23.604 - (-24.0)) * 242.428 = 459.8

# Let's search for objects near x in [165, 200] and y in [440, 480]:
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()
fm, st = ctypes.c_int(), ctypes.c_int()
r, g, b, a = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()

print("Searching objects near Cotia (x ~ 170-195, y ~ 445-475)...")
for idx, p in enumerate(page.get_objects()):
    pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
    if 160 <= left.value <= 210 and 430 <= bottom.value <= 490:
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        color_info = ""
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            color_info += f"fill=#{r.value:02X}{g.value:02X}{b.value:02X} "
        if st.value != 0:
            pdfium_c.FPDFPageObj_GetStrokeColor(p.raw, ctypes.byref(r), ctypes.byref(g), ctypes.byref(b), ctypes.byref(a))
            color_info += f"stroke=#{r.value:02X}{g.value:02X}{b.value:02X} "
        print(f"Obj {idx}: type={p.type}, l={left.value:.2f}, b={bottom.value:.2f}, r={right.value:.2f}, t={top.value:.2f} {color_info}")
