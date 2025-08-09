# 🛩️ Redis Air Traffic Control Simulator

A real-time aircraft tracking system using Redis geospatial capabilities with conflict detection, built for the Redis Hackathon.

![Demo Screenshot](demo.gif)

## ✨ Features

- **Real-time aircraft tracking** using Redis geospatial indexes
- **Collision detection** via Lua scripting
- **Live Web UI** with Leaflet.js map
- **Stress-tested** for high throughput (1000+ req/sec)
- **Performance metrics** (p95/p99 latency tracking)

## 🛠️ Tech Stack

- **Backend**: FastAPI + Redis 8
- **Frontend**: Leaflet.js + WebSocket
- **Data Structures**:
  - Geospatial sets (aircraft positions)
  - Sorted sets (altitudes)
  - Streams (collision alerts)

## 🚀 Quick Start

### Prerequisites
- Docker Desktop
- Python 3.10+
- Node.js (for optional UI)

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/redis-airtraffic-simulator.git
cd redis-airtraffic-simulator

# Set up virtual environment
python -m venv venv
.\venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt
```
### Running the System

# Start Redis Stack
docker run -d -p 6379:6379 -p 8001:8001 --name redis-airtraffic redis/redis-stack:latest

# Launch backend
uvicorn backend.main:app --reload

# Generate test data (new terminal)
python scripts/simulate.py

# Optional: Stress test
python scripts/stress_test.py --workers=10 --duration=60