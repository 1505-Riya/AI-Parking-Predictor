import pandas as pd
import random
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
app = FastAPI()

# 1. PASTE THE CLASS DEFINITION HERE
class VisionUpdate(BaseModel):
    occupied: int
    total: int
    confidence: float

# 2. KEEP YOUR AI_STATE HERE
ai_state = {"total": 60, "occupied": 25, "confidence": 98.4, "availability": 45}

# 3. PASTE THE POST ROUTE HERE
@app.post("/api/sync_vision")
async def sync_vision(data: VisionUpdate):
    global ai_state
    ai_state["occupied"] = data.occupied
    ai_state["total"] = data.total
    ai_state["confidence"] = data.confidence
    # This math updates your 45% live
    ai_state["availability"] = round(((data.total - data.occupied) / data.total) * 100, 1)
    return {"status": "synchronized"}

# Simulated AI State for the live node
ai_state = {"total": 60, "occupied": 25, "confidence": 98.4}

@app.get("/api/map_data")
async def get_map_data():
    results = []
    
    if os.path.exists('lots_location.csv'):
        try:
            df = pd.read_csv('lots_location.csv')
            # Top 150 points for performance
            df_display = df.head(150).copy()
            
            for i, row in df_display.iterrows():
                lat = float(row.get('Latitude', row.get('latitude')))
                lng = float(row.get('Longitude', row.get('longitude')))
                
                # DISTRICT MAPPING (Local Searchable Text)
                if i == 0:
                    name = "LIVE AI SENSOR (PKLot Node)"
                    status = "Active Vision Feed"
                elif lat < 1.29:
                    name = f"CBD Hub #{i}"; status = "Marina Bay District"
                elif lng > 103.92:
                    name = f"East Coast Node #{i}"; status = "Changi / Airport"
                elif lng < 103.75:
                    name = f"West Side Parking #{i}"; status = "Jurong Sector"
                elif lat > 1.40:
                    name = f"North Gateway #{i}"; status = "Woodlands Area"
                else:
                    name = f"Central Hub #{i}"; status = "Orchard / Bishan"

                results.append({
                    "lat": lat, "lng": lng, "name": name, 
                    "status": status, "availability": random.randint(15, 95) if i != 0 else 45,
                    "confidence": 98.4 if i == 0 else random.randint(92, 98)
                })
        except Exception as e:
            print(f"Data Error: {e}")

    return results

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Singapore AI Hub Server Running...")
    uvicorn.run(app, host="127.0.0.1", port=8000)