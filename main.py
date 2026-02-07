from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
import pandas as pd
from datetime import datetime
import random

app = FastAPI()

# Global state for AI data
ai_state = {"occupied": 0, "total": 0, "confidence": 0}

@app.post("/api/sync_vision")
async def sync(data: dict):
    global ai_state
    ai_state.update(data)
    return {"status": "synced"}

@app.get("/api/map_data")
async def get_map_data():
    # Load your Singapore CSV
    df = pd.read_csv('lots_location.csv')
    
    # We will show the first 100 markers for performance
    df_display = df.head(100).copy()
    
    results = []
    for i, row in df_display.iterrows():
        # Node 0 is our Live AI node
        if i == 0:
            total = ai_state["total"] if ai_state["total"] > 0 else 50
            avail_pct = max(0, round(((total - ai_state["occupied"]) / total) * 100, 1))
            status = f"Live AI: {ai_state['occupied']} cars"
            conf = ai_state["confidence"]
        else:
            # Simulated predictive data for other nodes
            avail_pct = random.randint(10, 95)
            status = "Historical Prediction"
            conf = random.randint(90, 98)

        results.append({
            "id": i,
            "lat": float(row['Latitude']),
            "lng": float(row['Longitude']),
            "availability": avail_pct,
            "status": status,
            "confidence": conf
        })
    return results

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)