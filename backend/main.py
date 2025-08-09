from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import redis
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")
r = redis.Redis(
    host='127.0.0.1',  # Use explicit IP instead of 'localhost'
    port=6379,
    socket_connect_timeout=3,
    socket_keepalive=True
)

CONFLICT_SCRIPT_SHA = "b5c841ce73f07f9a0c8c0bf035eeb11c53ec9ade"  # From Step 2

class PositionUpdate(BaseModel):
    aircraft_id: str
    lng: float
    lat: float
    alt: int
    speed: int

@app.post("/update_position")
async def update_position(data: PositionUpdate):
    # Store position using the idiomatic redis-py method.
    # The client library handles converting numbers to strings for Redis.
    r.geoadd("aircraft:positions", (data.lng, data.lat, data.aircraft_id))
    
    # Store altitude
    r.zadd("aircraft:altitudes", {data.aircraft_id: data.alt})
    
    # Check for conflicts
    conflicts = r.evalsha(
        CONFLICT_SCRIPT_SHA, 
        1,
        "aircraft:positions",
        data.lng,
        data.lat,
        data.alt,
        data.aircraft_id
    )
    return {"conflicts": conflicts}

@app.get("/current_positions")
async def get_positions():
    # Use a pipeline to fetch all data in a single round trip for performance.
    pipe = r.pipeline()
    
    # 1. Get all aircraft IDs and their altitudes at once.
    aircraft_with_scores = r.zrange("aircraft:altitudes", 0, -1, withscores=True)
    if not aircraft_with_scores:
        return []

    # 2. For each aircraft ID, add a GEOPOS command to the pipeline.
    for aircraft_id, _ in aircraft_with_scores:
        pipe.geopos("aircraft:positions", aircraft_id)
    
    # 3. Execute the pipeline to get all geographic positions.
    geo_positions = pipe.execute()

    # 4. Combine the results.
    positions = []
    for i, (aircraft_id_bytes, alt) in enumerate(aircraft_with_scores):
        pos_data = geo_positions[i]
        if pos_data and pos_data[0]:
            lng, lat = pos_data[0]
            positions.append({
                "id": aircraft_id_bytes.decode(),
                "lat": lat,
                "lng": lng,
                "alt": int(alt)
            })
    return positions


@app.websocket("/alerts")
async def alert_feed(websocket: WebSocket):
    await websocket.accept()
    last_id = '$'  # Start from latest message
    
    while True:
        alerts = r.xread({"conflict_alerts": last_id}, count=1, block=5000)
        if alerts:
            last_id = alerts[0][1][0][0]  # Update last message ID
            await websocket.send_text(json.dumps(alerts[0][1][0][1]))

@app.get("/")
async def get_root():
    with open("frontend/map.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)