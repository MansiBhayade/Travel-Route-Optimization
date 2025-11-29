
from typing import List, Optional
from pydantic import BaseModel, Field

class Order(BaseModel):
    customer: str = Field(..., description="Customer/site name")
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")
    demand_kl: Optional[float] = Field(None, description="Diesel demand (KL)")
    earliest_min: Optional[int] = Field(None, description="Earliest delivery start (minutes from midnight)")
    latest_min: Optional[int] = Field(None, description="Latest delivery start (minutes from midnight)")
    service_minutes: Optional[int] = Field(15, description="Service time at site (minutes)")

class OptimizeRequest(BaseModel):
    orders: List[Order]
    depot_lat: float = Field(19.0330, description="Depot latitude (default Navi Mumbai)")
    depot_lng: float = Field(73.0297, description="Depot longitude (default Navi Mumbai)")
    truck_capacity_kl: Optional[float] = Field(None, description="Truck capacity (KL)")
    average_speed_kmph: float = Field(35.0, description="Average driving speed for ETA")
    start_time_min: int = Field(9*60, description="Trip start time (minutes from midnight)")
    use_google_distance: bool = Field(False, description="Use Google Distance Matrix if available")

class Trip(BaseModel):
    route: List[str]
    total_distance_km: float
    total_time_min: float
    capacity_ok: bool
    time_window_violations: int

class OptimizeResponse(BaseModel):
    optimalRoute: List[str]
    totalDistanceKm: float
    estimatedTimeMin: float
    optimal_trips: List[Trip]
    explanation: str
    assumptions: List[str]
