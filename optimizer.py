from typing import List
import numpy as np
from llm import llm_explanation

from schemas import OptimizeRequest, OptimizeResponse, Trip
from utils import build_distance_matrix, nearest_neighbor_route, two_opt, route_distance, km_to_minutes

def optimize(req: OptimizeRequest) -> OptimizeResponse:
    """
    Build distance matrix (Depot + Customers), compute route with NN+2opt,
    and return totals + route names.
    """
    # 1) Coordinates: index 0 is Depot; 1..n are customers
    coords = [(req.depot_lat, req.depot_lng)] + [(o.lat, o.lng) for o in req.orders]
    names  = ["DEPOT"] + [o.customer for o in req.orders]

    # 2) Distance matrix
    D = build_distance_matrix(coords)

    # 3) Initial route via Nearest Neighbor (includes depot)
    nn_route = nearest_neighbor_route(D, start_index=0)

    # Ensure depot is first (safety in case NN picks otherwise)
    if nn_route[0] != 0:
        depot_pos = nn_route.index(0)
        nn_route = nn_route[depot_pos:] + nn_route[:depot_pos]

    # 4) Improve with 2-opt
    best_route = two_opt(nn_route, D)

    # 5) Compute totals
    total_km = route_distance(D, best_route)
    total_min = km_to_minutes(total_km, req.average_speed_kmph)

    # 6) Names: exclude depot from output route
    route_names = [names[i] for i in best_route if i != 0]

    # 6. Generate LLM explanation
    explanation = llm_explanation(
        route_names=route_names,
        total_km=round(float(total_km), 2),
        total_min=round(float(total_min), 1),
        speed=req.average_speed_kmph,
    )

    # 7) Package response (single trip for now; capacity/time windows come later)
    trip = Trip(
        route=route_names,
        total_distance_km=round(float(total_km), 2),
        total_time_min=round(float(total_min), 1),
        capacity_ok=True,                # since we didn't apply capacity yet
        time_window_violations=0         # since we didn't apply time windows yet
    )

    resp = OptimizeResponse(
        optimalRoute=route_names,
        totalDistanceKm=trip.total_distance_km,
        estimatedTimeMin=trip.total_time_min,
        optimal_trips=[trip],
        explanation=explanation,
        assumptions=[
            "Distances use haversine great-circle approximation.",
            f"Time = distance / {req.average_speed_kmph} km/h (no service time yet).",
            "No capacity or time-window constraints applied in this step."
        ]
    )
    return resp
