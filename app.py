import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import requests

st.set_page_config(page_title="Accident Risk Analyzer", page_icon="🚦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body { font-family: 'Inter', sans-serif; }
.block-container { padding: 2rem 3rem !important; max-width: 1200px; }
section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
section[data-testid="stSidebar"] .stRadio label { font-size: 15px; font-weight: 500; }
header[data-testid="stHeader"] { background: transparent; }

.card {
    background: var(--secondary-background-color, #ffffff); 
    border: 1px solid var(--border-color, #e2e8f0); 
    border-radius: 16px;
    padding: 28px; margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    color: var(--text-color, #1e293b);
}

.hero { text-align: center; padding: 48px 20px 36px; }
.hero h1 { font-size: 3rem; font-weight: 800; color: var(--text-color, #0f172a); margin: 0; line-height: 1.15; }
.hero .accent { background: linear-gradient(135deg, #2563eb, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { font-size: 1.1rem; color: var(--text-color, #64748b); opacity: 0.85; margin-top: 16px; max-width: 560px; margin-left: auto; margin-right: auto; }

.stat-card {
    background: var(--secondary-background-color, #ffffff); 
    border: 1px solid var(--border-color, #e2e8f0); 
    border-radius: 14px;
    padding: 22px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stat-card .value { font-size: 2rem; font-weight: 700; color: var(--text-color, #0f172a); }
.stat-card .label { font-size: 0.8rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }

.alert-low { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px; text-align: center; }
.alert-low .level { font-size: 1.8rem; font-weight: 700; color: #16a34a; }
.alert-med { background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 20px; text-align: center; }
.alert-med .level { font-size: 1.8rem; font-weight: 700; color: #d97706; }
.alert-high { background: #fef2f2; border: 1px solid #fecaca; border-radius: 12px; padding: 20px; text-align: center; }
.alert-high .level { font-size: 1.8rem; font-weight: 700; color: #dc2626; }

.section-title { font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 4px; }
.section-heading { font-size: 1.75rem; font-weight: 700; color: var(--text-color, #0f172a); margin-bottom: 6px; }
.section-desc { font-size: 0.95rem; color: var(--text-color, #64748b); opacity: 0.8; margin-bottom: 24px; }

.chart-insight { background: var(--secondary-background-color, #f8fafc); border-left: 3px solid #2563eb; padding: 10px 14px; margin-top: 10px; border-radius: 0 8px 8px 0; font-size: 0.85rem; color: var(--text-color, #475569); }

.score-ring { text-align: center; padding: 32px 20px; }
.score-ring .number { font-size: 4rem; font-weight: 800; line-height: 1; }
.score-ring .number.low { color: #16a34a; }
.score-ring .number.med { color: #d97706; }
.score-ring .number.high { color: #dc2626; }
.score-ring .label-text { font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.12em; color: #94a3b8; margin-top: 8px; }
.breakdown-card { background: var(--secondary-background-color, #f8fafc); border: 1px solid var(--border-color, #e2e8f0); border-radius: 12px; padding: 16px; text-align: center; }
.breakdown-card .bk-label { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; }
.breakdown-card .bk-value { font-size: 1.1rem; font-weight: 700; color: var(--text-color, #0f172a); margin-top: 4px; }
.breakdown-card .bk-weight { font-size: 0.8rem; color: var(--text-color, #64748b); opacity: 0.8; margin-top: 2px; }

.reco-card { background: var(--secondary-background-color, #ffffff); border: 1px solid var(--border-color, #e2e8f0); border-radius: 14px; padding: 24px 28px; margin-top: 20px; }
.reco-card .reco-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 16px; }
.reco-card .reco-title.low { color: #16a34a; }
.reco-card .reco-title.med { color: #d97706; }
.reco-card .reco-title.high { color: #dc2626; }
.reco-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border-color, #f1f5f9); font-size: 0.9rem; color: var(--text-color, #334155); }
.reco-item:last-child { border-bottom: none; }
.reco-icon { flex-shrink: 0; font-size: 1rem; }

#MainMenu, footer, .stDeployButton { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
button[kind="headerNoPadding"], [data-testid="collapsedControl"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stSidebar button[aria-label*="Collapse"] { display: none !important; }

</style>
""", unsafe_allow_html=True)

load_dotenv()
MONGODB_URI = st.secrets["MONGO_URI"] if "MONGO_URI" in st.secrets else os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB", "traffic_accident_db")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "accidents")

@st.cache_resource
def get_mongo_client():
    return MongoClient(MONGODB_URI)

client = get_mongo_client()
collection = client[MONGODB_DB][MONGODB_COLLECTION]

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

TIME_WEIGHTS = {"Morning": 20, "Afternoon": 30, "Evening": 50, "Night": 80}
WEATHER_WEIGHTS = {"Clear": 10, "Rain": 60, "Fog": 70}
ROAD_WEIGHTS = {"City": 30, "Highway": 70, "Rural": 50}
LOCATION_WEIGHTS = {
    "Mumbai": 10, "Delhi": 8, "Kolkata": 7, "Chennai": 7, "Bangalore": 5,
    "Hyderabad": 5, "Pune": 5, "Ahmedabad": 5, "Lucknow": 6, "Patna": 7,
    "Jaipur": 4, "Chandigarh": 3, "Bhopal": 4, "Indore": 4, "Nagpur": 4,
    "Kochi": 5, "Guwahati": 6, "Dehradun": 5, "Surat": 5, "Visakhapatnam": 4,
}

def fetch_live_weather(city):
    api_key = st.secrets["WEATHER_API_KEY"] if "WEATHER_API_KEY" in st.secrets else os.getenv("OPENWEATHER_API_KEY", "")
    if not api_key:
        return None, None
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            raw_weather = data["weather"][0]["main"]
            temp_k = data.get("main", {}).get("temp")
            temp_c = round(temp_k - 273.15) if temp_k else None
            
            if raw_weather in ["Clear"]:
                mapped_weather = "Clear"
            elif raw_weather in ["Rain", "Drizzle", "Thunderstorm"]:
                mapped_weather = "Rain"
            elif raw_weather in ["Fog", "Mist", "Haze", "Smoke"]:
                mapped_weather = "Fog"
            else:
                mapped_weather = "Clear"
                
            return mapped_weather, raw_weather
        else:
            return None, None
    except Exception:
        return None, None

def fetch_data():
    docs = list(collection.find({}, {"_id": 0}))
    if not docs:
        return pd.DataFrame(columns=["time", "weather", "road_type", "severity", "location"])
    return pd.DataFrame(docs)

def display_html_table(df):
    cols = ["time", "weather", "road_type", "location", "severity"]
    existing_cols = [c for c in cols if c in df.columns]
    df_subset = df[existing_cols].copy()
    df_subset.columns = [c.replace("_", " ").title() for c in df_subset.columns]
    html = df_subset.to_html(index=False, classes="custom-table", border=0)
    
    styled_html = f"""<style>
.table-container {{
    width: 100%;
    overflow-x: auto;
    background: #ffffff;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    margin-top: 10px;
    margin-bottom: 20px;
}}
.custom-table {{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-family: 'Inter', sans-serif;
}}
.custom-table th {{
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 14px 20px;
    border-bottom: 1px solid #edf2f7;
}}
.custom-table td {{
    padding: 14px 20px;
    font-size: 0.9rem;
    color: #1e293b;
    border-bottom: 1px solid #f1f5f9;
}}
.custom-table tr:last-child td {{
    border-bottom: none;
}}
.custom-table tr:hover {{
    background-color: #f8fafc;
}}
</style>
<div class="table-container">
    {html}
</div>"""
    st.markdown(styled_html, unsafe_allow_html=True)

def calculate_risk_score(time_v, weather_v, road_v, location_v):
    t = TIME_WEIGHTS[time_v]
    w = WEATHER_WEIGHTS[weather_v]
    r = ROAD_WEIGHTS[road_v]
    l = LOCATION_WEIGHTS.get(location_v, 0)
    score = min(round((t + w + r) / 3 + l), 100)
    return score, t, w, r, l

def classify_risk(score):
    if score <= 40:
        return "Low", "low"
    elif score <= 70:
        return "Medium", "med"
    else:
        return "High", "high"

def get_recommendations(time_v, weather_v, road_v, location_v, level):
    tips = []

    if level == "High":
        tips.append(("🚨", "High-risk conditions detected. Avoid travel if possible."))
        tips.append(("🛑", "If travel is necessary, inform someone of your route and ETA."))
    elif level == "Medium":
        tips.append(("⚠️", "Moderate risk detected. Exercise extra caution while driving."))
    else:
        tips.append(("✅", "Conditions are relatively safe. Follow standard driving practices."))

    if time_v == "Night":
        tips.append(("🌙", "Avoid late-night travel if possible. Visibility is significantly reduced."))
        tips.append(("💡", "Use high-beam headlights on empty roads, low-beam when traffic is near."))
    elif time_v == "Evening":
        tips.append(("🌆", "Be cautious during peak traffic hours. Stay alert for sudden stops."))
    elif time_v == "Morning":
        tips.append(("🌅", "Watch for sun glare during early morning hours."))

    if weather_v == "Rain":
        tips.append(("🌧️", "Drive slowly — roads may be slippery. Increase following distance."))
        tips.append(("🚗", "Avoid sudden braking and sharp turns on wet surfaces."))
    elif weather_v == "Fog":
        tips.append(("🌫️", "Use fog lights and maintain a safe following distance."))
        tips.append(("🐌", "Reduce speed significantly. Avoid overtaking other vehicles."))

    if road_v == "Highway":
        tips.append(("🛣️", "Maintain speed limits and stay alert for lane changes."))
        tips.append(("🔄", "Take regular breaks on long highway drives to avoid fatigue."))
    elif road_v == "Rural":
        tips.append(("🏔️", "Watch for unmarked roads, sharp curves, and wildlife."))
    elif road_v == "City":
        tips.append(("🏙️", "Watch for pedestrians, cyclists, and frequent signal changes."))

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

with st.sidebar:
    st.markdown("### 🚦 Accident Risk Analyzer")
    st.markdown("<p style='color:#64748b;font-size:13px;margin-top:-10px'>Data-driven safety insights</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", ["Home", "Predict", "Map", "Insights", "Add Data"], label_visibility="collapsed")

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
        display_html_table(df.tail(10))

elif page == "Predict":
    st.markdown('<div class="section-title">⚡ RISK ASSESSMENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Predict Accident Risk</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Select conditions below to calculate a risk score (0–100) based on weighted analysis of time, weather, road type, and location.</div>', unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            p_time = st.selectbox("🕐 Time of Day", TIME_OPTIONS)
        with c2:
            p_road = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
        with c3:
            p_location = st.selectbox("📍 Location", LOCATION_OPTIONS)

    live_w, raw_w = fetch_live_weather(p_location)
    weather_emoji = {"Clear": "☀️", "Rain": "🌧️", "Fog": "🌫️"}

    if live_w:
        p_weather = live_w
        st.markdown(f"<div class='weather-card' style='padding: 16px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; margin-top: 12px; margin-bottom: 16px; display: flex; align-items: center; gap: 10px;'><span style='font-size: 1.5rem;'>{weather_emoji.get(live_w, '🌦')}</span><div><div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b;'>Current Weather in {p_location}</div><div style='font-size: 1.1rem; font-weight: 700; color: #0f172a;'>{raw_w}</div></div></div>", unsafe_allow_html=True)
    else:
        p_weather = "Clear"
        st.error("⚠️ Unable to fetch weather")
        st.info("ℹ️ Falling back to default weather (Clear)")

    st.markdown(f"<p style='color:#2563eb;font-weight:600;margin-top:8px'>📍 Selected Location: {p_location}</p>", unsafe_allow_html=True)

    if st.button("🔍 Predict Risk", use_container_width=True):
        score, t_w, w_w, r_w, l_w = calculate_risk_score(p_time, p_weather, p_road, p_location)
        level, css_key = classify_risk(score)

        risk_emoji = {"Low": "✅", "Medium": "⚠️", "High": "🚨"}
        css_class = {"Low": "alert-low", "Medium": "alert-med", "High": "alert-high"}

        st.markdown("---")

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

        st.progress(min(score, 100))
        st.markdown("")

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

elif page == "Map":
    st.markdown('<div class="section-title">🗺️ ACCIDENT RISK MAP</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Geographical Risk Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Analyze safety levels geographically using actual user entry data mapped across India.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    df = fetch_data()

    if df.empty:
        st.info("No data available to display on map. Go to **Add Data** to insert records.")
    else:
        import folium
        
        CITY_COORDS = {
            "Delhi": [28.6139, 77.2090], "Mumbai": [19.0760, 72.8777],
            "Bangalore": [12.9716, 77.5946], "Chennai": [13.0827, 80.2707],
            "Kolkata": [22.5726, 88.3639], "Hyderabad": [17.3850, 78.4867],
            "Pune": [18.5204, 73.8567], "Ahmedabad": [23.0225, 72.5714],
            "Jaipur": [26.9124, 75.7873], "Lucknow": [26.8467, 80.9462],
            "Chandigarh": [30.7333, 76.7794], "Bhopal": [23.2599, 77.4126],
            "Indore": [22.7196, 75.8577], "Patna": [25.5941, 85.1376],
            "Nagpur": [21.1458, 79.0882], "Kochi": [9.9312, 76.2673],
            "Guwahati": [26.1445, 91.7362], "Dehradun": [30.3165, 78.0322],
            "Surat": [21.1702, 72.8311], "Visakhapatnam": [17.6868, 83.2185]
        }

        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
        
        markers_added = 0
        for _, row in df.iterrows():
            loc = row.get("location")
            if loc in CITY_COORDS:
                coords = CITY_COORDS[loc]
                t_v = row.get("time", "Morning")
                w_v = row.get("weather", "Clear")
                r_v = row.get("road_type", "City")
                
                score, _, _, _, _ = calculate_risk_score(t_v, w_v, r_v, loc)
                
                if score <= 40:
                    color = "#22c55e"
                elif score <= 70:
                    color = "#f97316"
                else:
                    color = "#ef4444"
                    
                popup_text = f"<b>{loc}</b> — Risk: {score}%<br><i>{t_v} | {w_v} | {r_v}</i>"
                
                folium.CircleMarker(
                    location=coords,
                    radius=10,
                    popup=folium.Popup(popup_text, max_width=200),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7
                ).add_to(m)
                markers_added += 1
                
        if markers_added == 0:
            st.warning("No records with valid location coordinates found.")
        else:
            st.components.v1.html(m._repr_html_(), height=550)

elif page == "Insights":
    st.markdown('<div class="section-title">📊 DATA ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Insights & Visualizations</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Explore accident patterns with dynamic analytical tools.</div>', unsafe_allow_html=True)

    df = fetch_data()

    if df.empty:
        st.info("No data available yet. Go to **Add Data** to insert records.")
    else:
        with st.container(border=True):
            st.markdown("<h4 style='margin-top:0;'>🔍 Data Filters</h4>", unsafe_allow_html=True)
            f1, f2, f3, f4, f5 = st.columns(5)
            with f1:
                loc_filter = st.selectbox("Location", ["All"] + LOCATION_OPTIONS)
            with f2:
                time_filter = st.selectbox("Time", ["All"] + TIME_OPTIONS)
            with f3:
                weather_filter = st.selectbox("Weather", ["All"] + WEATHER_OPTIONS)
            with f4:
                road_filter = st.selectbox("Road Type", ["All"] + ROAD_TYPE_OPTIONS)
            with f5:
                sev_filter = st.selectbox("Severity", ["All"] + SEVERITY_OPTIONS)

            search_q = st.text_input("🔍 Search records (e.g. 'Delhi', 'Rain')", placeholder="Type to search all columns...")

        filtered_df = df.copy()
        if loc_filter != "All":
            filtered_df = filtered_df[filtered_df["location"] == loc_filter]
        if time_filter != "All":
            filtered_df = filtered_df[filtered_df["time"] == time_filter]
        if weather_filter != "All":
            filtered_df = filtered_df[filtered_df["weather"] == weather_filter]
        if road_filter != "All":
            filtered_df = filtered_df[filtered_df["road_type"] == road_filter]
        if sev_filter != "All":
            filtered_df = filtered_df[filtered_df["severity"] == sev_filter]

        if search_q:
            mask = filtered_df.apply(lambda r: r.astype(str).str.contains(search_q, case=False).any(), axis=1)
            filtered_df = filtered_df[mask]

        if filtered_df.empty:
            st.warning("No matching records found matching the search/filter criteria.")
        else:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("📊 Total Records", len(filtered_df))
            with m2:
                st.metric("🚨 High Risk", len(filtered_df[filtered_df["severity"] == "High"]))
            with m3:
                st.metric("⚠️ Medium Risk", len(filtered_df[filtered_df["severity"] == "Medium"]))
            with m4:
                st.metric("✅ Low Risk", len(filtered_df[filtered_df["severity"] == "Low"]))
            
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name="filtered_accident_data.csv", mime="text/csv", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            sns.set_theme(style="whitegrid", font="Inter")

            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True):
                    st.markdown("<div style='font-weight: 600; font-size: 1.05rem; margin-bottom: 10px; color: #0f172a;'>🌤️ Accidents by Weather</div>", unsafe_allow_html=True)
                    fig, ax = plt.subplots(figsize=(4.5, 2.5))
                    sns.countplot(data=filtered_df, x="weather", order=WEATHER_OPTIONS, palette=["#3b82f6","#06b6d4","#8b5cf6"], ax=ax)
                    ax.set_xlabel(""); ax.set_ylabel("Count")
                    for spine in ax.spines.values(): spine.set_visible(False)
                    plt.tight_layout()
                    st.pyplot(fig)
                    st.markdown('<div class="chart-insight" style="margin-top: 12px;">💡 Live dataset counts plotted against core weather categories.</div>', unsafe_allow_html=True)

            with c2:
                with st.container(border=True):
                    st.markdown("<div style='font-weight: 600; font-size: 1.05rem; margin-bottom: 10px; color: #0f172a;'>🕐 Accident Trend by Time</div>", unsafe_allow_html=True)
                    time_counts = filtered_df["time"].value_counts().reindex(TIME_OPTIONS, fill_value=0)
                    fig2, ax2 = plt.subplots(figsize=(4.5, 2.5))
                    ax2.plot(time_counts.index, time_counts.values, marker="o", linewidth=2.5, color="#2563eb", markersize=8)
                    ax2.fill_between(time_counts.index, time_counts.values, alpha=0.08, color="#2563eb")
                    ax2.set_xlabel(""); ax2.set_ylabel("Count")
                    for spine in ax2.spines.values(): spine.set_visible(False)
                    plt.tight_layout()
                    st.pyplot(fig2)
                    st.markdown('<div class="chart-insight" style="margin-top: 12px;">💡 Visual trends shifting across morning vs evening peaks.</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            c3, c4 = st.columns(2)
            with c3:
                with st.container(border=True):
                    st.markdown("<div style='font-weight: 600; font-size: 1.05rem; margin-bottom: 10px; color: #0f172a;'>⚠️ Severity Distribution</div>", unsafe_allow_html=True)
                    fig3, ax3 = plt.subplots(figsize=(4.5, 2.5))
                    sev = filtered_df["severity"].value_counts()
                    colors = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
                    ax3.pie(sev.values, labels=sev.index, autopct="%1.0f%%",
                            colors=[colors.get(l, "#94a3b8") for l in sev.index],
                            startangle=90, wedgeprops={"linewidth": 2, "edgecolor": "white"},
                            textprops={'fontsize': 9})
                    plt.tight_layout()
                    st.pyplot(fig3)
                    st.markdown('<div class="chart-insight" style="margin-top: 12px;">💡 Breakdown percentages comparing severity scales.</div>', unsafe_allow_html=True)

            with c4:
                with st.container(border=True):
                    st.markdown("<div style='font-weight: 600; font-size: 1.05rem; margin-bottom: 10px; color: #0f172a;'>📦 Severity by Road Type</div>", unsafe_allow_html=True)
                    sev_map = {"Low": 1, "Medium": 2, "High": 3}
                    df_box = filtered_df.copy()
                    df_box["severity_code"] = df_box["severity"].map(sev_map)
                    fig4, ax4 = plt.subplots(figsize=(4.5, 2.5))
                    sns.boxplot(data=df_box, x="road_type", y="severity_code", order=ROAD_TYPE_OPTIONS,
                                palette=["#3b82f6","#06b6d4","#8b5cf6"], ax=ax4)
                    ax4.set_xlabel(""); ax4.set_ylabel("Severity (1-Low, 3-High)")
                    for spine in ax4.spines.values(): spine.set_visible(False)
                    plt.tight_layout()
                    st.pyplot(fig4)
                    st.markdown('<div class="chart-insight" style="margin-top: 12px;">💡 Median score ranges defined natively per road category.</div>', unsafe_allow_html=True)

            st.markdown("")
            with st.container(border=True):
                st.markdown("<h4 style='margin-top:0;'>📋 Filtered Data Workspace</h4>", unsafe_allow_html=True)
                st.dataframe(filtered_df, use_container_width=True)


elif page == "Add Data":
    st.markdown('<div class="section-title">📝 DATA ENTRY</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Add New Accident Record</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Enter accident details below. Records are saved instantly to MongoDB Atlas.</div>', unsafe_allow_html=True)

    with st.container(border=True):
        with st.form("add_form", clear_on_submit=True):
            row1_col1, row1_col2 = st.columns(2)
            with row1_col1:
                time_v = st.selectbox("🕐 Time of Day", TIME_OPTIONS)
            with row1_col2:
                weather_v = st.selectbox("🌤️ Weather Condition", WEATHER_OPTIONS)

            row2_col1, row2_col2, row2_col3 = st.columns(3)
            with row2_col1:
                road_v = st.selectbox("🛣️ Road Type", ROAD_TYPE_OPTIONS)
            with row2_col2:
                severity_v = st.selectbox("⚠️ Severity Level", SEVERITY_OPTIONS)
            with row2_col3:
                location_v = st.selectbox("📍 Location", LOCATION_OPTIONS)

            submitted = st.form_submit_button("➕ Add Record", use_container_width=True)

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
        display_html_table(df.tail(8))
