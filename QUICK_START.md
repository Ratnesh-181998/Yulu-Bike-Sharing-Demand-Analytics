# Yulu Streamlit App - Quick Start Guide

## 🚀 Running the App

### Option 1: Direct Run (Recommended)
```bash
streamlit run app.py
```

### Option 2: With Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Option 3: With Custom Browser
```bash
streamlit run app.py --server.headless false
```

## 🌐 Access URLs

- **Local**: http://localhost:8501
- **Network**: http://192.168.1.3:8501 (accessible from other devices on same network)

## 🎯 Navigation Guide

### Tab 1: Overview (🏠)
- Read the business problem
- Understand the dataset
- View quick statistics

### Tab 2: EDA (📊)
- Explore data structure
- View statistical summaries
- Analyze distributions

### Tab 3: Visualizations (📈)
- Interactive temporal patterns
- Weather and season analysis
- User type comparisons
- Correlation heatmaps

### Tab 4: Hypothesis Testing (🔬)
- **Test 1**: Working Day Effect (T-Test)
- **Test 2**: Season Effect (ANOVA)
- **Test 3**: Weather Effect (ANOVA)
- **Test 4**: Weather-Season Dependency (Chi-Square)

### Tab 5: Insights (💡)
- Key findings
- Strategic recommendations
- Impact analysis

### Tab 6: Complete Analysis (📋)
- Comprehensive statistics
- Export data options
- Full correlation matrix

### Tab 7: Logs (📝)
- View application activity
- Track all actions
- Clear logs option

## 🎨 Features

✅ Premium dark theme design
✅ Interactive Plotly visualizations
✅ Real-time statistical analysis
✅ Comprehensive hypothesis testing
✅ Downloadable reports
✅ Application logging

## 🛠️ Troubleshooting

### App won't start?
```bash
# Check if Streamlit is installed
pip install streamlit

# Check if all dependencies are installed
pip install -r requirements.txt
```

### Port already in use?
```bash
# Use a different port
streamlit run app.py --server.port 8503
```

### Data file not found?
- Ensure `yulu_data.csv` or `bike_sharing.txt` is in the same directory as `app.py`

## 📊 Data Export

The app allows you to download:
1. Processed dataset (CSV)
2. Statistical summaries (CSV)
3. Correlation matrix (CSV)

Access these from the "Complete Analysis" tab.

## 🔄 Refresh Data

The app uses `@st.cache_data` for performance. To reload data:
1. Click the menu (☰) in top-right
2. Select "Clear cache"
3. Click "Rerun"

## 💾 Saving Your Work

- All visualizations can be saved using the camera icon in Plotly charts
- Download data from the "Complete Analysis" tab
- Logs are automatically saved to `yulu_app.log`

## 🎯 Best Practices

1. **Start with Overview** - Understand the problem first
2. **Explore EDA** - Get familiar with the data
3. **Review Visualizations** - Identify patterns
4. **Study Hypothesis Tests** - Understand statistical significance
5. **Read Insights** - Get actionable recommendations

## 📱 Mobile Access

Access the app from your phone/tablet using the Network URL:
```
http://192.168.1.3:8501
```
(Make sure you're on the same WiFi network)

## 🔒 Security Note

This is a local development server. For production deployment, consider:
- Streamlit Cloud
- Heroku
- AWS/Azure/GCP

## 📧 Support

For issues or questions, check:
1. Application logs (`yulu_app.log`)
2. Streamlit documentation: https://docs.streamlit.io
3. The "Logs" tab in the app

---

**Happy Analyzing! 🚴📊**
