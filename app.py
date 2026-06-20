from fastapi import FastAPI
from pydantic import BaseModel
import pickle

app = FastAPI()

# Saved ML model load karna
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('le_cause.pkl', 'rb') as f:
    le_cause = pickle.load(f)
with open('le_station.pkl', 'rb') as f:
    le_station = pickle.load(f)

# Request format define karna
class EventRequest(BaseModel):
    event_cause: str
    police_station: str

@app.post("/predict_resources")
def predict_traffic(request: EventRequest):
    try:
        # User ki request ko numbers mein convert karna
        cause_enc = le_cause.transform([request.event_cause])[0]
        station_enc = le_station.transform([request.police_station])[0]
        
        # Model se priority predict karwana
        prediction = model.predict([[cause_enc, station_enc]])[0]
        
        # Priority ke hisaab se logic lagana
        if prediction == "High":
            cops, barricades, spike = 15, 40, 85
        elif prediction == "Medium":
            cops, barricades, spike = 8, 20, 50
        else:
            cops, barricades, spike = 4, 10, 20
            
        return {
            "status": "success",
            "predicted_priority": prediction,
            "traffic_spike_percentage": spike,
            "recommended_cops": cops,
            "recommended_barricades": barricades
        }
    except Exception as e:
        return {"error": str(e)}