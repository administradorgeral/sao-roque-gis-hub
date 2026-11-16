import pypdfium2.raw as pdfium_c

page_obj_funcs = [f for f in dir(pdfium_c) if 'FPDFPageObj' in f or 'FPDFPath' in f]
print("Funções encontradas:", page_obj_funcs[:30])
