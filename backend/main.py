from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import redis
import json

app = FastAPI()
r = redis.Redis(host='localhost', port=6379)

CONFLICT_SCRIPT_SHA = "f744b0229e689e69fe14c655a774c6aecb584c28"  # From Step 2

class PositionUpdate(BaseModel):
    aircraft_id: str
    lng: float
    lat: float
    alt: int
    speed: int

@app.post("/update_position")
async def update_position(data: PositionUpdate):
    # Store position
    r.geoadd(
        "aircraft:positions", 
        {data.aircraft_id: (data.lng, data.lat)}  # New Redis-py syntax 
    )
    r.zadd("aircraft:altitudes", {data.aircraft_id: data.alt})
    
    # Check for conflicts
    conflicts = r.evalsha(
        CONFLICT_SCRIPT_SHA, 
        1,  # 1 key
        "aircraft:positions",  # KEYS[1]
        data.lng, data.lat, data.alt, data.aircraft_id  # ARGV[1-4]
    )
    
    return {"conflicts": conflicts}

@app.websocket("/alerts")
async def alert_feed(websocket: WebSocket):
    await websocket.accept()
    last_id = '$'  # Start from latest message
    
    while True:
        alerts = r.xread({"conflict_alerts": last_id}, count=1, block=5000)
        if alerts:
            last_id = alerts[0][1][0][0]  # Update last message ID
            await websocket.send_text(json.dumps(alerts[0][1][0][1]))