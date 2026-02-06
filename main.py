from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random
import time
from datetime import datetime

app = FastAPI(title="AI Smart Parking Predictor")

# --- DATA MODELS ---
class ChatQuery(BaseModel):
    query: str

# --- REAL-TIME ANALYTICS ENGINE ---
def calculate_dynamic_availability(base_zone_id, hour_of_day):
    """
    Simulates AI inference based on temporal patterns and 'live' surges.
   
    """
    # Base occupancy patterns (e.g., Office areas full at 9 AM, Markets at 6 PM)
    patterns = {
        1: {"peak": 18, "name": "Vastrapur Market"},      # Evening peak
        2: {"peak": 10, "name": "Prahlad Nagar (Office)"}, # Morning peak
        3: {"peak": 21, "name": "Satellite Residential"}, # Late night peak
        4: {"peak": 13, "name": "Bodakdev (Commercial)"}   # Lunch peak
    }
    
    config = patterns.get(base_zone_id)
    # Distance from peak hour reduces availability
    distance_from_peak = abs(hour_of_day - config["peak"])
    base_avail = 20 + (distance_from_peak * 5) # Simulating a trend
    
    # Near Real-Time 'Jitter': Simulates live vehicle movement
    live_jitter = random.randint(-5, 5)
    
    # Event-related demand surge simulation
    # For a hackathon, we simulate a surge if the current real-world second is even
    surge_factor = 0.7 if int(time.time()) % 2 == 0 else 1.0
    
    final_availability = max(5, min(95, (base_avail + live_jitter) * surge_factor))
    return round(final_availability, 1)

# --- API ENDPOINTS ---

@app.get("/api/predict")
async def get_predictions(target_hour: int = Query(default=datetime.now().hour)):
    """
    Returns zone-wise availability and confidence levels.
   
    """
    zones = [
        {"id": 1, "name": "Vastrapur Market", "lat": 23.0350, "lng": 72.5293},
        {"id": 2, "name": "Prahlad Nagar (Office)", "lat": 23.0120, "lng": 72.5108},
        {"id": 3, "name": "Satellite Residential", "lat": 23.0300, "lng": 72.5300},
        {"id": 4, "name": "Bodakdev (Commercial)", "lat": 23.0420, "lng": 72.5150},
    ]
    
    results = []
    for zone in zones:
        availability = calculate_dynamic_availability(zone["id"], target_hour)
        results.append({
            **zone,
            "availability": availability,
            "confidence": random.randint(85, 98), # AI Confidence metric
            "trend": "falling" if availability < 30 else "stable",
            "last_updated": datetime.now().strftime("%H:%M:%S")
        })
    return results

@app.post("/api/chat")
async def chat_with_ai(data: ChatQuery):
    """
    Simulates RAG/LLM logic for informed parking decisions.
   
    """
    # Simulated contextual awareness
    responses = [
        "Analysis shows high traffic flow trends toward Zone 1. I suggest Zone 2 for immediate parking.",
        "A demand surge is predicted near the Market area due to evening hours. Confidence: 92%.",
        "Traffic patterns are stable. Zone 3 currently offers the lowest fuel consumption route."
    ]
    return {"reply": random.choice(responses)}

# --- STATIC FILES (UI) ---
# Ensure your index.html is in a folder named 'static'
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)