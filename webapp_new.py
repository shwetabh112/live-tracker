import streamlit as st
import folium
from streamlit_folium import st_folium
import random

# Initialize session state
if "vehicles" not in st.session_state:
    st.session_state.vehicles = {
        1: {"latitude": 40.7128, "longitude": -74.0060, "status": "idle"},
        2: {"latitude": 34.0522, "longitude": -118.2437, "status": "moving"},
        3: {"latitude": 41.8781, "longitude": -87.6298, "status": "stopped"},
    }

def simulate_vehicle_movement():
    for vid, info in st.session_state.vehicles.items():
        if info["status"] == "moving":
            info["latitude"] += random.uniform(-0.01, 0.01)
            info["longitude"] += random.uniform(-0.01, 0.01)

st.sidebar.title("Control Panel")
for vid in st.session_state.vehicles:
    command = st.sidebar.selectbox(
        f"Vehicle {vid} Command",
        ["None", "start", "stop", "park"],
        key=f"command_{vid}"
    )
    if command == "start":
        st.session_state.vehicles[vid]["status"] = "moving"
    elif command == "stop":
        st.session_state.vehicles[vid]["status"] = "stopped"
    elif command == "park":
        st.session_state.vehicles[vid]["status"] = "idle"

simulate = st.sidebar.button("Simulate Next Step")
if simulate:
    simulate_vehicle_movement()

m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)
for vid, info in st.session_state.vehicles.items():
    folium.Marker(
        location=[info["latitude"], info["longitude"]],
        popup=f"Vehicle {vid}: {info['status']}",
        icon=folium.Icon(
            color="green" if info["status"] == "moving"
            else "red" if info["status"] == "stopped"
            else "blue"
        )
    ).add_to(m)

st.title("🚗 Vehicle Tracker Dashboard")
st_folium(m, width=725)
