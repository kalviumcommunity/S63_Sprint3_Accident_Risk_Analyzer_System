"""Phase 6 Streamlit web application."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app.predict import predict_severity


st.set_page_config(
    page_title="Traffic Accident Risk Predictor",
    page_icon="🚦",
    layout="centered",
)

st.title("Traffic Accident Risk Prediction System")
st.write(
    "Select accident conditions to predict likely severity and risk level."
)

time_value = st.selectbox(
    "Time of Day",
    ["Morning", "Afternoon", "Evening", "Night"],
)
weather_value = st.selectbox(
    "Weather",
    ["Clear", "Rain", "Fog"],
)
road_type_value = st.selectbox(
    "Road Type",
    ["Highway", "City", "Rural"],
)

predict_clicked = st.button("Predict Severity")

if predict_clicked:
    try:
        result = predict_severity(
            time_value=time_value,
            weather_value=weather_value,
            road_type_value=road_type_value,
        )

        st.success("Prediction generated successfully")
        st.subheader("Prediction Result")
        st.write(f"Predicted Severity: {result['severity']}")
        st.write(f"Risk Level: {result['risk_level']}")

    except FileNotFoundError as error:
        st.error(str(error))
        st.info("Run Phase 4 training script before using this app.")
    except Exception as error:
        st.error(f"Unexpected error: {error}")
