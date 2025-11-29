from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from schemas import OptimizeRequest, OptimizeResponse
from optimizer import optimize

app = FastAPI(title="AI Route Optimizer", version="0.3.0")

@app.get("/ping")
async def ping():
    import time
    return JSONResponse({"status": "ok", "ts": int(time.time())})

@app.post("/ai/route/optimize", response_model=OptimizeResponse)
async def ai_route_optimize(payload: OptimizeRequest):
    try:
        return optimize(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
