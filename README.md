# 🚦 Traffic Accident Risk Analyzer System

A complete **Data Science + Machine Learning** web application built with Streamlit that analyzes traffic accident data, identifies patterns, and predicts accident severity.

---

## 🎯 Objectives

1. **Collect accident data** through an interactive web form
2. **Store data live** in MongoDB Atlas
3. **Visualize patterns** across time, weather, road type, and severity
4. **Predict accident severity** using a trained RandomForest ML model

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Streamlit | Web application framework |
| MongoDB Atlas | Cloud database |
| Pandas | Data manipulation |
| scikit-learn | Machine learning (RandomForest) |
| Matplotlib & Seaborn | Data visualization |

---

## 📁 Project Structure

```
S63_Sprint3_Accident_Risk_Analyzer_System/
│
├── app.py               # Main Streamlit application (all-in-one)
├── requirements.txt     # Python dependencies
├── .env                 # MongoDB connection credentials
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file with your MongoDB credentials:

```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
MONGODB_DB=traffic_accident_db
MONGODB_COLLECTION=accidents
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 📊 Features

### 🏠 Home — Live Data Entry
- Add accident records through a clean form
- Data is stored instantly in MongoDB Atlas
- View all records in a live data table with summary metrics

### 🔮 Predict — ML Severity Prediction
- Trained RandomForest model on your live data
- Select time, weather, and road type conditions
- Get instant severity prediction (Low / Medium / High)

### 📊 Insights — Charts & Analysis
- Count plots for time, weather, road type distributions
- Severity breakdown pie chart
- Time vs Weather heatmap
- All visualizations update live from MongoDB data

### ℹ️ About — Project Overview
- Project objectives, tech stack, and architecture

---

## 📊 Dataset Structure

| Field | Type | Values |
|-------|------|--------|
| `time` | Categorical | Morning, Afternoon, Evening, Night |
| `weather` | Categorical | Clear, Rain, Fog |
| `road_type` | Categorical | Highway, City, Rural |
| `severity` | Target | Low, Medium, High |

> **No hardcoded data** — all data comes from user input through the form.

---

## 🔄 How It Works

1. **Data Entry** → User fills the form and submits
2. **MongoDB Storage** → Record is inserted into MongoDB Atlas
3. **Live Display** → Data table and metrics update instantly
4. **ML Training** → RandomForest trains on all available records
5. **Prediction** → Model predicts severity for new conditions
6. **Visualization** → Charts reflect live data patterns

---

*Built as part of Sprint 3 — Kalvium Community Project*
