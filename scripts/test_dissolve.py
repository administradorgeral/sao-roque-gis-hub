import time
from shapely.ops import unary_union
from shapely import simplify, transform
import pyproj
import geopandas as gpd

print("Testando dissolve e simplificação com GeoPandas / Shapely...")
# Vamos carregar os polígonos extraídos em extract_full_vectors
# Vamos fazer uma função limpa para gerar o GeoPackage / GeoJSON otimizado
