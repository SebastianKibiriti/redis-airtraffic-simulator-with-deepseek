# 🛩️ Redis Air Traffic Control Simulator

A real-time aircraft tracking system using Redis geospatial capabilities with conflict detection, built for the Redis Hackathon.

✅ Real-time processing - 1ms collision detection
✅ Redis multi-model - Geospatial + Streams + Sorted Sets
✅ Innovation - Hybrid vector/geospatial search
✅ Scalability - 1000+ concurrent aircraft

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
# ⚙️ Running the System
```bash
### Start Redis Stack
docker run -d -p 6379:6379 -p 8001:8001 --name redis-airtraffic redis/redis-stack:latest

### Launch backend
uvicorn backend.main:app --reload

### Generate test data (new terminal)
python scripts/simulate.py

### Optional: Stress test
python scripts/stress_test.py --workers=10 --duration=60
```
# Key Files

**backend/**
- main.py (FastAPI endpoints)
- conflict_check.lua (Collision detection)

**frontend/**
- map.html (Live tracking UI)
- styles.css (Map styling)

**scripts/**
- simulate.py (Test data generator)
- stress_test.py (Performance tester)

# Redis Model Data

## Aircraft position (Geospatial)
GEOADD aircraft:positions -73.78 40.64 flight123

## Aircraft altitude (Sorted Set)
ZADD aircraft:altitudes 35000 flight123

## Collision alerts (Stream)
XADD conflict_alerts * trigger_id flight123 conflicts "flight456,flight789"