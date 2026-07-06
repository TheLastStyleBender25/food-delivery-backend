from math import radians, cos, sin, sqrt, atan2

def calculate_distance_in_kn(lat1, lon1, lat2, lon2) -> float:
    R = 6371
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a=(sin(d_lat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c
