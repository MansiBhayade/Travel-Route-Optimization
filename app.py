
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schemas import OptimizeRequest, OptimizeResponse, Trip

app = FastAPI(title="AI Route Optimizer", version="0.2.0")

@app.get("/ping")
async def ping():
    import time
    return JSONResponse({"status": "ok", "ts": int(time.time())})

@app.post("/ai/route/optimize", response_model=OptimizeResponse)
async def ai_route_optimize(payload: OptimizeRequest):
    """
    Stub for now: returns a simple sequence and rough totals.
    We'll replace this with actual heuristics in the next step.
    """
    try:
        # simple visiting order = the order they were provided (placeholder)
        visiting_order = [o.customer for o in payload.orders]
        # placeholder numbers until we add real logic
        total_distance_km = 0.0
        estimated_time_min = 0.0

        return OptimizeResponse(
            optimalRoute=visiting_order,
            totalDistanceKm=total_distance_km,
            estimatedTimeMin=estimated_time_min,
            optimal_trips=[
                Trip(
                    route=visiting_order,
                    total_distance_km=total_distance_km,
                    total_time_min=estimated_time_min,
                    capacity_ok=True,
                    time_window_violations=0
                )
            ],
            explanation="Stub response; optimization logic will be added next.",
            assumptions=[
                "Using placeholder totals until the optimizer is implemented.",
                "Average speed/service times will be applied in the next step."
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

