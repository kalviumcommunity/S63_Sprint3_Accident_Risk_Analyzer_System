"""
Traffic Accident Risk Analyzer System
======================================
A complete Streamlit application for accident data entry,
analysis, ML prediction, and visualization.

Run with:  streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Page Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Accident Risk Analyzer",
    page_icon="🚦",
    layout="wide",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MongoDB Connection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "traffic_accident_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "accidents")


@st.cache_resource
def get_mongo_client():
    """Create a reusable MongoDB client (cached across reruns)."""
    return MongoClient(MONGODB_URI)


client = get_mongo_client()
db = client[MONGODB_DB]
collection = db[MONGODB_COLLECTION]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Constants
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIME_OPTIONS = ["Morning", "Afternoon", "Evening", "Night"]
WEATHER_OPTIONS = ["Clear", "Rain", "Fog"]
ROAD_TYPE_OPTIONS = ["Highway", "City", "Rural"]
SEVERITY_OPTIONS = ["Low", "Medium", "High"]
TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
INVERSE_TARGET_MAP = {0: "Low", 1: "Medium", 2: "High"}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helper Functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def insert_record(time_val, weather_val, road_type_val, severity_val):
    """Insert a single accident record into MongoDB."""
    record = {
        "time": time_val,
        "weather": weather_val,
        "road_type": road_type_val,
        "severity": severity_val,
    }
    collection.insert_one(record)


def fetch_all_records():
    """Fetch all records from MongoDB and return as DataFrame."""
    documents = list(collection.find({}, {"_id": 0}))
    if not documents:
        return pd.DataFrame(columns=["time", "weather", "road_type", "severity"])
    return pd.DataFrame(documents)


def train_model(df):
    """Train a RandomForest model on the accident data."""
    X = pd.get_dummies(df[["time", "weather", "road_type"]])
    y = df["severity"].map(TARGET_MAP)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, list(X.columns), accuracy


def predict_severity(model, feature_columns, time_val, weather_val, road_type_val):
    """Predict severity using the trained model."""
    input_data = pd.DataFrame(
        [{"time": time_val, "weather": weather_val, "road_type": road_type_val}]
    )
    input_encoded = pd.get_dummies(input_data)

    # Align columns with training data
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[feature_columns]

    prediction = model.predict(input_encoded)[0]
    return INVERSE_TARGET_MAP[prediction]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Sidebar Navigation
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.sidebar.title("🚦 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Predict", "Insights", "About"],
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Home — Data Entry + Live Records
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "Home":
    st.title("🚦 Traffic Accident Risk Analyzer")
    st.markdown(
        "Enter accident conditions below. Every record is saved to "
        "**MongoDB Atlas** and displayed live."
    )
    st.markdown("---")

    # ── Data Entry Form ─────────────────────────────────────────────
    st.subheader("📝 Add New Accident Record")

    with st.form("accident_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            time_val = st.selectbox("Time of Day", TIME_OPTIONS)
            weather_val = st.selectbox("Weather Condition", WEATHER_OPTIONS)

        with col2:
            road_type_val = st.selectbox("Road Type", ROAD_TYPE_OPTIONS)
            severity_val = st.selectbox("Severity Level", SEVERITY_OPTIONS)

        submitted = st.form_submit_button("➕ Add Accident Record")

    if submitted:
        try:
            insert_record(time_val, weather_val, road_type_val, severity_val)
            st.success("Record added successfully ✅")
        except Exception as e:
            st.error(f"Failed to insert record: {e}")

    st.markdown("---")

    # ── Live Records ────────────────────────────────────────────────
    st.subheader("📊 Live Accident Records")

    df = fetch_all_records()

    if df.empty:
        st.info("No data available yet. Use the form above to add records.")
    else:
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Total Records", len(df))
        col_b.metric("Most Common Weather", df["weather"].mode()[0])
        col_c.metric("Most Common Severity", df["severity"].mode()[0])

        st.dataframe(df, use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Predict — ML Severity Prediction
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Predict":
    st.title("🔮 Predict Accident Severity")
    st.markdown(
        "Select conditions below to predict accident severity "
        "using a **RandomForest ML model** trained on your live data."
    )
    st.markdown("---")

    df = fetch_all_records()

    if len(df) < 5:
        st.warning(
            f"⚠️ You need at least **5 records** to train the model. "
            f"Currently you have **{len(df)}**. Go to Home and add more data."
        )
    else:
        # Train model on live data
        model, feature_columns, accuracy = train_model(df)

        st.info(f"📈 Model trained on **{len(df)} records** — Accuracy: **{accuracy:.2%}**")
        st.markdown("---")

        # Prediction form
        st.subheader("🎯 Enter Conditions")

        col1, col2, col3 = st.columns(3)
        with col1:
            pred_time = st.selectbox("Time of Day", TIME_OPTIONS, key="pred_time")
        with col2:
            pred_weather = st.selectbox("Weather", WEATHER_OPTIONS, key="pred_weather")
        with col3:
            pred_road = st.selectbox("Road Type", ROAD_TYPE_OPTIONS, key="pred_road")

        if st.button("🔍 Predict Severity"):
            result = predict_severity(
                model, feature_columns, pred_time, pred_weather, pred_road
            )

            # Color-coded result
            color_map = {"Low": "green", "Medium": "orange", "High": "red"}
            risk_map = {"Low": "Low Risk ✅", "Medium": "Moderate Risk ⚠️", "High": "High Risk 🚨"}

            st.markdown("---")
            st.subheader("📋 Prediction Result")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Predicted Severity", result)
            with res_col2:
                st.metric("Risk Level", risk_map[result])

            st.markdown(
                f"**Conditions:** {pred_time} · {pred_weather} · {pred_road}"
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: Insights — Charts and Analysis
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Insights":
    st.title("📊 Insights & Visualizations")
    st.markdown("Explore accident patterns from your **live MongoDB data**.")
    st.markdown("---")

    df = fetch_all_records()

    if df.empty:
        st.info("No data available yet. Go to Home and add some records first.")
    else:
        st.subheader(f"Analyzing {len(df)} records")

        # ── Row 1: Count plots ──────────────────────────────────────
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Accidents by Time of Day**")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x="time", order=TIME_OPTIONS, palette="Blues_d", ax=ax1)
            ax1.set_xlabel("Time of Day")
            ax1.set_ylabel("Count")
            plt.tight_layout()
            st.pyplot(fig1)

        with col2:
            st.markdown("**Accidents by Weather**")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x="weather", order=WEATHER_OPTIONS, palette="Oranges_d", ax=ax2)
            ax2.set_xlabel("Weather")
            ax2.set_ylabel("Count")
            plt.tight_layout()
            st.pyplot(fig2)

        st.markdown("---")

        # ── Row 2: More charts ──────────────────────────────────────
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Accidents by Road Type**")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x="road_type", order=ROAD_TYPE_OPTIONS, palette="Greens_d", ax=ax3)
            ax3.set_xlabel("Road Type")
            ax3.set_ylabel("Count")
            plt.tight_layout()
            st.pyplot(fig3)

        with col4:
            st.markdown("**Severity Distribution**")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            severity_counts = df["severity"].value_counts()
            colors = ["#2ecc71", "#f39c12", "#e74c3c"]
            ax4.pie(
                severity_counts.values,
                labels=severity_counts.index,
                autopct="%1.1f%%",
                colors=colors[:len(severity_counts)],
                startangle=90,
            )
            ax4.set_title("Severity Breakdown")
            plt.tight_layout()
            st.pyplot(fig4)

        st.markdown("---")

        # ── Row 3: Heatmap ──────────────────────────────────────────
        st.markdown("**Time vs Weather — Accident Count Heatmap**")
        heatmap_data = pd.crosstab(df["time"], df["weather"])
        fig5, ax5 = plt.subplots(figsize=(8, 4))
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd", ax=ax5)
        ax5.set_xlabel("Weather")
        ax5.set_ylabel("Time of Day")
        plt.tight_layout()
        st.pyplot(fig5)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: About
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "About":
    st.title("ℹ️ About This Project")
    st.markdown("---")

    st.markdown(
        """
        ### Traffic Accident Risk Analyzer System

        A comprehensive **Data Science + Machine Learning** application that
        analyzes traffic accident data to identify patterns and predict severity.

        ---

        #### 🎯 Objectives
        - Analyze accident data to identify patterns (time, weather, road type)
        - Build a Machine Learning model to predict accident severity
        - Provide actionable insights for accident prevention
        - Interactive web interface for easy predictions

        ---

        #### 🛠️ Tech Stack
        | Technology | Purpose |
        |------------|---------|
        | **Python** | Core language |
        | **Streamlit** | Web application framework |
        | **MongoDB Atlas** | Cloud database |
        | **Pandas** | Data manipulation |
        | **scikit-learn** | Machine learning |
        | **Matplotlib & Seaborn** | Data visualization |

        ---

        #### 🔄 How It Works
        1. **Data Entry** — Users add accident records through the form
        2. **Live Storage** — Records are stored in MongoDB Atlas instantly
        3. **Analysis** — Visualize patterns with interactive charts
        4. **Prediction** — ML model predicts severity based on conditions

        ---

        #### 📊 Dataset Structure
        | Field | Values |
        |-------|--------|
        | Time | Morning, Afternoon, Evening, Night |
        | Weather | Clear, Rain, Fog |
        | Road Type | Highway, City, Rural |
        | Severity | Low, Medium, High |

        ---

        *Built as part of Sprint 3 — Kalvium Community Project*
        """
    )
