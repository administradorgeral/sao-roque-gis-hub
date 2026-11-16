import pypdfium2 as pdfium
import ctypes
import pypdfium2.raw as pdfium_c
import geopandas as gpd
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union, linemerge
from shapely.validation import make_valid
from PIL import Image

pdf_path = "C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/js/maps_pdf/temas/zoneamento_rbcv_2019.pdf"
doc = pdfium.PdfDocument(pdf_path)
page = doc[0]

# Precise parameters derived from tick marks #87, #69, #141, #123, #105
slope_lon = 1.0 / 242.41
intercept_lon = -47.0 - (slope_lon * 157.92)

slope_lat = 1.0 / 242.43
intercept_lat = -25.0 - (slope_lat * 121.41)

print(f"Calibration Parameters:")
print(f"  slope_lon: {slope_lon:.8f}, intercept_lon: {intercept_lon:.8f}")
print(f"  slope_lat: {slope_lat:.8f}, intercept_lat: {intercept_lat:.8f}")

# Check neatline box coordinates:
x_min, x_max = 31.201, 564.493
y_min, y_max = 33.079, 740.201

lon_min = slope_lon * x_min + intercept_lon
lon_max = slope_lon * x_max + intercept_lon
lat_min = slope_lat * y_min + intercept_lat
lat_max = slope_lat * y_max + intercept_lat

print(f"\nLeaflet ImageOverlay Bounds:")
print(f"  rasterBounds: [[{lat_min:.5f}, {lon_min:.5f}], [{lat_max:.5f}, {lon_max:.5f}]]")

# Check position of Mata da Câmara in São Roque
# São Roque Mata da Câmara is roughly around -23.535, -47.125
sr_pt = Point(-47.125, -23.535)
print(f"\nMata da Câmara expected coords: {sr_pt.y:.5f}, {sr_pt.x:.5f}")
x_pt = (sr_pt.x - intercept_lon) / slope_lon
y_pt = (sr_pt.y - intercept_lat) / slope_lat
print(f"  Corresponding PDF points: x={x_pt:.2f}, y={y_pt:.2f}")
