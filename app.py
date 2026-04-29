"""
Traffic Accident Risk Analyzer — Premium Streamlit App
Run:  python -m streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

# ── Config ───────────────────────────────────────────────────────────
st.set_page_config(page_title="Accident Risk Analyzer", page_icon="🚦", layout="wide")

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Base */
html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px; }
section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
section[data-testid="stSidebar"] .stRadio label { font-size: 15px; font-weight: 500; }
header[data-testid="stHeader"] { background: transparent; }

/* Card */
.card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px;
    padding: 28px; margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
}

/* Hero */
.hero { text-align: center; padding: 48px 20px 36px; }
.hero h1 { font-size: 3rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.15; }
.hero .accent { background: linear-gradient(135deg, #2563eb, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { font-size: 1.1rem; color: #64748b; margin-top: 16px; max-width: 560px; margin-left: auto; margin-right: auto; }

/* Stat card */
.stat-card {
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
    padding: 22px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stat-card .value { font-size: 2rem; font-weight: 700; color: #0f172a; }
.stat-card .label { font-size: 0.8rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }

/* Alert boxes */
.alert-low { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px; text-align: center; }
.alert-low .level { font-size: 1.8rem; font-weight: 700; color: #16a34a; }
.alert-med { background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 20px; text-align: center; }
.alert-med .level { font-size: 1.8rem; font-weight: 700; color: #d97706; }
.alert-high { background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 20px; text-align: center; }
.alert-high .level { font-size: 1.8rem; font-weight: 700; color: #dc2626; }

/* Section */
.section-title { font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 4px; }
.section-heading { font-size: 1.75rem; font-weight: 700; color: #0f172a; margin-bottom: 6px; }
.section-desc { font-size: 0.95rem; color: #64748b; margin-bottom: 24px; }

/* Chart insight */
.chart-insight { background: #f8fafc; border-left: 3px solid #2563eb; padding: 10px 14px; margin-top: 10px; border-radius: 0 8px 8px 0; font-size: 0.85rem; color: #475569; }

/* Hide ALL Streamlit default UI chrome */
#MainMenu, footer, .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
button[kind="headerNoPadding"], [data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stSidebar button[aria-label*="Collapse"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── MongoDB ──────────────────────────────────────────────────────────
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "traffic_accident_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "accidents")

@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGODB_URI)

client = get_mongo_client()
collection = client[MONGODB_DB][MONGODB_COLLECTION]

# ── Constants ────────────────────────────────────────────────────────
TIME_OPTIONS = ["Morning", "Afternoon", "Evening", "Night"]
WEATHER_OPTIONS = ["Clear", "Rain", "Fog"]
ROAD_TYPE_OPTIONS = ["Highway", "City", "Rural"]
SEVERITY_OPTIONS = ["Low", "Medium", "High"]
TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
INV_MAP = {0: "Low", 1: "Medium", 2: "High"}

# ── Helpers ──────────────────────────────────────────────────────────
def fetch_data():
    docs = list(collection.find({}, {"_id": 0}))
    if not docs:
        return pd.DataFrame(columns=["time", "weather", "road_type", "severity"])
    return pd.DataFrame(docs)

def train_model(df):
    X = pd.get_dummies(df[["time", "weather", "road_type"]])
    y = df["severity"].map(TARGET_MAP)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, model.predict(X_te))
    return model, list(X.columns), acc

def predict(model, cols, time_v, weather_v, road_v):
    inp = pd.get_dummies(pd.DataFrame([{"time": time_v, "weather": weather_v, "road_type": road_v}]))
    for c in cols:
        if c not in inp.columns:
            inp[c] = 0
    return INV_MAP[model.predict(inp[cols])[0]]

# ── Sidebar ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🚦 Accident Risk Analyzer")
    st.markdown("<p style='color:#64748b;font-size:13px;margin-top:-10px'>Data-driven safety insights</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["Home", "Predict", "Insights", "Add Data"], label_visibility="collapsed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>🚦 Accident Risk<br><span class="accent">Analyzer</span></h1>
        <p>Predict accident severity using machine learning. Analyze traffic patterns and make data-driven safety decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    df = fetch_data()
    total = len(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="label">Total Records</div><div class="value">{total}</div></div>', unsafe_allow_html=True)
    with c2:
        val = df["weather"].mode()[0] if not df.empty else "—"
        st.markdown(f'<div class="stat-card"><div class="label">Top Weather</div><div class="value">{val}</div></div>', unsafe_allow_html=True)
    with c3:
        val = df["severity"].mode()[0] if not df.empty else "—"
        st.markdown(f'<div class="stat-card"><div class="label">Top Severity</div><div class="value">{val}</div></div>', unsafe_allow_html=True)
    with c4:
        val = df["road_type"].mode()[0] if not df.empty else "—"
        st.markdown(f'<div class="stat-card"><div class="label">Top Road Type</div><div class="value">{val}</div></div>', unsafe_allow_html=True)

    if not df.empty:
        st.markdown("")
        st.markdown('<div class="section-title">RECENT RECORDS</div>', unsafe_allow_html=True)
        st.dataframe(df.tail(10), use_container_width=True, hide_index=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PREDICT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Predict":
    st.markdown('<div class="section-title">⚡ RISK ASSESSMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Predict Accident Severity</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Select conditions to predict severity using a RandomForest model trained on your live data.</div>', unsafe_allow_html=True)

    df = fetch_data()

    if len(df) < 5:
        st.warning(f"⚠️ Need at least **5 records** to train the model. Currently: **{len(df)}**. Go to **Add Data** first.")
    else:
        model, feat_cols, acc = train_model(df)
        st.info(f"📈 Model trained on **{len(df)} records** — Accuracy: **{acc:.0%}**")
        st.markdown("---")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            p_time = st.selectbox("🕐 Time of Day", TIME_OPTIONS)
        with c2:
            p_weather = st.selectbox("🌤️ Weather", WEATHER_OPTIONS)
        with c3:
            p_road = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔍 Predict Risk", use_container_width=True):
            result = predict(model, feat_cols, p_time, p_weather, p_road)
            risk_map = {"Low": "Low Risk ✅", "Medium": "Moderate Risk ⚠️", "High": "High Risk 🚨"}
            css_class = {"Low": "alert-low", "Medium": "alert-med", "High": "alert-high"}

            st.markdown("---")
            r1, r2 = st.columns(2)
            with r1:
                st.markdown(f'<div class="{css_class[result]}"><div style="font-size:0.8rem;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Predicted Severity</div><div class="level">{result}</div></div>', unsafe_allow_html=True)
            with r2:
                st.markdown(f'<div class="{css_class[result]}"><div style="font-size:0.8rem;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px">Risk Level</div><div class="level">{risk_map[result]}</div></div>', unsafe_allow_html=True)

            st.markdown(f"<p style='text-align:center;color:#64748b;margin-top:16px'>Conditions: <b>{p_time}</b> · <b>{p_weather}</b> · <b>{p_road}</b></p>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INSIGHTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Insights":
    st.markdown('<div class="section-title">📊 DATA ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Insights & Visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Explore accident patterns from your live MongoDB data.</div>', unsafe_allow_html=True)

    df = fetch_data()

    if df.empty:
        st.info("No data available yet. Go to **Add Data** to insert records.")
    else:
        sns.set_theme(style="whitegrid", font="Inter")

        # Row 1: Bar + Line
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**🌤️ Accidents by Weather**")
            fig, ax = plt.subplots(figsize=(5, 3.5))
            sns.countplot(data=df, x="weather", order=WEATHER_OPTIONS, palette=["#3b82f6","#06b6d4","#8b5cf6"], ax=ax)
            ax.set_xlabel(""); ax.set_ylabel("Count")
            for spine in ax.spines.values(): spine.set_visible(False)
            plt.tight_layout()
            st.pyplot(fig)
            top_w = df["weather"].value_counts().idxmax()
            st.markdown(f'<div class="chart-insight">💡 <b>{top_w}</b> is the most common weather condition in recorded accidents.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**🕐 Accident Trend by Time**")
            time_counts = df["time"].value_counts().reindex(TIME_OPTIONS, fill_value=0)
            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            ax2.plot(time_counts.index, time_counts.values, marker="o", linewidth=2.5, color="#2563eb", markersize=8)
            ax2.fill_between(time_counts.index, time_counts.values, alpha=0.08, color="#2563eb")
            ax2.set_xlabel(""); ax2.set_ylabel("Count")
            for spine in ax2.spines.values(): spine.set_visible(False)
            plt.tight_layout()
            st.pyplot(fig2)
            peak = time_counts.idxmax()
            st.markdown(f'<div class="chart-insight">💡 <b>{peak}</b> has the highest accident count, indicating elevated risk.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")

        # Row 2: Pie + Box
        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**⚠️ Severity Distribution**")
            fig3, ax3 = plt.subplots(figsize=(5, 3.5))
            sev = df["severity"].value_counts()
            colors = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
            ax3.pie(sev.values, labels=sev.index, autopct="%1.0f%%",
                    colors=[colors.get(l, "#94a3b8") for l in sev.index],
                    startangle=90, wedgeprops={"linewidth": 2, "edgecolor": "white"})
            plt.tight_layout()
            st.pyplot(fig3)
            top_s = sev.idxmax()
            st.markdown(f'<div class="chart-insight">💡 <b>{top_s}</b> severity is most frequent in the current dataset.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c4:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**📦 Severity by Road Type (Box Plot)**")
            sev_map = {"Low": 1, "Medium": 2, "High": 3}
            df_box = df.copy()
            df_box["severity_code"] = df_box["severity"].map(sev_map)
            fig4, ax4 = plt.subplots(figsize=(5, 3.5))
            sns.boxplot(data=df_box, x="road_type", y="severity_code", order=ROAD_TYPE_OPTIONS,
                        palette=["#3b82f6","#06b6d4","#8b5cf6"], ax=ax4)
            ax4.set_xlabel(""); ax4.set_ylabel("Severity (1=Low, 3=High)")
            for spine in ax4.spines.values(): spine.set_visible(False)
            plt.tight_layout()
            st.pyplot(fig4)
            st.markdown('<div class="chart-insight">💡 Box plot shows severity score spread and potential outliers per road type.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("")

        # Row 3: Heatmap
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**🗺️ Time vs Weather — Accident Heatmap**")
        hm = pd.crosstab(df["time"], df["weather"])
        fig5, ax5 = plt.subplots(figsize=(8, 3.5))
        sns.heatmap(hm, annot=True, fmt="d", cmap="Blues", ax=ax5, linewidths=1, linecolor="white")
        ax5.set_xlabel(""); ax5.set_ylabel("")
        plt.tight_layout()
        st.pyplot(fig5)
        st.markdown('<div class="chart-insight">💡 Heatmap reveals which time-weather combinations have the most accidents.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ADD DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Add Data":
    st.markdown('<div class="section-title">📝 DATA ENTRY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Add New Accident Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Enter accident details below. Records are saved instantly to MongoDB Atlas.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            time_v = st.selectbox("🕐 Time of Day", TIME_OPTIONS)
            weather_v = st.selectbox("🌤️ Weather Condition", WEATHER_OPTIONS)
        with c2:
            road_v = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
            severity_v = st.selectbox("⚠️ Severity Level", SEVERITY_OPTIONS)

        submitted = st.form_submit_button("➕ Add Record", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        try:
            collection.insert_one({"time": time_v, "weather": weather_v, "road_type": road_v, "severity": severity_v})
            st.success("Record added successfully ✅")
        except Exception as e:
            st.error(f"Error: {e}")

    df = fetch_data()
    if not df.empty:
        st.markdown("---")
        st.markdown(f'<div class="section-title">RECENT RECORDS ({len(df)} total)</div>', unsafe_allow_html=True)
        st.dataframe(df.tail(8), use_container_width=True, hide_index=True)
