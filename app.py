import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from datetime import datetime
from scipy import stats
from scipy.stats import ttest_ind, f_oneway, chi2_contingency, shapiro, levene
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    filename='yulu_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.info("="*50)
logger.info("Yulu Application Started")
logger.info("="*50)

# Page Configuration
st.set_page_config(
    page_title="Yulu Bike Sharing Analysis",
    layout="wide",
    page_icon="🚴",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS matching Aerofit style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    .block-container {
        background: rgba(17, 24, 39, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    h1 {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-in-out;
        letter-spacing: -1px;
    }
    h2 { 
        color: #f3f4f6 !important; 
        border-bottom: 3px solid #8b5cf6; 
        padding-bottom: 0.5rem; 
        margin-top: 2rem; 
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(139, 92, 246, 0.3);
    }
    h3 { 
        color: #e5e7eb !important; 
        margin-top: 1.5rem; 
        font-weight: 600 !important; 
    }
    p, li, span, div { color: #cbd5e1; }
    
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    [data-testid="stMetricLabel"] { 
        color: #9ca3af !important; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { 
        gap: 12px; 
        background-color: rgba(17, 24, 39, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
        color: #a78bfa; 
        border-radius: 10px; 
        padding: 12px 24px; 
        font-weight: 600; 
        transition: all 0.3s ease; 
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    .stTabs [data-baseweb="tab"]:hover { 
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
        transform: translateY(-2px); 
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%) !important; 
        color: white !important; 
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
        transform: translateY(-2px);
    }
    
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%); 
        border-right: 1px solid rgba(139, 92, 246, 0.3);
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 { 
        color: white !important; 
        -webkit-text-fill-color: white !important; 
    }
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] span { 
        color: #cbd5e1 !important; 
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
        color: white; 
        border-radius: 12px; 
        padding: 0.75rem 2rem; 
        font-weight: 600; 
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); 
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.6); 
        color: white; 
    }
    
    @keyframes fadeInDown { 
        from { opacity: 0; transform: translateY(-30px); } 
        to { opacity: 1; transform: translateY(0); } 
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .card {
        padding: 1rem; 
        border-radius: 16px; 
        text-align: center; 
        color: white; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.4); 
        transition: all 0.4s ease; 
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    .card:hover::before {
        left: 100%;
    }
    .card:hover { 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(244, 114, 182, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(244, 114, 182, 0.2) 100%);
        border-color: rgba(139, 92, 246, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
    }
    
    .stExpander {
        background: rgba(17, 24, 39, 0.5);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
    }
    
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
<div style='position: fixed; top: 3.5rem; right: 1.5rem; z-index: 9999;'>
    <div style='background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); 
                border-radius: 20px; padding: 0.6rem 1.2rem; 
                box-shadow: 0 4px 20px rgba(139, 92, 246, 0.5);
                animation: fadeInDown 1s ease-in-out;'>
        <span style='color: white; font-weight: 700; font-size: 0.9rem; letter-spacing: 1.5px;'>
            ✨ By RATNESH SINGH
        </span>
    </div>
</div>
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='font-size: 4rem; margin-bottom: 0;'>🚴 Yulu Bike Sharing Analytics</h1>
    <p style='font-size: 1.3rem; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-top: 0.5rem; letter-spacing: 1px;'>
        🎯 Hypothesis Testing & Demand Prediction Analysis
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Feature Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>📊</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Data</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>10,886 Records</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>🔍</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>EDA</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Visual Analysis</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>🔬</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Testing</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Hypothesis Tests</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class='card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <div style='font-size: 2rem; margin-bottom: 0.25rem;'>💡</div>
        <h3 style='color: white !important; margin: 0.25rem 0; font-size: 1.1rem;'>Insights</h3>
        <p style='margin: 0; font-size: 0.8rem; color: rgba(255,255,255,0.8);'>Recommendations</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Enhanced Sidebar
with st.sidebar:
    st.markdown("## 📑 Navigation")
    st.markdown("---")
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(139, 92, 246, 0.3);'>
        <h3 style='color: #a78bfa !important; margin-top: 0;'>📊 Project Overview</h3>
        <p><strong>Company:</strong> Yulu - India's leading micro-mobility provider</p>
        <p><strong>Goal:</strong> Identify factors affecting bike demand</p>
        <p><strong>Period:</strong> 2011-2012</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(244, 114, 182, 0.3);'>
        <h3 style='color: #f472b6 !important; margin-top: 0;'>🔍 Analysis Steps</h3>
        <ul style='margin: 0; padding-left: 1.2rem;'>
            <li>Data Loading & Preprocessing</li>
            <li>Univariate & Bivariate EDA</li>
            <li>Statistical Hypothesis Testing</li>
            <li>Insights & Recommendations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border: 1px solid rgba(56, 239, 125, 0.3);'>
        <h3 style='color: #38ef7d !important; margin-top: 0;'>💡 Key Findings</h3>
        <p>✓ <strong>Season:</strong> Significant impact on demand</p>
        <p>✓ <strong>Weather:</strong> Strong correlation</p>
        <p>✓ <strong>Temperature:</strong> +0.63 correlation</p>
    </div>
    """, unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    logger.info("Loading dataset...")
    try:
        try:
            df = pd.read_csv("yulu_data.csv")
        except:
            df = pd.read_csv("bike_sharing.txt")
        
        logger.info(f"Dataset loaded: {df.shape}")
        
        # Preprocessing
        data = df.copy()
        
        data["weather"].replace({1: "Clear", 2: "Cloudy", 3: "Little Rain", 4: "Heavy Rain"}, inplace=True)
        data["season"].replace({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}, inplace=True)
        data["workingday"].replace({1: "Yes", 0: "No"}, inplace=True)
        data["holiday"].replace({1: "Yes", 0: "No"}, inplace=True)
        
        data["datetime"] = pd.to_datetime(data["datetime"])
        data["day"] = data["datetime"].dt.day_name()
        data["date"] = data["datetime"].dt.date
        data["hour"] = data["datetime"].dt.hour
        data["Month"] = data["datetime"].dt.month
        data["Month_name"] = data["datetime"].dt.month_name()
        data["year"] = data["datetime"].dt.year
        
        def get_temp(temp):
            if temp <= 12: return "Very Low"
            elif temp > 12 and temp < 24: return "Low"
            elif temp >= 24 and temp < 35: return "Moderate"
            elif temp >= 35: return "High"
        
        data["temperature"] = data["atemp"].apply(get_temp)
        
        def get_humidity(H):
            if 0 <= H <= 10: return "10%"
            elif 11 <= H <= 20: return "20%"
            elif 21 <= H <= 30: return "30%"
            elif 31 <= H <= 40: return "40%"
            elif 41 <= H <= 50: return "50%"
            elif 51 <= H <= 60: return "60%"
            elif 61 <= H <= 70: return "70%"
            elif 71 <= H <= 80: return "80%"
            elif 81 <= H <= 90: return "90%"
            elif 91 <= H <= 100: return "100%"
        
        data["humidity_level"] = data["humidity"].apply(get_humidity)
        
        def get_windspeed(W):
            if 0 <= W <= 10: return "Low"
            elif 11 <= W <= 20: return "Moderate"
            elif 21 <= W <= 30: return "High"
            elif W > 30: return "Very High"
        
        data["windspeed_level"] = data["windspeed"].apply(get_windspeed)
        
        logger.info("Preprocessing completed")
        return data
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        st.error(f"Error loading data: {str(e)}")
        return None

try:
    df = load_data()
    logger.info("Data ready")
except Exception as e:
    logger.error(f"Failed to load data: {str(e)}")
    st.error("❌ Failed to load data")
    st.stop()

# Main Tabs
tabs = st.tabs([
    "📊 Problem Statement",
    "🔍 Interactive EDA", 
    "📈 Univariate Analysis",
    "🔗 Bivariate Analysis",
    "🔬 Hypothesis Testing",
    "💡 Insights & Recommendations",
    "📚 Complete Analysis",
    "📝 Logs"
])

logger.info("Main tabs created")

# TAB 1: Problem Statement
with tabs[0]:
    st.header("📊 About Yulu & Problem Statement")
    logger.info("Problem Statement tab accessed")
    
    # Enhanced Metrics with Gradient Cards
    st.markdown("""
    <style>
        .metric-container {
            background: rgba(17, 24, 39, 0.7);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid rgba(139, 92, 246, 0.2);
            transition: all 0.3s ease;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
            border-color: rgba(139, 92, 246, 0.5);
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0.5rem 0;
        }
        .metric-label {
            color: #94a3b8;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }
        .metric-icon {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
            background: rgba(139, 92, 246, 0.1);
            width: 50px;
            height: 50px;
            line-height: 50px;
            border-radius: 50%;
            margin: 0 auto 1rem auto;
        }
    </style>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-icon" style="color: #667eea;">📊</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Records</div>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 0.5rem;">Hourly Data Points</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-icon" style="color: #f472b6;">🧩</div>
            <div class="metric-value">{df.shape[1]}</div>
            <div class="metric-label">Features</div>
            <div style="font-size: 0.8rem; color: #f472b6; margin-top: 0.5rem;">Analytical Columns</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-icon" style="color: #38ef7d;">🚲</div>
            <div class="metric-value">{df['count'].sum() // 1000}k+</div>
            <div class="metric-label">Total Rentals</div>
            <div style="font-size: 0.8rem; color: #38ef7d; margin-top: 0.5rem;">Bikes Rented</div>
        </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-icon" style="color: #fb923c;">⚡</div>
            <div class="metric-value">{df['count'].mean():.1f}</div>
            <div class="metric-label">Avg / Hour</div>
            <div style="font-size: 0.8rem; color: #fb923c; margin-top: 0.5rem;">Demand Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # About Yulu & Business Challenge in a Grid
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown("""
        <div style='background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)); 
                    padding: 2rem; border-radius: 20px; border: 1px solid rgba(102, 126, 234, 0.3); height: 100%;'>
            <h3 style='color: #8b5cf6 !important; margin-top: 0; display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 2rem;'>🚴</span> About Yulu
            </h3>
            <p style='color: #cbd5e1; line-height: 1.8; font-size: 1.05rem;'>
                <strong>Yulu</strong> is India's leading micro-mobility service provider, revolutionizing daily commutes. 
                Starting as a mission to eliminate traffic congestion, Yulu provides safe, shared, and sustainable 
                commuting solutions through a user-friendly mobile app.
            </p>
            <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; margin-top: 1.5rem;'>
                <p style='color: #a5b4fc; margin: 0; font-size: 0.95rem;'>
                    <strong>📍 Key Zones:</strong> Metro stations, bus stands, office spaces, residential areas, and corporate hubs.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style='background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9)); 
                    padding: 2rem; border-radius: 20px; border: 1px solid rgba(244, 114, 182, 0.3); height: 100%;'>
            <h3 style='color: #ec4899 !important; margin-top: 0; display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 2rem;'>⚠️</span> The Challenge
            </h3>
            <p style='color: #cbd5e1; line-height: 1.6;'>
                Yulu has experienced a recent dip in revenues. The company needs to understand:
            </p>
            <ul style='color: #f472b6; margin-bottom: 0;'>
                <li style='margin-bottom: 0.5rem;'>Which variables predict demand?</li>
            <p style='margin: 0; font-size: 0.9rem;'>All {len(df):,} records complete</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <p style='font-size: 2rem; margin: 0; color: #38ef7d;'>✓</p>
            <p style='margin: 0.5rem 0;'><strong>No Duplicates</strong></p>
            <p style='margin: 0; font-size: 0.9rem;'>Clean dataset</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sample Data
    st.subheader("🔍 Sample Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

# TAB 2: Interactive EDA
with tabs[1]:
    st.header("🔍 Interactive Exploratory Data Analysis")
    logger.info("Interactive EDA tab accessed")
    
    viz_tabs = st.tabs(["📊 Overview", "🌡️ Weather Patterns", "⏰ Temporal Patterns", "👥 User Analysis"])
    
    with viz_tabs[0]:
        st.subheader("Dataset Overview")
        
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6; margin-bottom: 1.5rem;'>
            <h4 style='color: #a78bfa; margin-top: 0;'>📊 Understanding the Data</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                This section provides a comprehensive overview of the bike-sharing dataset, including 
                statistical summaries and distribution patterns.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Numerical Features Summary**")
            numerical_cols = ['temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count']
            st.dataframe(df[numerical_cols].describe().T, use_container_width=True)
        
        with col2:
            st.markdown("**Categorical Features**")
            cat_summary = []
            for col in ['season', 'holiday', 'workingday', 'weather']:
                value_counts = df[col].value_counts()
                cat_summary.append({
                    'Feature': col,
                    'Unique': df[col].nunique(),
                    'Most Common': value_counts.index[0],
                    'Frequency': value_counts.values[0]
                })
            st.dataframe(pd.DataFrame(cat_summary), use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Interactive Data Explorer
        st.markdown("**🔍 Interactive Data Explorer**")
        
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            season_filter = st.multiselect("Filter by Season", df['season'].unique(), default=df['season'].unique())
        with col_filter2:
            weather_filter = st.multiselect("Filter by Weather", df['weather'].unique(), default=df['weather'].unique())
        with col_filter3:
            workday_filter = st.multiselect("Filter by Working Day", df['workingday'].unique(), default=df['workingday'].unique())
        
        filtered_df = df[
            (df['season'].isin(season_filter)) & 
            (df['weather'].isin(weather_filter)) &
            (df['workingday'].isin(workday_filter))
        ]
        
        st.info(f"📊 Showing **{len(filtered_df):,}** of **{len(df):,}** records")
        st.dataframe(filtered_df.head(100), use_container_width=True, height=400)
    
    with viz_tabs[1]:
        st.subheader("Weather Pattern Analysis")
        
        st.markdown("""
        <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #f472b6; margin-bottom: 1.5rem;'>
            <h4 style='color: #f472b6; margin-top: 0;'>🌤️ Weather Impact on Rentals</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                Weather conditions play a crucial role in bike rental demand. This analysis examines how seasonal 
                changes and daily weather patterns influence customer behavior and rental volumes. Understanding 
                these patterns helps optimize fleet distribution and pricing strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌸 Season Distribution**")
            st.caption("📌 Distribution of data points across four seasons")
            st.markdown("""
            <div style='background: rgba(102, 126, 234, 0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;'>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.85rem;'>
                    This chart shows how our dataset is distributed across seasons. Each season represents 
                    approximately 3 months of data, helping us understand seasonal variations in bike usage.
                    <br><br>
                    <strong>Key Insight:</strong> Balanced seasonal distribution ensures our analysis captures 
                    all weather patterns throughout the year.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            season_counts = df['season'].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=season_counts.index,
                y=season_counts.values,
                marker=dict(
                    color=['#667eea', '#f093fb', '#11998e', '#fa709a'],
                    line=dict(color='rgba(255,255,255,0.3)', width=2)
                ),
                text=season_counts.values,
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Records: %{y}<br>Percentage: %{y:.1%}<extra></extra>'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Season'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Number of Records'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🌤️ Weather Condition Distribution**")
            st.caption("📌 Proportion of different weather conditions in the dataset")
            st.markdown("""
            <div style='background: rgba(240, 147, 251, 0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;'>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.85rem;'>
                    Weather conditions are categorized into Clear, Cloudy, Light Rain, and Heavy Rain. 
                    This donut chart reveals the frequency of each weather type during the observation period.
                    <br><br>
                    <strong>Key Insight:</strong> Clear weather dominates, but understanding rental patterns 
                    during adverse weather is crucial for operational planning.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            weather_counts = df['weather'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=weather_counts.index,
                values=weather_counts.values,
                hole=0.4,
                marker=dict(colors=['#667eea', '#f093fb', '#11998e', '#fa709a']),
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Average rentals by season and weather
        st.markdown("**📊 Impact Analysis: Rentals vs Environmental Conditions**")
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.05); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;'>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'>
                The following charts compare average bike rentals across different seasons and weather conditions. 
                This analysis reveals which environmental factors drive higher demand, enabling data-driven decisions 
                for inventory management, pricing strategies, and marketing campaigns.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌸 Average Rentals by Season**")
            st.caption("📌 Seasonal demand patterns reveal peak and off-peak periods")
            
            season_avg = df.groupby('season')['count'].mean().reset_index()
            season_avg_sorted = season_avg.sort_values('count', ascending=False)
            
            fig = go.Figure(data=[go.Bar(
                x=season_avg['season'],
                y=season_avg['count'],
                marker=dict(color=['#667eea', '#f093fb', '#11998e', '#fa709a']),
                text=[f'{v:.0f}' for v in season_avg['count']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg Rentals: %{y:.1f}<extra></extra>'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Season'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Average Rentals per Hour'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            best_season = season_avg.loc[season_avg['count'].idxmax(), 'season']
            worst_season = season_avg.loc[season_avg['count'].idxmin(), 'season']
            best_count = season_avg['count'].max()
            worst_count = season_avg['count'].min()
            variation = ((best_count - worst_count) / worst_count * 100)
            
            st.success(f"""
            **📈 Seasonal Insights:**
            - **Peak Season:** {best_season} with **{best_count:.0f}** bikes/hour
            - **Low Season:** {worst_season} with **{worst_count:.0f}** bikes/hour
            - **Variation:** {variation:.1f}% difference between peak and low seasons
            - **Recommendation:** Increase fleet by {variation:.0f}% during {best_season}
            """)
        
        with col2:
            st.markdown("**☀️ Average Rentals by Weather Condition**")
            st.caption("📌 Weather significantly impacts customer willingness to rent bikes")
            
            weather_avg = df.groupby('weather')['count'].mean().reset_index()
            weather_avg_sorted = weather_avg.sort_values('count', ascending=False)
            
            fig = go.Figure(data=[go.Bar(
                x=weather_avg['weather'],
                y=weather_avg['count'],
                marker=dict(
                    color=weather_avg['count'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title='Avg<br>Rentals')
                ),
                text=[f'{v:.0f}' for v in weather_avg['count']],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Avg Rentals: %{y:.1f}<extra></extra>'
            )])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Weather Condition'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Average Rentals per Hour'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            best_weather = weather_avg.loc[weather_avg['count'].idxmax(), 'weather']
            worst_weather = weather_avg.loc[weather_avg['count'].idxmin(), 'weather']
            best_weather_count = weather_avg['count'].max()
            worst_weather_count = weather_avg['count'].min()
            weather_impact = ((best_weather_count - worst_weather_count) / worst_weather_count * 100)
            
            st.info(f"""
            **🌤️ Weather Insights:**
            - **Best Conditions:** {best_weather} with **{best_weather_count:.0f}** bikes/hour
            - **Worst Conditions:** {worst_weather} with **{worst_weather_count:.0f}** bikes/hour
            - **Impact:** {weather_impact:.1f}% drop in adverse weather
            - **Strategy:** Implement dynamic pricing during poor weather to maintain revenue
            """)
    
    with viz_tabs[2]:
        st.subheader("Temporal Pattern Analysis")
        
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #38ef7d; margin-bottom: 1.5rem;'>
            <h4 style='color: #38ef7d; margin-top: 0;'>⏰ Time-Based Demand Patterns</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                Understanding temporal patterns is critical for optimizing bike availability and maximizing revenue. 
                This section analyzes rental patterns across different time scales - hourly, daily, and monthly - 
                revealing peak demand periods and helping predict future trends. These insights drive strategic 
                decisions on fleet management, staffing, and maintenance scheduling.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hourly pattern
        st.markdown("**📈 Hourly Rental Pattern Throughout the Day**")
        st.caption("📌 Identifying peak hours for optimal fleet distribution")
        st.markdown("""
        <div style='background: rgba(139, 92, 246, 0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.85rem;'>
                This line chart shows average bike rentals for each hour of the day (0-23). The pattern reveals 
                commuter behavior with distinct morning and evening peaks, typical of urban bike-sharing systems.
                <br><br>
                <strong>What to Look For:</strong> Two peaks typically appear around 8 AM (morning commute) and 
                5-6 PM (evening commute), with lower demand during late night and early morning hours.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        hourly_data = df.groupby('hour')['count'].mean().reset_index()
        fig = px.line(hourly_data, x='hour', y='count',
                      markers=True)
        fig.update_traces(line_color='#8b5cf6', line_width=3, marker=dict(size=8, color='#ec4899'))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Hour of Day (0-23)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Average Bike Rentals'),
            height=400,
            hovermode='x unified'
        )
        fig.add_annotation(
            x=hourly_data.loc[hourly_data['count'].idxmax(), 'hour'],
            y=hourly_data['count'].max(),
            text=f"Peak: {hourly_data['count'].max():.0f} bikes",
            showarrow=True,
            arrowhead=2,
            arrowcolor='#ec4899',
            font=dict(color='#ec4899', size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        peak_hour = hourly_data.loc[hourly_data['count'].idxmax(), 'hour']
        peak_count = hourly_data['count'].max()
        low_hour = hourly_data.loc[hourly_data['count'].idxmin(), 'hour']
        low_count = hourly_data['count'].min()
        
        st.info(f"""
        **🕐 Hourly Insights:**
        - **Peak Hour:** {peak_hour}:00 with **{peak_count:.0f}** average rentals
        - **Lowest Hour:** {low_hour}:00 with **{low_count:.0f}** average rentals
        - **Peak-to-Low Ratio:** {(peak_count/low_count):.1f}x difference
        - **Action:** Deploy {((peak_count/low_count - 1) * 100):.0f}% more bikes during peak hours
        - **Opportunity:** Implement surge pricing during {peak_hour-1}:00-{peak_hour+2}:00 window
        """)
        
        st.markdown("---")
        
        # Day of week pattern
        st.markdown("**📅 Day of Week Rental Patterns**")
        st.caption("📌 Comparing weekday vs weekend demand")
        st.markdown("""
        <div style='background: rgba(244, 114, 182, 0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.85rem;'>
                This bar chart compares average rentals across all seven days of the week. The pattern helps 
                distinguish between commuter-driven weekday demand and leisure-driven weekend demand.
                <br><br>
                <strong>Business Insight:</strong> Weekday patterns indicate professional commuters, while 
                weekend spikes suggest recreational users. This affects marketing strategies and pricing models.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_data = df.groupby('day')['count'].mean().reindex(day_order).reset_index()
        
        fig = px.bar(daily_data, x='day', y='count',
                     color='count',
                     color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=False, title='Day of Week'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Average Rentals'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        weekday_avg = daily_data[daily_data['day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]['count'].mean()
        weekend_avg = daily_data[daily_data['day'].isin(['Saturday', 'Sunday'])]['count'].mean()
        
        st.success(f"""
        **📊 Weekly Pattern Insights:**
        - **Weekday Average:** {weekday_avg:.0f} bikes/hour
        - **Weekend Average:** {weekend_avg:.0f} bikes/hour
        - **Difference:** {abs(weekday_avg - weekend_avg):.0f} bikes/hour ({'higher' if weekday_avg > weekend_avg else 'lower'} on weekdays)
        - **Strategy:** {'Focus on commuter packages for weekdays' if weekday_avg > weekend_avg else 'Promote leisure rides on weekends'}
        """)
        
        st.markdown("---")
        
        # Monthly pattern
        st.markdown("**📆 Monthly Rental Trends**")
        st.caption("📌 Seasonal variations and year-round demand patterns")
        st.markdown("""
        <div style='background: rgba(56, 239, 125, 0.05); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='color: #cbd5e1; margin: 0; font-size: 0.85rem;'>
                Monthly trends reveal seasonal demand fluctuations throughout the year. This helps in planning 
                annual maintenance schedules, inventory adjustments, and seasonal marketing campaigns.
                <br><br>
                <strong>Strategic Value:</strong> Identifying low-demand months allows for scheduled maintenance 
                without impacting revenue, while high-demand months require maximum fleet availability.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        monthly_data = df.groupby('Month_name')['count'].mean().reindex([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]).reset_index()
        
        fig = px.line(monthly_data, x='Month_name', y='count',
                      markers=True)
        fig.update_traces(line_color='#11998e', line_width=3, marker=dict(size=10))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=False, title='Month', tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Average Rentals'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        best_month_idx = monthly_data['count'].idxmax()
        worst_month_idx = monthly_data['count'].idxmin()
        best_month = monthly_data.loc[best_month_idx, 'Month_name']
        worst_month = monthly_data.loc[worst_month_idx, 'Month_name']
        
        st.warning(f"""
        **📅 Monthly Insights:**
        - **Peak Month:** {best_month} ({monthly_data.loc[best_month_idx, 'count']:.0f} bikes/hour)
        - **Lowest Month:** {worst_month} ({monthly_data.loc[worst_month_idx, 'count']:.0f} bikes/hour)
        - **Annual Variation:** {((monthly_data.loc[best_month_idx, 'count'] - monthly_data.loc[worst_month_idx, 'count']) / monthly_data.loc[worst_month_idx, 'count'] * 100):.1f}% difference
        - **Maintenance Window:** Schedule major maintenance during {worst_month}
        - **Marketing Focus:** Launch promotional campaigns in {best_month} to maximize revenue
        """)
    
    with viz_tabs[3]:
        st.subheader("User Type Analysis")
        
        st.markdown("""
        <div style='background: rgba(250, 112, 154, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #fa709a; margin-bottom: 1.5rem;'>
            <h4 style='color: #fa709a; margin-top: 0;'>👥 Casual vs Registered Users</h4>
            <p style='color: #cbd5e1; margin: 0;'>
                Compare behavior and patterns between casual and registered users.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**User Type Distribution**")
            user_data = pd.DataFrame({
                'User Type': ['Casual', 'Registered'],
                'Total Rentals': [df['casual'].sum(), df['registered'].sum()]
            })
            fig = px.pie(user_data, values='Total Rentals', names='User Type',
                         hole=0.4,
                         color_discrete_sequence=['#8b5cf6', '#ec4899'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            
            registered_pct = (df['registered'].sum() / (df['casual'].sum() + df['registered'].sum())) * 100
            st.success(f"📊 **Registered users:** {registered_pct:.1f}% of total rentals")
        
        with col2:
            st.markdown("**User Types by Working Day**")
            workday_users = df.groupby('workingday')[['casual', 'registered']].mean().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(x=workday_users['workingday'], y=workday_users['casual'],
                                 name='Casual', marker_color='#8b5cf6'))
            fig.add_trace(go.Bar(x=workday_users['workingday'], y=workday_users['registered'],
                                 name='Registered', marker_color='#ec4899'))
            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

# TAB 3: Univariate Analysis
with tabs[2]:
    st.header("📈 Univariate Analysis")
    logger.info("Univariate Analysis tab accessed")
    
    st.markdown("""
    <div style='background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea; margin-bottom: 1.5rem;'>
        <h4 style='color: #667eea; margin-top: 0;'>📊 Individual Variable Analysis</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            Examine the distribution and characteristics of each variable independently.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Select feature to analyze
    num_feature = st.selectbox("Select Numerical Feature", ['temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Distribution of {num_feature}**")
        fig = px.histogram(df, x=num_feature, nbins=30,
                          color_discrete_sequence=['#8b5cf6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"**Box Plot of {num_feature}**")
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[num_feature], name=num_feature,
                             marker_color='#ec4899', boxmean='sd'))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.markdown(f"**Statistical Summary for {num_feature}**")
    stats_df = df[num_feature].describe().to_frame().T
    st.dataframe(stats_df, use_container_width=True)

# TAB 4: Bivariate Analysis
with tabs[3]:
    st.header("🔗 Bivariate Analysis")
    logger.info("Bivariate Analysis tab accessed")
    
    st.markdown("""
    <div style='background: rgba(244, 114, 182, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #f472b6; margin-bottom: 1.5rem;'>
        <h4 style='color: #f472b6; margin-top: 0;'>🔗 Relationship Analysis</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            Explore relationships between variables and their impact on bike rentals.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Temperature vs Rentals
    st.markdown("**🌡️ Temperature vs Bike Rentals**")
    fig = px.scatter(df, x='temp', y='count',
                     color='season',
                     trendline='ols',
                     opacity=0.6,
                     color_discrete_sequence=['#667eea', '#f093fb', '#11998e', '#fa709a'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation
    corr_value = df['temp'].corr(df['count'])
    st.success(f"📊 **Correlation:** {corr_value:.3f} (Strong positive correlation)")
    
    st.markdown("---")
    
    # Correlation Heatmap
    st.markdown("**🔥 Correlation Heatmap**")
    numerical_cols = ['temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count']
    corr_matrix = df[numerical_cols].corr()
    
    fig = px.imshow(corr_matrix,
                    text_auto='.2f',
                    aspect='auto',
                    color_continuous_scale='RdBu_r',
                    labels=dict(color='Correlation'))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1'),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **🔍 Key Correlations with Bike Rentals:**
    - **Temperature (atemp)**: +0.63 (Strong positive)
    - **Registered Users**: +0.97 (Very strong positive)
    - **Humidity**: -0.32 (Moderate negative)
    """)

# TAB 5: Hypothesis Testing
with tabs[4]:
    st.header("🔬 Hypothesis Testing")
    logger.info("Hypothesis Testing tab accessed")
    
    st.markdown("""
    <div style='background: rgba(56, 239, 125, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #38ef7d; margin-bottom: 1.5rem;'>
        <h4 style='color: #38ef7d; margin-top: 0;'>🔬 Statistical Hypothesis Tests</h4>
        <p style='color: #cbd5e1; margin: 0;'>
            Perform rigorous statistical tests to validate our findings and answer key business questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    test_tabs = st.tabs(["T-Test: Working Day", "ANOVA: Season", "ANOVA: Weather", "Chi-Square: Weather-Season"])
    
    # Test 1: Working Day Effect
    with test_tabs[0]:
        st.subheader("📊 Test 1: Working Day Effect on Rentals")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h4 style='color: #a78bfa;'>Hypotheses</h4>
                <p><strong>H₀ (Null):</strong> Working day has NO effect on bike rentals</p>
                <p><strong>H₁ (Alternative):</strong> Working day HAS an effect on bike rentals</p>
                <p><strong>Test:</strong> Independent 2-Sample T-Test</p>
                <p><strong>Significance Level:</strong> α = 0.05</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            working_yes = df[df['workingday'] == 'Yes']['count']
            working_no = df[df['workingday'] == 'No']['count']
            
            t_stat, p_value = ttest_ind(working_yes, working_no)
            
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #f472b6;'>Results</h4>
                <p><strong>T-Statistic:</strong> {t_stat:.4f}</p>
                <p><strong>P-Value:</strong> {p_value:.6f}</p>
                <p><strong>Decision:</strong> {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value < 0.05:
            st.success("✅ **Conclusion:** Working day has a statistically significant effect on bike rentals.")
        else:
            st.warning("⚠️ **Conclusion:** No statistically significant effect of working day on bike rentals.")
        
        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Box(y=working_yes, name='Working Day: Yes', marker_color='#8b5cf6'))
        fig.add_trace(go.Box(y=working_no, name='Working Day: No', marker_color='#ec4899'))
        fig.update_layout(
            title='Distribution of Bike Rentals by Working Day',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Test 2: Season Effect
    with test_tabs[1]:
        st.subheader("📊 Test 2: Season Effect on Rentals")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h4 style='color: #a78bfa;'>Hypotheses</h4>
                <p><strong>H₀ (Null):</strong> Mean rentals are SAME across all seasons</p>
                <p><strong>H₁ (Alternative):</strong> Mean rentals DIFFER across seasons</p>
                <p><strong>Test:</strong> One-Way ANOVA</p>
                <p><strong>Significance Level:</strong> α = 0.05</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            spring = df[df['season'] == 'Spring']['count']
            summer = df[df['season'] == 'Summer']['count']
            fall = df[df['season'] == 'Fall']['count']
            winter = df[df['season'] == 'Winter']['count']
            
            f_stat, p_value = f_oneway(spring, summer, fall, winter)
            
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #f472b6;'>Results</h4>
                <p><strong>F-Statistic:</strong> {f_stat:.4f}</p>
                <p><strong>P-Value:</strong> {p_value:.6f}</p>
                <p><strong>Decision:</strong> {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value < 0.05:
            st.success("✅ **Conclusion:** Bike rentals differ significantly across seasons.")
        else:
            st.warning("⚠️ **Conclusion:** No significant difference in rentals across seasons.")
        
        # Visualization
        fig = go.Figure()
        for season in ['Spring', 'Summer', 'Fall', 'Winter']:
            season_data = df[df['season'] == season]['count']
            fig.add_trace(go.Box(y=season_data, name=season))
        
        fig.update_layout(
            title='Distribution of Bike Rentals by Season',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Test 3: Weather Effect
    with test_tabs[2]:
        st.subheader("📊 Test 3: Weather Effect on Rentals")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h4 style='color: #a78bfa;'>Hypotheses</h4>
                <p><strong>H₀ (Null):</strong> Mean rentals are SAME across all weather conditions</p>
                <p><strong>H₁ (Alternative):</strong> Mean rentals DIFFER across weather conditions</p>
                <p><strong>Test:</strong> One-Way ANOVA</p>
                <p><strong>Significance Level:</strong> α = 0.05</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            weather_groups = [df[df['weather'] == w]['count'].values for w in df['weather'].unique()]
            f_stat, p_value = f_oneway(*weather_groups)
            
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #f472b6;'>Results</h4>
                <p><strong>F-Statistic:</strong> {f_stat:.4f}</p>
                <p><strong>P-Value:</strong> {p_value:.6f}</p>
                <p><strong>Decision:</strong> {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value < 0.05:
            st.success("✅ **Conclusion:** Bike rentals differ significantly across weather conditions.")
        else:
            st.warning("⚠️ **Conclusion:** No significant difference in rentals across weather conditions.")
        
        # Visualization
        fig = go.Figure()
        for weather in df['weather'].unique():
            weather_data = df[df['weather'] == weather]['count']
            fig.add_trace(go.Box(y=weather_data, name=weather))
        
        fig.update_layout(
            title='Distribution of Bike Rentals by Weather',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Test 4: Weather-Season Dependency
    with test_tabs[3]:
        st.subheader("📊 Test 4: Weather Dependency on Season")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h4 style='color: #a78bfa;'>Hypotheses</h4>
                <p><strong>H₀ (Null):</strong> Weather is INDEPENDENT of season</p>
                <p><strong>H₁ (Alternative):</strong> Weather is DEPENDENT on season</p>
                <p><strong>Test:</strong> Chi-Square Test of Independence</p>
                <p><strong>Significance Level:</strong> α = 0.05</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            contingency_table = pd.crosstab(df['season'], df['weather'])
            chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)
            
            st.markdown(f"""
            <div class='metric-card'>
                <h4 style='color: #f472b6;'>Results</h4>
                <p><strong>Chi-Square:</strong> {chi2_stat:.4f}</p>
                <p><strong>P-Value:</strong> {p_value:.6f}</p>
                <p><strong>DoF:</strong> {dof}</p>
                <p><strong>Decision:</strong> {'Reject H₀' if p_value < 0.05 else 'Fail to Reject H₀'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if p_value < 0.05:
            st.success("✅ **Conclusion:** Weather is significantly dependent on season.")
        else:
            st.warning("⚠️ **Conclusion:** Weather is independent of season.")
        
        # Visualization
        fig = px.imshow(contingency_table,
                        text_auto=True,
                        aspect='auto',
                        color_continuous_scale='Viridis',
                        labels=dict(x='Weather', y='Season', color='Count'))
        fig.update_layout(
            title='Season vs Weather Contingency Table',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# TAB 6: Insights & Recommendations
with tabs[5]:
    st.header("💡 Business Insights & Recommendations")
    logger.info("Insights tab accessed")
    
    # Key Insights Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        peak_hour = df.groupby('hour')['count'].mean().idxmax()
        peak_value = df.groupby('hour')['count'].mean().max()
        st.markdown(f"""
        <div class='card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); text-align: left; height: 280px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🕐</div>
            <h3 style='color: white !important; margin: 0 0 1rem 0;'>Peak Hours</h3>
            <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                <strong>Peak Time:</strong> {peak_hour}:00<br>
                <strong>Avg Rentals:</strong> {peak_value:.0f} bikes<br>
                <strong>Pattern:</strong> Morning (7-9 AM) & Evening (5-7 PM) rush hours
            </p>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 1rem;'>
                💡 Ensure maximum bike availability during peak commute hours
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        best_season = df.groupby('season')['count'].mean().idxmax()
        best_season_val = df.groupby('season')['count'].mean().max()
        worst_season = df.groupby('season')['count'].mean().idxmin()
        worst_season_val = df.groupby('season')['count'].mean().min()
        st.markdown(f"""
        <div class='card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); text-align: left; height: 280px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🌸</div>
            <h3 style='color: white !important; margin: 0 0 1rem 0;'>Seasonal Patterns</h3>
            <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                <strong>Best:</strong> {best_season} ({best_season_val:.0f} bikes)<br>
                <strong>Worst:</strong> {worst_season} ({worst_season_val:.0f} bikes)<br>
                <strong>Variation:</strong> {((best_season_val - worst_season_val) / worst_season_val * 100):.1f}% difference
            </p>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 1rem;'>
                💡 Plan maintenance during low-demand seasons
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        best_weather = df.groupby('weather')['count'].mean().idxmax()
        best_weather_val = df.groupby('weather')['count'].mean().max()
        worst_weather = df.groupby('weather')['count'].mean().idxmin()
        worst_weather_val = df.groupby('weather')['count'].mean().min()
        st.markdown(f"""
        <div class='card' style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); text-align: left; height: 280px;'>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🌤️</div>
            <h3 style='color: white !important; margin: 0 0 1rem 0;'>Weather Impact</h3>
            <p style='color: rgba(255,255,255,0.9); line-height: 1.8;'>
                <strong>Best:</strong> {best_weather} ({best_weather_val:.0f} bikes)<br>
                <strong>Worst:</strong> {worst_weather} ({worst_weather_val:.0f} bikes)<br>
                <strong>Impact:</strong> {((best_weather_val - worst_weather_val) / worst_weather_val * 100):.1f}% drop
            </p>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 1rem;'>
                💡 Implement weather-based pricing
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recommendations
    st.subheader("🚀 Actionable Recommendations")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        with st.expander("🎯 **Operational Strategies**", expanded=True):
            st.markdown("""
            1. **Dynamic Fleet Management**
               - Redistribute bikes based on hourly demand patterns
               - Increase availability during peak hours (7-9 AM, 5-7 PM)
               - Reduce fleet during low-demand hours (1-5 AM)
            
            2. **Seasonal Planning**
               - Schedule maintenance during winter (lowest demand)
               - Maximize fleet availability during fall (highest demand)
               - Prepare for seasonal transitions
            
            3. **Weather-Based Operations**
               - Implement weather alert system
               - Adjust pricing based on weather forecasts
               - Offer rain protection accessories
            """)
    
    with rec_col2:
        with st.expander("💼 **Business Strategies**", expanded=True):
            st.markdown("""
            4. **User Conversion Program**
               - Convert casual users to registered (81% are registered)
               - Offer loyalty rewards and discounts
               - Create subscription plans
            
            5. **Pricing Optimization**
               - Surge pricing during peak hours
               - Weather-based dynamic pricing
               - Seasonal promotional campaigns
            
            6. **Marketing Focus**
               - Target working professionals (commute hours)
               - Promote eco-friendly transportation
               - Partner with corporates for employee programs
            """)

# TAB 7: Complete Analysis
with tabs[6]:
    st.header("📚 Complete Analysis Summary")
    logger.info("Complete Analysis tab accessed")
    
    # Analysis sub-tabs
    analysis_tabs = st.tabs([
        "📊 Overview Statistics",
        "📈 Temporal Analysis", 
        "🌡️ Environmental Factors",
        "👥 User Behavior",
        "🔗 Advanced Analytics"
    ])
    
    # Sub-tab 1: Overview Statistics
    with analysis_tabs[0]:
        st.subheader("📊 Comprehensive Statistics Overview")
        
        # Key Metrics in gradient cards
        st.markdown("**🎯 Key Performance Indicators**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{df['count'].sum():,}</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>TOTAL RENTALS</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{df['count'].mean():.1f}</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>AVG RENTALS/HOUR</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{df['count'].max()}</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>MAX RENTALS/HOUR</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            registered_pct = (df['registered'].sum() / df['count'].sum() * 100)
            casual_pct = (df['casual'].sum() / df['count'].sum() * 100)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{registered_pct:.1f}%</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>REGISTERED USERS %</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{casual_pct:.1f}%</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>CASUAL USERS %</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{df['temp'].mean():.1f}°C</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>AVG TEMPERATURE</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            peak_hour = df.groupby('hour')['count'].mean().idxmax()
            best_season = df.groupby('season')['count'].mean().idxmax()
            best_weather = df.groupby('weather')['count'].mean().idxmax()
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{peak_hour}:00</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>PEAK HOUR</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{best_season}</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>BEST SEASON</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='metric-card' style='text-align: center; margin-top: 1rem;'>
                <p style='font-size: 2.5rem; margin: 0; background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;'>{best_weather}</p>
                <p style='margin: 0.5rem 0; color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>BEST WEATHER</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Detailed Statistics
        st.markdown("**📊 Detailed Descriptive Statistics**")
        with st.expander("View Full Statistics Table", expanded=False):
            st.dataframe(df.describe(include='all').T, use_container_width=True)
        
        # Distribution Overview
        st.markdown("**📈 Distribution Overview**")
        col1, col2 = st.columns(2)
        
        with col1:
            # Rental distribution
            fig = px.histogram(df, x='count', nbins=50,
                              title='Distribution of Bike Rentals',
                              color_discrete_sequence=['#8b5cf6'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Number of Rentals'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Frequency'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Temperature distribution
            fig = px.histogram(df, x='temp', nbins=30,
                              title='Temperature Distribution',
                              color_discrete_sequence=['#ec4899'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Temperature (°C)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Frequency'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Sub-tab 2: Temporal Analysis
    with analysis_tabs[1]:
        st.subheader("📈 Comprehensive Temporal Analysis")
        
        # Time series plot
        st.markdown("**📅 Daily Rental Trends Over Time**")
        daily_rentals = df.groupby('date')['count'].sum().reset_index()
        daily_rentals['date'] = pd.to_datetime(daily_rentals['date'])
        
        fig = px.line(daily_rentals, x='date', y='count',
                      title='Total Daily Rentals Over Time')
        fig.update_traces(line_color='#8b5cf6', line_width=2)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Date'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Total Rentals'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Hourly heatmap
        st.markdown("**🔥 Hourly Rental Heatmap by Day of Week**")
        
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hourly_day_data = df.groupby(['day', 'hour'])['count'].mean().reset_index()
        hourly_pivot = hourly_day_data.pivot(index='day', columns='hour', values='count')
        hourly_pivot = hourly_pivot.reindex(day_order)
        
        fig = px.imshow(hourly_pivot,
                        labels=dict(x='Hour of Day', y='Day of Week', color='Avg Rentals'),
                        aspect='auto',
                        color_continuous_scale='Viridis')
        fig.update_layout(
            title='Average Rentals Heatmap: Day vs Hour',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Monthly comparison
        st.markdown("**📊 Monthly Rental Comparison**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_avg = df.groupby('Month_name')['count'].mean().reindex([
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ]).reset_index()
            
            fig = px.bar(monthly_avg, x='Month_name', y='count',
                        title='Average Rentals by Month',
                        color='count',
                        color_continuous_scale='Plasma')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Year comparison
            yearly_avg = df.groupby('year')['count'].mean().reset_index()
            
            fig = px.bar(yearly_avg, x='year', y='count',
                        title='Average Rentals by Year',
                        color='count',
                        color_continuous_scale='Turbo')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Sub-tab 3: Environmental Factors
    with analysis_tabs[2]:
        st.subheader("🌡️ Environmental Factors Analysis")
        
        # Temperature vs Humidity scatter
        st.markdown("**🌡️ Temperature vs Humidity Impact**")
        fig = px.scatter(df, x='temp', y='humidity',
                        color='count',
                        size='count',
                        title='Temperature vs Humidity (colored by rentals)',
                        color_continuous_scale='Viridis',
                        opacity=0.6)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Environmental factors comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💨 Windspeed Impact**")
            windspeed_bins = pd.cut(df['windspeed'], bins=5)
            windspeed_avg = df.groupby(windspeed_bins)['count'].mean().reset_index()
            windspeed_avg['windspeed'] = windspeed_avg['windspeed'].astype(str)
            
            fig = px.bar(windspeed_avg, x='windspeed', y='count',
                        title='Average Rentals by Windspeed Range',
                        color='count',
                        color_continuous_scale='Blues')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Windspeed Range'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**💧 Humidity Impact**")
            humidity_bins = pd.cut(df['humidity'], bins=5)
            humidity_avg = df.groupby(humidity_bins)['count'].mean().reset_index()
            humidity_avg['humidity'] = humidity_avg['humidity'].astype(str)
            
            fig = px.bar(humidity_avg, x='humidity', y='count',
                        title='Average Rentals by Humidity Range',
                        color='count',
                        color_continuous_scale='Greens')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False, title='Humidity Range'),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Correlation with environmental factors
        st.markdown("**🔗 Environmental Correlations with Rentals**")
        env_corr = df[['temp', 'atemp', 'humidity', 'windspeed', 'count']].corr()['count'].drop('count').sort_values(ascending=False)
        
        fig = px.bar(x=env_corr.index, y=env_corr.values,
                    title='Correlation of Environmental Factors with Rentals',
                    color=env_corr.values,
                    color_continuous_scale='RdBu_r',
                    color_continuous_midpoint=0)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=False, title='Environmental Factor'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Correlation'),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sub-tab 4: User Behavior
    with analysis_tabs[3]:
        st.subheader("👥 User Behavior Analysis")
        
        # User type trends over time
        st.markdown("**📈 User Type Trends Over Time**")
        
        daily_users = df.groupby('date')[['casual', 'registered']].sum().reset_index()
        daily_users['date'] = pd.to_datetime(daily_users['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_users['date'], y=daily_users['casual'],
                                name='Casual Users',
                                line=dict(color='#8b5cf6', width=2),
                                fill='tozeroy'))
        fig.add_trace(go.Scatter(x=daily_users['date'], y=daily_users['registered'],
                                name='Registered Users',
                                line=dict(color='#ec4899', width=2),
                                fill='tozeroy'))
        
        fig.update_layout(
            title='Daily User Type Trends',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Date'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Number of Users'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # User behavior by conditions
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌤️ User Types by Weather**")
            weather_users = df.groupby('weather')[['casual', 'registered']].mean().reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=weather_users['weather'], y=weather_users['casual'],
                                name='Casual', marker_color='#8b5cf6'))
            fig.add_trace(go.Bar(x=weather_users['weather'], y=weather_users['registered'],
                                name='Registered', marker_color='#ec4899'))
            
            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**🌸 User Types by Season**")
            season_users = df.groupby('season')[['casual', 'registered']].mean().reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=season_users['season'], y=season_users['casual'],
                                name='Casual', marker_color='#8b5cf6'))
            fig.add_trace(go.Bar(x=season_users['season'], y=season_users['registered'],
                                name='Registered', marker_color='#ec4899'))
            
            fig.update_layout(
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#cbd5e1'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)'),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # User type ratio analysis
        st.markdown("**📊 User Type Ratio by Hour**")
        hourly_users = df.groupby('hour')[['casual', 'registered']].mean().reset_index()
        hourly_users['casual_pct'] = (hourly_users['casual'] / (hourly_users['casual'] + hourly_users['registered'])) * 100
        hourly_users['registered_pct'] = (hourly_users['registered'] / (hourly_users['casual'] + hourly_users['registered'])) * 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hourly_users['hour'], y=hourly_users['casual_pct'],
                                name='Casual %',
                                line=dict(color='#8b5cf6', width=3),
                                mode='lines+markers'))
        fig.add_trace(go.Scatter(x=hourly_users['hour'], y=hourly_users['registered_pct'],
                                name='Registered %',
                                line=dict(color='#ec4899', width=3),
                                mode='lines+markers'))
        
        fig.update_layout(
            title='User Type Percentage by Hour of Day',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            xaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Hour'),
            yaxis=dict(showgrid=True, gridcolor='rgba(139, 92, 246, 0.1)', title='Percentage'),
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Sub-tab 5: Advanced Analytics
    with analysis_tabs[4]:
        st.subheader("🔗 Advanced Analytics")
        
        # Correlation matrix
        st.markdown("**🔥 Complete Correlation Matrix**")
        numerical_cols = ['temp', 'atemp', 'humidity', 'windspeed', 'casual', 'registered', 'count']
        corr_matrix = df[numerical_cols].corr()
        
        fig = px.imshow(corr_matrix,
                        text_auto='.2f',
                        aspect='auto',
                        color_continuous_scale='RdBu_r',
                        labels=dict(color='Correlation'),
                        zmin=-1, zmax=1)
        fig.update_layout(
            title='Feature Correlation Heatmap',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Top correlations
        st.markdown("**📊 Top Correlations with Bike Rentals**")
        
        count_corr = corr_matrix['count'].drop('count').sort_values(ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Positive Correlations**")
            positive_corr = count_corr[count_corr > 0]
            for feature, corr in positive_corr.items():
                st.markdown(f"""
                <div class='metric-card' style='margin-bottom: 0.5rem;'>
                    <p style='margin: 0; color: #cbd5e1;'><strong>{feature}:</strong> <span style='color: #38ef7d;'>{corr:.3f}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Negative Correlations**")
            negative_corr = count_corr[count_corr < 0]
            for feature, corr in negative_corr.items():
                st.markdown(f"""
                <div class='metric-card' style='margin-bottom: 0.5rem;'>
                    <p style='margin: 0; color: #cbd5e1;'><strong>{feature}:</strong> <span style='color: #f472b6;'>{corr:.3f}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistical summary table
        st.markdown("**📋 Complete Statistical Summary**")
        with st.expander("View Detailed Statistics", expanded=False):
            st.dataframe(df[numerical_cols].describe().T, use_container_width=True)
    
    st.markdown("---")
    
    # Download options
    st.subheader("💾 Export Data & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Processed Data",
            data=csv,
            file_name="yulu_processed_data.csv",
            mime="text/csv"
        )
    
    with col2:
        summary = df.describe(include='all').to_csv()
        st.download_button(
            label="📥 Download Statistics",
            data=summary,
            file_name="yulu_statistics.csv",
            mime="text/csv"
        )
    
    with col3:
        corr_csv = df[numerical_cols].corr().to_csv()
        st.download_button(
            label="📥 Download Correlations",
            data=corr_csv,
            file_name="yulu_correlations.csv",
            mime="text/csv"
        )

# TAB 8: Logs
with tabs[7]:
    st.header("📝 Application Logs")
    logger.info("Logs tab accessed")
    
    st.markdown("""
    <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 10px; border-left: 4px solid #8b5cf6;'>
        <p style='color: #cbd5e1; margin: 0;'>
            This section shows all actions performed in the current session.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        with open('yulu_app.log', 'r') as f:
            logs = f.readlines()
            for log in logs[-50:]:  # Show last 50 logs
                st.text(log.strip())
    except:
        st.info("No logs available yet.")

if __name__ == "__main__":
    logger.info("Yulu App running successfully")
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: #9ca3af;'>
        <p>Made with ❤️ using Streamlit & Plotly</p>
        <p style='font-size: 0.9rem;'>© 2025 Yulu Bike Sharing Ratnesh Analytics</p>
    </div>
    """, unsafe_allow_html=True)
