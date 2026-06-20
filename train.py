import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

print("Loading Astram dataset...")
# Load tumhara real dataset
df = pd.read_csv("Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv")

# Hume sirf important columns chahiye
data = df[['event_cause', 'police_station', 'priority']].dropna()

print("Processing Data...")
# Categorical text ko numbers mein convert karna
le_cause = LabelEncoder()
le_station = LabelEncoder()

data['event_cause_encoded'] = le_cause.fit_transform(data['event_cause'])
data['police_station_encoded'] = le_station.fit_transform(data['police_station'])

X = data[['event_cause_encoded', 'police_station_encoded']]
y = data['priority'] # Low, Medium, High

print("Training ML Model...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Model aur encoders ko save karna taaki API use kar sake
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('le_cause.pkl', 'wb') as f:
    pickle.dump(le_cause, f)
with open('le_station.pkl', 'wb') as f:
    pickle.dump(le_station, f)

print("Model Training Successful! Saved as model.pkl")