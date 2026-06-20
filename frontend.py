"""
Traffic Command Center — Streamlit Dashboard
=============================================
Run with:  streamlit run frontend.py
"""

import requests
import streamlit as st
import folium
from streamlit_folium import st_folium

# ──────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Gridlock · Traffic Command Center",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS — premium dark theme
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Global ───────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    /* hide default streamlit chrome */
    #MainMenu, header, footer {visibility: hidden;}

    /* ── Sidebar ──────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1117 0%, #161b22 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stTextInput label {
        color: #8b949e !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.08em;
    }

    /* ── Metric cards ─────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, rgba(22,27,34,0.95) 0%, rgba(13,17,23,0.98) 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 28px 24px;
        text-align: center;
        transition: transform 0.25s cubic-bezier(.4,0,.2,1),
                    box-shadow 0.25s cubic-bezier(.4,0,.2,1);
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 16px;
        padding: 1px;
        background: linear-gradient(135deg, rgba(255,255,255,0.08), transparent 60%);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.45);
    }
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 8px;
        display: block;
    }
    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #8b949e;
    }
    .severity-low    { color: #3fb950; text-shadow: 0 0 24px rgba(63,185,80,0.35); }
    .severity-medium { color: #d29922; text-shadow: 0 0 24px rgba(210,153,34,0.35); }
    .severity-high   { color: #f85149; text-shadow: 0 0 24px rgba(248,81,73,0.35); }
    .metric-blue     { color: #58a6ff; text-shadow: 0 0 24px rgba(88,166,255,0.35); }
    .metric-purple   { color: #bc8cff; text-shadow: 0 0 24px rgba(188,140,255,0.35); }

    /* ── Header area ──────────────────────────── */
    .dashboard-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 6px;
    }
    .dashboard-header h1 {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #8b949e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .dashboard-subtitle {
        color: #8b949e;
        font-size: 0.82rem;
        margin-bottom: 20px;
        font-weight: 400;
    }

    /* ── Status badge ─────────────────────────── */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .status-live {
        background: rgba(63,185,80,0.12);
        color: #3fb950;
        border: 1px solid rgba(63,185,80,0.25);
    }
    .status-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #3fb950;
        animation: pulse-dot 2s ease-in-out infinite;
    }
    @keyframes pulse-dot {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(63,185,80,0.5); }
        50%       { opacity: 0.6; box-shadow: 0 0 0 6px rgba(63,185,80,0); }
    }

    /* ── Map container ────────────────────────── */
    .map-container {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        margin-bottom: 24px;
    }

    /* ── Streamlit overrides ──────────────────── */
    .stApp { background: #0d1117; }
    div[data-testid="stHorizontalBlock"] { gap: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Real Data Mappings (Linked to Backend API)
# ──────────────────────────────────────────────
LOCATION_COORDS: dict[str, tuple[float, float]] = {
    "Peenya": (13.0400, 77.5180),
    "HSR Layout": (12.9218, 77.6451),
    "Wilson Garden": (12.9556, 77.5857),
    "Ashok Nagar": (12.9720, 77.6194),
    "Jayanagara": (12.9298, 77.5824)
}

EVENT_TYPES: list[str] = [
    "vehicle_breakdown",
    "others",
    "pot_holes",
    "bmtc_bus"
]

def _get_api_data(event_type: str, location: str) -> dict:
    """
    Fetches real predictions from the FastAPI backend.
    """
    payload = {
        "event_cause": event_type,
        "police_station": location
    }
    
    try:
        # Call the backend API
        response = requests.post("http://127.0.0.1:8000/predict_resources", json=payload, timeout=5)
        api_data = response.json()
        
        # Extract coordinates
        lat, lon = LOCATION_COORDS.get(location, (12.9716, 77.5946))
        
        return {
            "congestion_severity": api_data.get("predicted_priority", "Medium"),
            "police_required": api_data.get("recommended_cops", 0),
            "barricades_needed": api_data.get("recommended_barricades", 0),
            "lat": lat,
            "lon": lon,
            "nearby_incidents": [],
        }
        
    except requests.exceptions.RequestException:
        st.sidebar.error("⚠️ Backend API is offline! Start it using 'uvicorn app:app --reload'")
        lat, lon = LOCATION_COORDS.get(location, (12.9716, 77.5946))
        return {
            "congestion_severity": "Low",
            "police_required": "—",
            "barricades_needed": "—",
            "lat": lat,
            "lon": lon,
            "nearby_incidents": [],
        }


# ──────────────────────────────────────────────
# Sidebar controls
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding: 18px 0 10px;">
            <span style="font-size:2.2rem;">🚦</span>
            <h2 style="margin:6px 0 2px; font-weight:800; letter-spacing:-0.03em;
                        background:linear-gradient(135deg,#fff,#8b949e);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                TrafficSense
            </h2>
            <span style="font-size:0.68rem; color:#8b949e; text-transform:uppercase;
                         letter-spacing:0.1em; font-weight:600;">
                AI Command Center
            </span>
        </div>
        <hr style="border:none; border-top:1px solid rgba(255,255,255,0.06); margin:16px 0 24px;">
        """,
        unsafe_allow_html=True,
    )

    event_type = st.selectbox("Event Type", EVENT_TYPES, index=0)
    location = st.selectbox("Police Station Zone", list(LOCATION_COORDS.keys()), index=0)

    st.markdown(
        """
        <hr style="border:none; border-top:1px solid rgba(255,255,255,0.06); margin:24px 0 16px;">
        <p style="font-size:0.68rem; color:#3fb950; text-align:center; line-height:1.6; font-weight: 600;">
            ✅ Connected to FastAPI Backend
        </p>
        """,
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Fetch data from Backend
# ──────────────────────────────────────────────
data = _get_api_data(event_type, location)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="dashboard-header">
        <h1>Traffic Command Center</h1>
        <span class="status-badge status-live">
            <span class="status-dot"></span> Live ML Engine
        </span>
    </div>
    <p class="dashboard-subtitle">
        Real-time predictive resource allocation — Bengaluru Traffic Police
    </p>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Map
# ──────────────────────────────────────────────
SEVERITY_COLORS = {"Low": "#3fb950", "Medium": "#d29922", "High": "#f85149"}
severity = data.get("congestion_severity", "Low")
sev_color = SEVERITY_COLORS.get(severity, "#3fb950")

m = folium.Map(
    location=[data["lat"], data["lon"]],
    zoom_start=14,
    tiles="CartoDB dark_matter",
    control_scale=True,
)

# Primary incident marker
folium.CircleMarker(
    location=[data["lat"], data["lon"]],
    radius=18,
    color=sev_color,
    fill=True,
    fill_color=sev_color,
    fill_opacity=0.25,
    weight=2,
    popup=folium.Popup(
        f"<b>{event_type}</b><br>{location}<br>Severity: {severity}",
        max_width=220,
    ),
    tooltip=f"{location} — {severity}",
).add_to(m)

folium.Marker(
    location=[data["lat"], data["lon"]],
    popup=f"<b>{event_type}</b><br>{location}",
    tooltip=location,
    icon=folium.Icon(color="red" if severity == "High" else "orange" if severity == "Medium" else "green", icon="exclamation-triangle", prefix="fa"),
).add_to(m)

st.markdown('<div class="map-container">', unsafe_allow_html=True)
st_folium(m, use_container_width=True, height=460, returned_objects=[])
st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Metric cards
# ──────────────────────────────────────────────
sev_class = f"severity-{severity.lower()}"

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <span class="metric-icon">🔥</span>
            <div class="metric-value {sev_class}">{severity}</div>
            <div class="metric-label">Predicted Congestion Priority</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <span class="metric-icon">👮</span>
            <div class="metric-value metric-blue">{data['police_required']}</div>
            <div class="metric-label">Recommended Cops</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <span class="metric-icon">🚧</span>
            <div class="metric-value metric-purple">{data['barricades_needed']}</div>
            <div class="metric-label">Barricades Needed</div>
        </div>
        """,
        unsafe_allow_html=True,
    )