import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
import ctypes

doc = pdfium.PdfDocument(r'js/maps_pdf/temas/Mapa Fragilidade Potencial.pdf')
page = doc[0]
objs = list(page.get_objects())

red, grn, blu, alf = ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint(), ctypes.c_uint()
fm, st = ctypes.c_int(), ctypes.c_int()
left, bottom, right, top = ctypes.c_float(), ctypes.c_float(), ctypes.c_float(), ctypes.c_float()

target_classes = ['#006100', '#7AAB00', '#FFFF00', '#FF0000', '#A80000']

all_bounds = {c: [1e9, 1e9, -1e9, -1e9] for c in target_classes}
total_count = {c: 0 for c in target_classes}

for idx, p in enumerate(objs):
    if type(p).__name__ == 'PdfObject':
        pdfium_c.FPDFPath_GetDrawMode(p.raw, ctypes.byref(fm), ctypes.byref(st))
        if fm.value != 0:
            pdfium_c.FPDFPageObj_GetBounds(p.raw, ctypes.byref(left), ctypes.byref(bottom), ctypes.byref(right), ctypes.byref(top))
            pdfium_c.FPDFPageObj_GetFillColor(p.raw, ctypes.byref(red), ctypes.byref(grn), ctypes.byref(blu), ctypes.byref(alf))
            f_hex = f'#{red.value:02X}{grn.value:02X}{blu.value:02X}'
            if f_hex in target_classes:
                total_count[f_hex] += 1
                box = all_bounds[f_hex]
                box[0] = min(box[0], left.value)
                box[1] = min(box[1], bottom.value)
                box[2] = max(box[2], right.value)
                box[3] = max(box[3], top.value)

for c in target_classes:
    box = all_bounds[c]
    print(f'{c}: total={total_count[c]}, bounds=({box[0]:.1f}, {box[1]:.1f}, {box[2]:.1f}, {box[3]:.1f})')
