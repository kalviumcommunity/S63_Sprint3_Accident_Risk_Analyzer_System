"""
Traffic Accident Risk Analyzer — Premium Streamlit App
Run:  python -m streamlit run app.py
"""

import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient
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

/* Risk Score */
.score-ring { text-align: center; padding: 32px 20px; }
.score-ring .number { font-size: 4rem; font-weight: 800; line-height: 1; }
.score-ring .number.low { color: #16a34a; }
.score-ring .number.med { color: #d97706; }
.score-ring .number.high { color: #dc2626; }
.score-ring .label-text { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; margin-top: 8px; }
.breakdown-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center; }
.breakdown-card .bk-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; }
.breakdown-card .bk-value { font-size: 1.1rem; font-weight: 700; color: #0f172a; margin-top: 4px; }
.breakdown-card .bk-weight { font-size: 0.8rem; color: #64748b; margin-top: 2px; }

/* Recommendations */
.reco-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px 28px; margin-top: 20px; }
.reco-card .reco-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 16px; }
.reco-card .reco-title.low { color: #16a34a; }
.reco-card .reco-title.med { color: #d97706; }
.reco-card .reco-title.high { color: #dc2626; }
.reco-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 0.9rem; color: #334155; }
.reco-item:last-child { border-bottom: none; }
.reco-icon { flex-shrink: 0; font-size: 1rem; }

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
LOCATION_OPTIONS = [
    "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
    "Chandigarh", "Bhopal", "Indore", "Patna", "Nagpur",
    "Kochi", "Guwahati", "Dehradun", "Surat", "Visakhapatnam",
]

# Risk score weights
TIME_WEIGHTS = {"Morning": 20, "Afternoon": 30, "Evening": 50, "Night": 80}
WEATHER_WEIGHTS = {"Clear": 10, "Rain": 60, "Fog": 70}
ROAD_WEIGHTS = {"City": 30, "Highway": 70, "Rural": 50}
LOCATION_WEIGHTS = {
    "Mumbai": 10, "Delhi": 8, "Kolkata": 7, "Chennai": 7, "Bangalore": 5,
    "Hyderabad": 5, "Pune": 5, "Ahmedabad": 5, "Lucknow": 6, "Patna": 7,
    "Jaipur": 4, "Chandigarh": 3, "Bhopal": 4, "Indore": 4, "Nagpur": 4,
    "Kochi": 5, "Guwahati": 6, "Dehradun": 5, "Surat": 5, "Visakhapatnam": 4,
}

# ── Helpers ──────────────────────────────────────────────────────────
def fetch_data():
    docs = list(collection.find({}, {"_id": 0}))
    if not docs:
        return pd.DataFrame(columns=["time", "weather", "road_type", "severity", "location"])
    return pd.DataFrame(docs)

def calculate_risk_score(time_v, weather_v, road_v, location_v):
    """Calculate risk score 0–100 from weighted inputs + location bonus."""
    t = TIME_WEIGHTS[time_v]
    w = WEATHER_WEIGHTS[weather_v]
    r = ROAD_WEIGHTS[road_v]
    l = LOCATION_WEIGHTS.get(location_v, 0)
    score = min(round((t + w + r) / 3 + l), 100)
    return score, t, w, r, l

def classify_risk(score):
    """Map score to risk level."""
    if score <= 40:
        return "Low", "low"
    elif score <= 70:
        return "Medium", "med"
    else:
        return "High", "high"

def get_recommendations(time_v, weather_v, road_v, location_v, level):
    """Generate smart safety recommendations based on conditions."""
    tips = []

    # Risk-level tips
    if level == "High":
        tips.append(("🚨", "High-risk conditions detected. Avoid travel if possible."))
        tips.append(("🛑", "If travel is necessary, inform someone of your route and ETA."))
    elif level == "Medium":
        tips.append(("⚠️", "Moderate risk detected. Exercise extra caution while driving."))
    else:
        tips.append(("✅", "Conditions are relatively safe. Follow standard driving practices."))

    # Time-based tips
    if time_v == "Night":
        tips.append(("🌙", "Avoid late-night travel if possible. Visibility is significantly reduced."))
        tips.append(("💡", "Use high-beam headlights on empty roads, low-beam when traffic is near."))
    elif time_v == "Evening":
        tips.append(("🌆", "Be cautious during peak traffic hours. Stay alert for sudden stops."))
    elif time_v == "Morning":
        tips.append(("🌅", "Watch for sun glare during early morning hours."))

    # Weather-based tips
    if weather_v == "Rain":
        tips.append(("🌧️", "Drive slowly — roads may be slippery. Increase following distance."))
        tips.append(("🚗", "Avoid sudden braking and sharp turns on wet surfaces."))
    elif weather_v == "Fog":
        tips.append(("🌫️", "Use fog lights and maintain a safe following distance."))
        tips.append(("🐌", "Reduce speed significantly. Avoid overtaking other vehicles."))

    # Road-type tips
    if road_v == "Highway":
        tips.append(("🛣️", "Maintain speed limits and stay alert for lane changes."))
        tips.append(("🔄", "Take regular breaks on long highway drives to avoid fatigue."))
    elif road_v == "Rural":
        tips.append(("🏔️", "Watch for unmarked roads, sharp curves, and wildlife."))
    elif road_v == "City":
        tips.append(("🏙️", "Watch for pedestrians, cyclists, and frequent signal changes."))

    # Location-based tips
    loc_tips = {
        "Mumbai": "Mumbai sees heavy monsoon rainfall — waterlogging and flooding are common. Avoid low-lying routes.",
        "Delhi": "Delhi has dense traffic, smog, and poor winter visibility. Keep safe distance and use low beams.",
        "Kolkata": "Kolkata has narrow roads and heavy monsoon flooding. Avoid underpasses during rain.",
        "Chennai": "Chennai is prone to cyclonic weather. Stay updated on weather alerts during monsoon.",
        "Bangalore": "Bangalore has frequent road construction and potholes. Watch for diversions and uneven surfaces.",
        "Hyderabad": "Hyderabad has fast-expanding road networks. Watch for unmarked speed breakers.",
        "Pune": "Pune has hilly terrain on outskirts. Drive carefully on expressway curves.",
        "Ahmedabad": "Ahmedabad has wide roads but aggressive driving patterns. Maintain lane discipline.",
        "Jaipur": "Jaipur has mixed traffic with heavy vehicles and animals. Stay alert at intersections.",
        "Lucknow": "Lucknow has narrow old-city roads. Be cautious in congested areas.",
        "Chandigarh": "Chandigarh has well-planned roads but high-speed traffic. Obey speed limits.",
        "Bhopal": "Bhopal has hilly roads with sharp turns. Use low gear on slopes.",
        "Indore": "Indore has rapid urbanization — watch for ongoing construction zones.",
        "Patna": "Patna has poor road infrastructure in many areas. Drive cautiously on damaged roads.",
        "Nagpur": "Nagpur is a major highway junction. Stay alert for heavy trucks.",
        "Kochi": "Kochi receives heavy rainfall. Roads can be slippery and waterlogged.",
        "Guwahati": "Guwahati has hilly terrain and frequent landslides during monsoon.",
        "Dehradun": "Dehradun has mountain roads with steep curves. Avoid overtaking on blind turns.",
        "Surat": "Surat has fast traffic on BRTS corridors. Follow bus lane rules.",
        "Visakhapatnam": "Visakhapatnam has coastal weather and cyclone risk. Check alerts before traveling.",
    }
    if location_v in loc_tips:
        tips.append(("📍", loc_tips[location_v]))

    return tips

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
# PREDICT — Risk Score System
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
elif page == "Predict":
    st.markdown('<div class="section-title">⚡ RISK ASSESSMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Predict Accident Risk</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Select conditions below to calculate a risk score (0–100) based on weighted analysis of time, weather, road type, and location.</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        p_time = st.selectbox("🕐 Time of Day", TIME_OPTIONS)
    with c2:
        p_weather = st.selectbox("🌤️ Weather", WEATHER_OPTIONS)
    with c3:
        p_road = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
    with c4:
        p_location = st.selectbox("📍 Location", LOCATION_OPTIONS)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<p style='color:#2563eb;font-weight:600;margin-top:8px'>📍 Selected Location: {p_location}</p>", unsafe_allow_html=True)

    if st.button("🔍 Predict Risk", use_container_width=True):
        score, t_w, w_w, r_w, l_w = calculate_risk_score(p_time, p_weather, p_road, p_location)
        level, css_key = classify_risk(score)

        risk_emoji = {"Low": "✅", "Medium": "⚠️", "High": "🚨"}
        css_class = {"Low": "alert-low", "Medium": "alert-med", "High": "alert-high"}

        st.markdown("---")

        # Score display — big number + progress bar
        left, right = st.columns([1, 1])

        with left:
            st.markdown(f'''
            <div class="card score-ring">
                <div class="label-text">Risk Score</div>
                <div class="number {css_key}">{score}</div>
                <div class="label-text" style="margin-top:4px">out of 100</div>
            </div>
            ''', unsafe_allow_html=True)

        with right:
            st.markdown(f'''
            <div class="{css_class[level]}" style="padding:32px 20px;text-align:center;height:100%">
                <div style="font-size:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:0.12em;color:#64748b;margin-bottom:8px">Risk Level</div>
                <div class="level">{risk_emoji[level]} {level} Risk</div>
            </div>
            ''', unsafe_allow_html=True)

        # Progress bar
        st.progress(min(score, 100))

        st.markdown("")

        # Breakdown cards
        st.markdown('<div class="section-title" style="margin-bottom:12px">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            st.markdown(f'<div class="breakdown-card"><div class="bk-label">🕐 Time</div><div class="bk-value">{p_time}</div><div class="bk-weight">Weight: {t_w}/80</div></div>', unsafe_allow_html=True)
        with b2:
            st.markdown(f'<div class="breakdown-card"><div class="bk-label">🌤️ Weather</div><div class="bk-value">{p_weather}</div><div class="bk-weight">Weight: {w_w}/70</div></div>', unsafe_allow_html=True)
        with b3:
            st.markdown(f'<div class="breakdown-card"><div class="bk-label">🛣️ Road Type</div><div class="bk-value">{p_road}</div><div class="bk-weight">Weight: {r_w}/70</div></div>', unsafe_allow_html=True)
        with b4:
            st.markdown(f'<div class="breakdown-card"><div class="bk-label">📍 Location</div><div class="bk-value">{p_location}</div><div class="bk-weight">Bonus: +{l_w}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        st.markdown(f'<div class="chart-insight">💡 Score = ({t_w} + {w_w} + {r_w}) / 3 + {l_w} = <b>{score}</b> → Classification: <b>{level} Risk</b></div>', unsafe_allow_html=True)

        # Smart Recommendations
        tips = get_recommendations(p_time, p_weather, p_road, p_location, level)
        items_html = "".join(
            f'<div class="reco-item"><span class="reco-icon">{icon}</span><span>{text}</span></div>'
            for icon, text in tips
        )
        st.markdown(f'''
        <div class="reco-card">
            <div class="reco-title {css_key}">🛡️ Safety Recommendations</div>
            {items_html}
        </div>
        ''', unsafe_allow_html=True)

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
        # Location filter
        if "location" in df.columns and not df["location"].isna().all():
            loc_filter = st.selectbox("📍 Filter by Location", ["All Locations"] + LOCATION_OPTIONS)
            if loc_filter != "All Locations":
                df = df[df["location"] == loc_filter]
                st.markdown(f"<p style='color:#2563eb;font-weight:600'>📍 Showing data for: {loc_filter} ({len(df)} records)</p>", unsafe_allow_html=True)
                if df.empty:
                    st.info(f"No records found for {loc_filter}. Add some data first.")
                    st.stop()
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
            location_v = st.selectbox("📍 Location", LOCATION_OPTIONS)
        with c2:
            road_v = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
            severity_v = st.selectbox("⚠️ Severity Level", SEVERITY_OPTIONS)

        submitted = st.form_submit_button("➕ Add Record", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        try:
            collection.insert_one({"time": time_v, "weather": weather_v, "road_type": road_v, "severity": severity_v, "location": location_v})
            st.success("Record added successfully ✅")
        except Exception as e:
            st.error(f"Error: {e}")

    df = fetch_data()
    if not df.empty:
        st.markdown("---")
        st.markdown(f'<div class="section-title">RECENT RECORDS ({len(df)} total)</div>', unsafe_allow_html=True)
        st.dataframe(df.tail(8), use_container_width=True, hide_index=True)
