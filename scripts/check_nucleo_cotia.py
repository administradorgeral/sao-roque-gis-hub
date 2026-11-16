import geopandas as gpd
from shapely.geometry import Point

gdf = gpd.read_file('data/rbcv_cinturao_verde_nucleos_web.geojson')
print("CRS:", gdf.crs)
print("Bounds:", gdf.total_bounds)

# In the user screenshot, the red pin is at:
# Lat: -23.65726, Lon: -46.98681
pt = Point(-46.98681, -23.65726)

# Let's find the nearest polygon or boundary of the Zona Núcleo to this point:
geom = gdf.geometry.iloc[0] # union of nucleos
dist_deg = geom.distance(pt)
print(f"Distance from red pin to Zona Núcleo: {dist_deg:.6f} degrees (~{dist_deg * 111320:.1f} m)")

# Let's find the northern boundary of the Morro Grande Zona Núcleo near Lon = -46.98681:
# Intersect geom with a vertical line at Lon = -46.98681
from shapely.geometry import LineString
line = LineString([(-46.98681, -23.80), (-46.98681, -23.60)])
inter = geom.intersection(line)
print(f"Intersection at Lon -46.98681: {inter}")
if hasattr(inter, 'geoms'):
    for g in inter.geoms:
        print(f"  Segment: {g.coords[:]}")
elif hasattr(inter, 'coords'):
    print(f"  Coords: {inter.coords[:]}")
