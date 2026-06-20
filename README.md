# TrafficSense

**Predictive Analytics Platform for Event-Driven Traffic Congestion Management**  
*Flipkart Gridlock Hackathon 2.0 – Theme 2: Event-Driven Congestion*

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)](https://streamlit.io/)

---

## 📋 Overview

Traffic management during planned and unplanned events traditionally relies on reactive decisions, leading to inefficient resource allocation and prolonged congestion. **TrafficSense** is an end-to-end predictive analytics platform that forecasts congestion severity and automates resource allocation (police personnel and barricades) using historical traffic data and machine learning.

This solution transforms reactive traffic management into a proactive, data-driven operation, enabling authorities to deploy resources strategically before congestion occurs.

---

## 🎯 Problem Statement

> *Traffic management during planned/unplanned events relies on reactive decisions.*

Current traffic management systems lack predictive capabilities, resulting in:
- Delayed response to congestion events
- Suboptimal allocation of police and barricade resources
- Increased commuter frustration and travel time
- Inability to anticipate congestion patterns during events

---

## ✨ Solution Highlights

TrafficSense addresses these challenges through:

| Feature | Benefit |
|---------|---------|
| **Predictive Congestion Forecasting** | Anticipates congestion severity using historical data patterns |
| **Automated Resource Allocation** | Recommends optimal police and barricade deployment |
| **Real-Time Spatial Mapping** | Visualizes congestion hotspots using interactive Folium maps |
| **Event-Driven Analytics** | Correlates congestion with planned/unplanned event data |
| **Machine Learning Engine** | Scikit-Learn Random Forest model for accurate predictions |

---


### Backend Engine
- **Framework**: FastAPI with Uvicorn ASGI server
- **Machine Learning**: Scikit-Learn Random Forest Classifier
- **API Endpoint**: RESTful API running on `localhost:8000`
- **Capabilities**: Congestion prediction, resource allocation recommendations

### Frontend Dashboard
- **Framework**: Python Streamlit
- **Mapping Library**: Folium for interactive spatial mapping
- **Visualization**: Real-time congestion heatmaps and resource deployment maps
- **Interface**: User-friendly dashboard for traffic authorities

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yogita-mehta/Gridlock-TrafficSense.git
   cd Gridlock-TrafficSense
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Backend Server** (Terminal 1)
   ```bash
   uvicorn app:app --reload
   ```
   Backend API runs on: `http://localhost:8000`

4. **Start the Frontend Dashboard** (Terminal 2 – separate terminal)
   ```bash
   python -m streamlit run frontend.py
   ```
   Frontend dashboard runs on: `http://localhost:8501`


---

## 🔧 API Reference

### POST `/predict`
Predict congestion severity for given event parameters.

**Request Body:**
```json
{
  "event_type": "planned",
  "expected_attendance": 5000,
  "duration_hours": 4,
  "location_lat": 28.6139,
  "location_lon": 77.2090
}
```

**Response:**
```json
{
  "congestion_level": "high",
  "confidence": 0.87,
  "recommended_police": 12,
  "recommended_barricades": 25,
  "peak_time": "18:30"
}
```

### GET `/health`
Health check endpoint for backend service.

---

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 🔮 Future Enhancements

- Integration with real-time IoT traffic sensors
- Multi-language support for regional authorities
- Advanced deep learning models (LSTM for time-series forecasting)
- Mobile application for field officers
- API integration with government traffic management systems

---

*Built with ❤️ for smarter traffic management*


