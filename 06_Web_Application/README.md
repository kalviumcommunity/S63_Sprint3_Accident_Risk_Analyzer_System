# Phase 6 - Web Application (Streamlit)

## Scope
- Build a simple Streamlit UI for accident severity prediction
- Collect user inputs: time, weather, road type
- Encode inputs to match training features
- Load trained model and display predicted severity and risk level

## Files
- `06_Web_Application/app.py`: Streamlit app entry point
- `src/app/predict.py`: Prediction and encoding helper logic

## Run
1. Ensure Phase 4 model exists at `data/models/accident_random_forest_model.joblib`
2. Start Streamlit:

streamlit run 06_Web_Application/app.py

## Inputs
- Time: Morning / Afternoon / Evening / Night
- Weather: Clear / Rain / Fog
- Road Type: Highway / City / Rural

## Output
- Predicted severity: Low / Medium / High
- Risk level: Low Risk / Moderate Risk / High Risk
