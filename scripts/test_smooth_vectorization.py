import pypdfium2 as pdfium
import numpy as np
import cv2
import time
from shapely.geometry import Polygon
from shapely import simplify, make_valid
import geopandas as gpd

print("Testando vetorização com fechamento morfológico anti-persiana...")
t0 = time.time()

pdf_path = r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\js\maps_pdf\temas\47531_4_2_3_2 MDT.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

objs = list(page.get_objects())
images = [obj for obj in objs if obj.type == 3][:87]

strip_bitmaps = [images[i].get_bitmap().to_numpy()[:, :, :3] for i in range(len(images))]
full_bgr = np.vstack(strip_bitmaps)
H, W, _ = full_bgr.shape

# Testar Classe 5 (Vermelho #FF2200 - 970 a 1125m)
mask = cv2.inRange(full_bgr, np.array([0, 25, 245]), np.array([15, 45, 255]))

# 1. Aplicar fechamento morfológico para eliminar frestas horizontais entre tiras
# Um kernel elíptico ou retangular vertical fecha as ranhuras horizontais
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 7)) # mais alto verticalmente para fechar linhas horizontais
closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# Suavizar bordas com blur mediano
smooth_mask = cv2.medianBlur(closed_mask, 5)

contours, _ = cv2.findContours(smooth_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
print(f"Contornos antes do filtro: {len(cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)[0])}")
print(f"Contornos após filtro anti-persiana: {len(contours)}")

# Salvar máscara comparativa para inspeção
cv2.imwrite(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\mask_raw.png", mask[2000:3000, 2500:3500])
cv2.imwrite(r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub\scripts\mask_smooth.png", smooth_mask[2000:3000, 2500:3500])
print("Máscaras salvas para comparação em scripts/mask_raw.png e mask_smooth.png")

doc.close()
