import multiprocessing
import time
import random
import requests
import statistics
import numpy as np

BASE_URL = "http://localhost:8000"

def generate_aircraft():
 return f"flight{random.randint(1000, 9999)}"

def random_jfk_coord():
    # Near JFK airport (±0.1 degrees)
 return (
        -73.7781 + random.uniform(-0.1, 0.1),
 40.6413 + random.uniform(-0.1, 0.1),
 random.randint(30000, 40000) # Altitude in feet
 )

def simulate_worker(worker_id, queue):
    num_flights = 100
    worker_latencies = []

    print(f"Worker {worker_id}: Starting simulation for {num_flights} flights...")

    for _ in range(num_flights):
        flight_start = time.time()
        aircraft = generate_aircraft()
        lng, lat, alt = random_jfk_coord()
        payload = {
            "aircraft_id": aircraft,
            "lng": lng,
            "lat": lat,
            "alt": alt,
            "speed": random.randint(400, 600),
        }

        try:
            requests.post(f"{BASE_URL}/update_position", json=payload, timeout=5)
            worker_latencies.append(time.time() - flight_start)
        except requests.exceptions.RequestException as e:
            print(f"Worker {worker_id}: Request failed: {e}")

    queue.put(worker_latencies)
    print(f"Worker {worker_id}: Finished.")

if __name__ == "__main__":
    num_workers = 10
    start = time.time()
    
    queue = multiprocessing.Queue()
    workers = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=simulate_worker, args=(i, queue))
        workers.append(p)
        p.start()

    all_latencies = []
    for p in workers:
        p.join()
        all_latencies.extend(queue.get())

    total_time = time.time() - start
    print(f"\n=== Aggregated Performance Metrics ===")
    print(f"Total requests processed: {len(all_latencies)} in {total_time:.2f}s")
    print(f"Throughput: {len(all_latencies) / total_time:.2f} req/sec")
    print(f"Average latency: {np.mean(all_latencies) * 1000:.2f}ms")
    print(f"Median latency (p50): {np.percentile(all_latencies, 50) * 1000:.2f}ms")
    print(f"95th percentile latency: {np.percentile(all_latencies, 95) * 1000:.2f}ms")
    print(f"99th percentile latency: {np.percentile(all_latencies, 99) * 1000:.2f}ms")
    print(f"Max latency: {np.max(all_latencies) * 1000:.2f}ms")