import random
import requests
import json
import time
import statistics

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
    latencies = []
    start_time = time.time()
    num_flights = 100

    print(f"Starting performance test with {num_flights} flights...")

    for _ in range(num_flights):
        flight_start = time.time()

        aircraft = generate_aircraft()
        lng, lat, alt = random_jfk_coord()

        payload = {
            "aircraft_id": aircraft,
            "lng": lng,
            "lat": lat,
            "alt": alt,
            "speed": random.randint(400, 600)
        }

        response = requests.post(
            f"{BASE_URL}/update_position",
            json=payload
        )

        latencies.append(time.time() - flight_start)

    total_time = time.time() - start_time
    print(f"\n=== Performance Metrics ===")
    print(f"Total flights processed: {len(latencies)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Average latency: {statistics.mean(latencies)*1000:.2f}ms")
    print(f"Max latency: {max(latencies)*1000:.2f}ms")
    print(f"Throughput: {len(latencies)/total_time:.1f} req/sec")

if __name__ == "__main__":
    simulate()