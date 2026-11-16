import math

def utm23s_to_latlon(easting, northing):
    """
    Converte coordenadas UTM Fuso 23S (SIRGAS 2000 / WGS84) para Latitude e Longitude (graus decimais).
    Elipsóide GRS80 / WGS84: a = 6378137.0, f = 1/298.257222101
    """
    a = 6378137.0
    f = 1.0 / 298.257222101
    b = a * (1.0 - f)
    e2 = (a*a - b*b) / (a*a)
    e_prime2 = (a*a - b*b) / (b*b)
    k0 = 0.9996
    
    # Fuso 23S: meridiano central = -45.0 graus
    lon0 = math.radians(-45.0)
    false_easting = 500000.0
    false_northing = 10000000.0 # Hemisfério Sul
    
    x = easting - false_easting
    y = northing - false_northing # negativo no hemisfério sul
    
    M = y / k0
    mu = M / (a * (1.0 - e2/4.0 - 3.0*e2*e2/64.0 - 5.0*e2*e2*e2/256.0))
    
    e1 = (1.0 - math.sqrt(1.0 - e2)) / (1.0 + math.sqrt(1.0 - e2))
    
    phi1 = mu + (3.0*e1/2.0 - 27.0*e1**3/32.0)*math.sin(2.0*mu) + \
           (21.0*e1**2/16.0 - 55.0*e1**4/32.0)*math.sin(4.0*mu) + \
           (151.0*e1**3/96.0)*math.sin(6.0*mu) + \
           (1097.0*e1**4/512.0)*math.sin(8.0*mu)
           
    sin_phi1 = math.sin(phi1)
    cos_phi1 = math.cos(phi1)
    tan_phi1 = math.tan(phi1)
    
    N1 = a / math.sqrt(1.0 - e2 * sin_phi1 * sin_phi1)
    T1 = tan_phi1 * tan_phi1
    C1 = e_prime2 * cos_phi1 * cos_phi1
    R1 = a * (1.0 - e2) / ((1.0 - e2 * sin_phi1 * sin_phi1)**1.5)
    D = x / (N1 * k0)
    
    lat = phi1 - (N1 * tan_phi1 / R1) * (
        D*D/2.0 - 
        (5.0 + 3.0*T1 + 10.0*C1 - 4.0*C1*C1 - 9.0*e_prime2) * (D**4)/24.0 +
        (61.0 + 90.0*T1 + 298.0*C1 + 45.0*T1*T1 - 252.0*e_prime2 - 3.0*C1*C1) * (D**6)/720.0
    )
    
    lon = lon0 + (
        D - 
        (1.0 + 2.0*T1 + C1) * (D**3)/6.0 + 
        (5.0 - 2.0*C1 + 28.0*T1 - 3.0*C1*C1 + 8.0*e_prime2 + 24.0*T1*T1) * (D**5)/120.0
    ) / cos_phi1
    
    return math.degrees(lat), math.degrees(lon)

# Testar com ponto do centro de São Roque
lat, lon = utm23s_to_latlon(284300, 7395700)
print(f"UTM (284300, 7395700) -> Lat: {lat:.5f}, Lon: {lon:.5f}")
# Bounding box test
lat_sw, lon_sw = utm23s_to_latlon(270308.5, 7382234.4)
lat_ne, lon_ne = utm23s_to_latlon(299278.6, 7410187.6)
print(f"SW -> Lat: {lat_sw:.5f}, Lon: {lon_sw:.5f}")
print(f"NE -> Lat: {lat_ne:.5f}, Lon: {lon_ne:.5f}")
