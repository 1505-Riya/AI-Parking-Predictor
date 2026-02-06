from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd
import random
from datetime import datetime
import os
import numpy as np

app = FastAPI(title="Surat Smart Parking AI")

class ChatQuery(BaseModel):
    query: str

# --- DATA LOADING & CLEANING ---
def load_and_clean_data():
    file_path = 'D58-Parking Lots.csv'
    if not os.path.exists(file_path):
        print("ERROR: CSV File not found!")
        return pd.DataFrame()
    
    # Handle Encodings (fixes Error 1)
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except:
        df = pd.read_csv(file_path, encoding='latin1')

    # FORCE NUMERIC CONVERSION (fixes Error 2 & 3)
    # This turns 'NaN' or junk strings like '21?11" N' into None instantly
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['No. of 4 wheeler parking'] = pd.to_numeric(df['No. of 4 wheeler parking'], errors='coerce').fillna(0)
    df['No. of 2 wheeler parking'] = pd.to_numeric(df['No. of 2 wheeler parking'], errors='coerce').fillna(0)

    # Drop rows that don't have valid numeric Latitude/Longitude
    df = df.dropna(subset=['Latitude', 'Longitude'])
    
    return df

@app.get("/api/predict")
async def get_predictions(target_hour: int = Query(default=datetime.now().hour)):
    df = load_and_clean_data()
    if df.empty:
        return {"error": "No valid data found in CSV."}
    
    results = []
    for _, row in df.iterrows():
        # Total slots calculation (now safe from NaN errors)
        total_slots = int(row['No. of 4 wheeler parking'] + row['No. of 2 wheeler parking'])
        
        # AI Simulation Logic
        is_peak = (10 <= target_hour <= 13) or (18 <= target_hour <= 21)
        base_avail = random.randint(5, 25) if is_peak else random.randint(60, 95)
        final_avail = round(max(2, min(98, base_avail + random.uniform(-3, 3))), 1)
        
        results.append({
            "name": str(row['Name of Parking']),
            "lat": float(row['Latitude']),
            "lng": float(row['Longitude']),
            "availability": final_avail,
            "total_slots": total_slots,
            "confidence": random.randint(90, 98),
            "trend": "falling" if final_avail < 30 else "stable",
            "last_updated": datetime.now().strftime("%H:%M:%S")
        })
    
    return results

@app.post("/api/chat")
async def chat_with_ai(data: ChatQuery):
    responses = [
        "Surat ICCC indicates high availability in the Varachha zone.",
        "Traffic flow is heavy near the Textile Market. Suggesting alternative routes.",
        "AI Prediction: 92% confidence that parking availability will increase in 45 minutes."
    ]
    return {"reply": random.choice(responses)}

# Serve static files (GUI)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)