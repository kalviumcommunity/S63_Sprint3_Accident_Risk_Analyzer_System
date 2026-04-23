# Traffic Accident Analysis & Risk Prediction System

## 📋 Project Overview

A comprehensive end-to-end data science and machine learning application that analyzes traffic accident data to identify patterns and predict accident severity. This system combines exploratory data analysis, machine learning, and a user-friendly web interface to help traffic management authorities make data-driven decisions for accident prevention.

---

## 🎯 Objectives

1. **Analyze accident data** to identify correlations and patterns (time of day, weather conditions, road type)
2. **Build a Machine Learning model** to predict accident severity
3. **Provide actionable insights** for accident prevention and risk mitigation
4. **Create an interactive web application** for easy user interaction and predictions

---

## 📊 Dataset Structure

The system works with accident data containing the following attributes:

| Field | Type | Values |
|-------|------|--------|
| `time` | Categorical | Morning, Afternoon, Evening, Night |
| `weather` | Categorical | Clear, Rain, Fog |
| `road_type` | Categorical | Highway, City, Rural |
| `severity` | Categorical (Target) | Low, Medium, High |

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Seaborn, Matplotlib
- **Machine Learning**: Scikit-learn
- **Database**: MongoDB
- **Database Driver**: PyMongo
- **Web Framework**: Streamlit
- **Notebook Environment**: Jupyter Notebook

---

## 📁 Project Structure

```
S63_Sprint3_Accident_Risk_Analyzer_System/
│
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration and constants
│
├── 01_Data_Connection/
│   ├── connect_mongodb.py            # MongoDB connection setup
│   └── fetch_data.ipynb              # Data fetching and initial exploration
│
├── 02_Exploratory_Data_Analysis/
│   ├── eda_analysis.ipynb            # Complete EDA with visualizations
│   └── eda_insights.py               # Reusable EDA functions
│
├── 03_Data_Preprocessing/
│   ├── preprocessing.py              # Data cleaning and encoding
│   └── preprocessing.ipynb           # Preprocessing notebook
│
├── 04_Machine_Learning/
│   ├── model_training.py             # Model training and evaluation
│   ├── model.pkl                     # Trained model (generated)
│   └── training.ipynb                # Model training notebook
│
├── 05_Insights_Conclusion/
│   ├── insights_report.md            # Final insights and conclusions
│   └── insights_analysis.ipynb       # Detailed analysis notebook
│
├── 06_Web_Application/
│   ├── app.py                        # Streamlit web application
│   ├── app_utils.py                  # Utility functions for the app
│   └── sample_predictions.csv        # Sample predictions
│
└── data/
    ├── raw_data/                     # Raw data from MongoDB
    ├── processed_data/               # Processed data
    └── models/                       # Saved models
```

---

## 🔄 Project Phases

### **PHASE 1: DATA CONNECTION**
- Establish connection to MongoDB using PyMongo
- Fetch accident data from the database
- Convert data to Pandas DataFrame
- Remove unnecessary fields (e.g., `_id`)
- **Deliverable**: Connected data source and initial DataFrame

### **PHASE 2: EXPLORATORY DATA ANALYSIS (EDA)**
Create comprehensive visualizations and insights:

**Visualizations:**
1. **Count Plots**: Accidents by weather, time, road type, and severity distribution
2. **Line Plot**: Accident trends over time
3. **Scatter Plot**: Relationship between time and severity
4. **Box Plot**: Detect outliers in severity data

**Each graph includes:**
- Clear visualization of the pattern
- Statistical insights and interpretations
- Actionable conclusions

**Deliverable**: Complete EDA notebook with visualizations and insights

### **PHASE 3: DATA PREPROCESSING**
- Handle missing values (if any)
- Encode categorical variables using `pd.get_dummies()`
- Normalize/scale features if needed
- Prepare clean dataset for ML model
- **Deliverable**: Clean, encoded dataset ready for training

### **PHASE 4: MACHINE LEARNING MODEL**
- Define features (X) and target variable (y)
- Split dataset using `train_test_split` (typically 80-20 ratio)
- Train RandomForestClassifier model
- Make predictions on test set
- Evaluate using accuracy_score and other metrics
- Save trained model for deployment
- **Deliverable**: Trained model with accuracy metrics

### **PHASE 5: INSIGHTS & CONCLUSIONS**
- Summarize key findings from analysis
- Document model performance and limitations
- Provide recommendations for accident prevention
- Note assumptions and data limitations
- **Deliverable**: Comprehensive insights report

### **PHASE 6: WEB APPLICATION (STREAMLIT)**
Build an interactive web interface:

**User Inputs:**
- Time (dropdown): Morning, Afternoon, Evening, Night
- Weather (dropdown): Clear, Rain, Fog
- Road Type (dropdown): Highway, City, Rural

**Processing:**
- Encode user inputs to match training format
- Pass to trained ML model
- Generate prediction

**Outputs:**
- Predicted accident severity (Low, Medium, High)
- Risk level visualization
- Optional: Historical graphs and insights

**Deliverable**: Fully functional web application

---

## ✨ Features

### Data Analysis Features
- ✅ Comprehensive exploratory data analysis
- ✅ Multi-dimensional visualization of accident patterns
- ✅ Statistical analysis and outlier detection
- ✅ Trend analysis over time

### ML Model Features
- ✅ Multi-class classification (Low, Medium, High severity)
- ✅ RandomForest-based prediction engine
- ✅ Model accuracy and performance metrics
- ✅ Trained model persistence

### Web Application Features
- ✅ User-friendly interface
- ✅ Real-time severity prediction
- ✅ Interactive dropdowns for input selection
- ✅ Clear visualization of results
- ✅ Risk assessment display

---

## 📦 Dependencies

Core dependencies (see `requirements.txt`):
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Visualization
- `seaborn` - Statistical visualization
- `scikit-learn` - Machine learning
- `pymongo` - MongoDB connection
- `streamlit` - Web framework
- `jupyter` - Notebook environment

---

## 📈 Expected Outcomes

### Analysis Phase
- Identification of accident patterns by time, weather, and road type
- Statistical relationships between factors and severity
- Trend analysis and anomaly detection

### Model Phase
- Trained ML model with >70% accuracy (target)
- Clear feature importance rankings
- Performance metrics and evaluation results

### Application Phase
- Working prediction interface
- User-friendly design
- Fast and accurate severity predictions

---

## 🎓 Learning Outcomes

By completing this project, you will learn:
- ✅ End-to-end data pipeline development
- ✅ Exploratory data analysis techniques
- ✅ Data preprocessing and feature engineering
- ✅ Machine learning model training and evaluation
- ✅ Web application development with Streamlit
- ✅ MongoDB integration in Python
- ✅ Data visualization best practices

