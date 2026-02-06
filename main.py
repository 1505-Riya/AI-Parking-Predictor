from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random

app = FastAPI()

class ChatQuery(BaseModel):
    query: str

# 1. Mock Prediction Data (Replace with your ML model later)
@app.get("/api/predict")
async def get_predictions():
    # Centered around Ahmedabad (near SAC/ISRO)
    zones = [
        {"id": 1, "name": "Vastrapur", "lat": 23.0350, "lng": 72.5293, "availability": random.randint(10, 90)},
        {"id": 2, "name": "Prahlad Nagar", "lat": 23.0120, "lng": 72.5108, "availability": random.randint(10, 90)},
        {"id": 3, "name": "Satellite Area", "lat": 23.0300, "lng": 72.5300, "availability": random.randint(10, 90)},
        {"id": 4, "name": "Bodakdev", "lat": 23.0420, "lng": 72.5150, "availability": random.randint(10, 90)},
    ]
    return zones

# 2. AI Chat Logic (Simulated RAG/LLM)
@app.post("/api/chat")
async def chat_with_ai(data: ChatQuery):
    responses = [
        f"Based on my analysis, Zone B (Prahlad Nagar) will have the most spots at your requested time.",
        "I've detected a local event nearby; parking in Zone A will be restricted after 6 PM.",
        "The model predicts a 85% probability of finding a spot in the Satellite area right now."
    ]
    return {"reply": random.choice(responses)}

# 3. Serve Frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")