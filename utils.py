from math import radians, sin, cos, sqrt, atan2
from typing import List
import numpy as np

EARTH_RADIUS_KM = 6371.0088  # WGS84 mean Earth radius

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points (km)."""
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2.0)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2.0)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return EARTH_RADIUS_KM * c

def build_distance_matrix(coords: List[tuple]) -> np.ndarray:
    """Create an NxN distance matrix using haversine."""
    n = len(coords)
    D = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i+1, n):
            d = haversine_km(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
            D[i, j] = d
            D[j, i] = d
    return D

def nearest_neighbor_route(D: np.ndarray, start_index: int = 0) -> List[int]:
    """Greedy TSP seed: always go to the nearest unvisited node."""
    n = D.shape[0]
    unvisited = set(range(n))
    route = [start_index]
    unvisited.remove(start_index)
    current = start_index
    while unvisited:
        next_idx = min(unvisited, key=lambda k: D[current, k])
        route.append(next_idx)
        unvisited.remove(next_idx)
        current = next_idx
    return route

def two_opt(route: List[int], D: np.ndarray, max_iter: int = 1000) -> List[int]:
    """Local search improvement for the route."""
    improved = True
    n = len(route)
    iters = 0
    while improved and iters < max_iter:
        improved = False
        iters += 1
        for i in range(1, n-2):
            for k in range(i+1, n-1):
                a, b = route[i-1], route[i]
                c, d = route[k], route[k+1]
                before = D[a, b] + D[c, d]
                after  = D[a, c] + D[b, d]
                if after + 1e-9 < before:
                    route[i:k+1] = reversed(route[i:k+1])
                    improved = True
        if not improved:
            break
    return route

def route_distance(D: np.ndarray, route: List[int]) -> float:
    """Sum of distances along the open route (no return to depot)."""
    return sum(D[route[i], route[i+1]] for i in range(len(route)-1))

def km_to_minutes(km: float, speed_kmph: float) -> float:
    """Convert distance to minutes using average speed."""
    return (km / speed_kmph) * 60.0
