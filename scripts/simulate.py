import random
import requests

BASE_URL = "http://localhost:8000"

def generate_aircraft():
    return f"flight{random.randint(1000, 9999)}"

def random_jfk_coord():
    # Near JFK airport (±0.1 degrees)
    return (
        -73.7781 + random.uniform(-0.1, 0.1),
        40.6413 + random.uniform(-0.1, 0.1),
        random.randint(30000, 40000)  # Altitude in feet
    )

def simulate():
    aircraft = generate_aircraft()
    lng, lat, alt = random_jfk_coord()
    
    response = requests.post(
        f"{BASE_URL}/update_position",
        json={
            "aircraft_id": aircraft,
            "lng": lng,
            "lat": lat,
            "alt": alt,
            "speed": random.randint(400, 600)
        }
    )
    print(f"{aircraft}: {response.json()}")

if __name__ == "__main__":
    for _ in range(20):  # Generate 20 planes
        simulate()