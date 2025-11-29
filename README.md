# AI Route Optimizer

A lightweight FastAPI service that computes an **optimal visiting order** for diesel delivery to multiple sites in a single trip.
It starts at a configurable **Depot**, builds a **distance matrix** using the Haversine great‑circle formula, and uses **Nearest Neighbor (NN)** plus **2‑opt** to produce a near‑optimal route quickly.

---

## 🌐 Architecture

```
Client (Swagger/Postman/curl)
        │
        ▼
   FastAPI (app.py)
        │
        ├── schemas.py    → Pydantic models for request & response
        ├── optimizer.py  → Orchestrates route calculation & totals
        └── utils.py      → Haversine, distance matrix, NN & 2‑opt, helpers
```

**Flow:**
1. Client sends `POST /ai/route/optimize` with a list of orders (site name + coordinates).
2. `optimizer.py` builds coordinates `[Depot + Customers]`, computes the **distance matrix** via **Haversine**.
3. `utils.py`:
   - **Nearest Neighbor** constructs an initial route (starting at Depot).
   - **2‑opt** improves it by removing inefficient edge crossings.
4. `optimizer.py` computes the **total distance (km)** and **estimated time (min)** using `average_speed_kmph`.
5. Returns a structured response: `optimalRoute`, `totalDistanceKm`, `estimatedTimeMin`, and a detailed `Trip`.

---

## 📌 Assumptions

- **Depot**
  - Defaults to `depot_lat = 19.0330`, `depot_lng = 73.0297` (Navi Mumbai region).
  - You can override these per request.

- **Distances**
  - Calculated using **Haversine** (straight‑line) for speed and offline operation.

- **Route Algorithm**
  - **Nearest Neighbor (NN)** for initial path + **2‑opt** for local improvement.
  - Works well for small/medium sets and returns results quickly.

- **Time Estimation**
  - `EstimatedTimeMin = (TotalDistanceKm / average_speed_kmph) × 60`.
  - Service time, capacity, and time windows are **not** applied in this minimal version (can be added later).

- **Extensibility (optional)**
  - **Google Distance Matrix API** for realistic road distances.
  - **Capacity constraints** (split into multiple trips if demand exceeds truck capacity).
  - **Time windows** (wait if early; count violations if late).
  - Small **Leaflet UI** to visualize routes.

---

## 🔌 APIs

### `GET /ping`
Health check.

**Response**
```json
{ "status": "ok", "ts": 1732... }
```

---

### `POST /ai/route/optimize`

Compute an optimized visiting order, total distance, and estimated time.

**Request body (minimal schema)**
```json
{
  "orders": [
    { "customer": "Site A", "lat": 19.0419, "lng": 73.0225 },
    { "customer": "Site B", "lat": 19.0759, "lng": 72.8777 },
    { "customer": "Site C", "lat": 19.0895, "lng": 73.0033 }
  ],
  "average_speed_kmph": 35,
  "depot_lat": 19.0330,  // optional; defaults shown
  "depot_lng": 73.0297   // optional
}
```

**Response (example; numbers depend on coordinates)**
```json
{
  "optimalRoute": ["Site A", "Site C", "Site B"],
  "totalDistanceKm": 28.6,
  "estimatedTimeMin": 49.0,
  "optimal_trips": [
    {
      "route": ["Site A", "Site C", "Site B"],
      "total_distance_km": 28.6,
      "total_time_min": 49.0,
      "capacity_ok": true,
      "time_window_violations": 0
    }
  ],
  "explanation": "Route computed using Nearest Neighbor + 2-opt over haversine distances. Estimated time assumes 35 km/h average speed.",
  "assumptions": [
    "Distances use haversine great-circle approximation.",
    "Time = distance / 35 km/h (no service time yet).",
    "No capacity or time-window constraints applied in this step."
  ]
}
```

---

## ▶️ How to run

### 1) Prerequisites
- **Python 3.10+**
- Windows/macOS/Linux
- PowerShell or terminal

### 2) Setup a virtual environment
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies
Install:
```bash
pip install -r requirements.txt
```

### 4) Project files
Place these files in the project folder:
- `app.py` — FastAPI endpoints (`/ping`, `/ai/route/optimize`)
- `schemas.py` — Pydantic models (`Order`, `OptimizeRequest`, `Trip`, `OptimizeResponse`)
- `utils.py` — Haversine, distance matrix, NN, 2‑opt, helpers
- `optimizer.py` — Orchestrates route build, computes totals, returns `OptimizeResponse`

### 5) Start the API
```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8081
```

**Health check**  
Open: `http://127.0.0.1:8081/ping`

**Swagger (interactive docs)**  
Open: `http://127.0.0.1:8081/docs`

### 6) Test the optimizer

**Swagger**  
- In `/docs`, expand `POST /ai/route/optimize` → **Try it out** → paste the sample request → **Execute**.

**curl (PowerShell)**
```powershell
curl -X POST "http://127.0.0.1:8081/ai/route/optimize" `
  -H "Content-Type: application/json" `
  -d "{ \"orders\": [
        { \"customer\": \"Site A\", \"lat\": 19.0419, \"lng\": 73.0225 },
        { \"customer\": \"Site B\", \"lat\": 19.0759, \"lng\": 72.8777 },
        { \"customer\": \"Site C\", \"lat\": 19.0895, \"lng\": 73.0033 }
      ],
      \"average_speed_kmph\": 35 }"
```

---

## 🧩 Repo structure (suggested)

```
ai-route-optimizer/
├── app.py
├── optimizer.py
├── schemas.py
├── utils.py
├── requirements.txt
└── README.md
```
