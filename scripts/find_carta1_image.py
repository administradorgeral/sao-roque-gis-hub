import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\minuta_pd2026\desmembrado\02_cartas_tecnicas\carta_01_macrozoneamento_municipal.pdf")
page = doc[0]

left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

for idx, obj in enumerate(page.get_objects()):
    if obj.type == pdfium.raw.FPDF_PAGEOBJ_IMAGE:
        pdfium_c.FPDFPageObj_GetBounds(obj.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
        print(f"Image Object {idx}: bounds x=[{left.value:.1f}, {right.value:.1f}], y=[{bottom.value:.1f}, {top.value:.1f}] w={right.value-left.value:.1f}, h={top.value-bottom.value:.1f}")
