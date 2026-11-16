import pyproj
from shapely.geometry import Point, box
from shapely.ops import transform

transformer = pyproj.Transformer.from_crs("EPSG:31983", "EPSG:4326", always_xy=True)

pt_utm = Point(284300, 7395700)
pt_wgs84 = transform(transformer.transform, pt_utm)
print("Transform UTM -> WGS84:")
print(f"X={pt_utm.x}, Y={pt_utm.y} -> Lon={pt_wgs84.x:.6f}, Lat={pt_wgs84.y:.6f}")
