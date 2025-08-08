from fastapi import FastAPI
import redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379)

@app.post("/update_position")
async def update_position(aircraft_id: str, lng: float, lat: float, alt: int, speed: int):
    # Implement Day 2 logic here
    return {"status": "Position updated"}