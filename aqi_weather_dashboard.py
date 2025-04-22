import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

# Set page config
st.set_page_config(page_title="🌏 Real-Time AQI & Weather Dashboard", page_icon="🌿", layout="centered")

# Custom CSS for black and yellow color combination, with gradient background and center title
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to right, #000000, #2c3e50);
        color: #FFD700;
    }
    .title-center {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #FFD700;
        margin-bottom: 10px;
    }
    .medium-font {
        font-size:22px !important;
        color: #FFD700;
        text-align: center;
    }
    .pollutant-label {
        color: #FF9933;
    }
    .input-label {
        color: #FFFFFF;
    }
    .card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 2px 2px 5px #000000;
        margin-bottom: 10px;
    }
    .card h2 {
        color: #FFD700;
        margin: 0;
        font-size: 28px;
    }
    .card p {
        color: #FFFFFF;
        margin: 0;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered GIF from local file
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.write("")
with col2:
    st.image("weather.gif", width=200)
with col3:
    st.write("")

# Centered title
st.markdown("<div class='title-center'>🌍 Real-Time AQI & Weather Dashboard</div>", unsafe_allow_html=True)

# Instruction text
st.markdown("<div class='medium-font'>🔍 Enter latitude and longitude to get real-time air quality and weather info.</div>", unsafe_allow_html=True)

# User Inputs
latitude = st.number_input("Latitude", value=19.0760, format="%.4f")
longitude = st.number_input("Longitude", value=72.8777, format="%.4f")
api_key = "8f5fe383ceaf1dbd5b320ca9a11090e8"

if st.button("Check Now 🚀"):
    # Fetch air quality data
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    aqi_response = requests.get(aqi_url).json()
    data = aqi_response['list'][0]

    aqi = data['main']['aqi']
    pollutants = data['components']

    # Fetch location name and weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url).json()

    try:
        city = weather_response['name']
        country = weather_response['sys']['country']
        st.markdown(f"<h2 style='color:#FFD700;text-align:center;'>📍 {city}, {country}</h2>", unsafe_allow_html=True)
    except:
        st.markdown("<h2 style='color:#FFD700;text-align:center;'>📍 Location not found</h2>", unsafe_allow_html=True)

    # Weather Section
    temp = weather_response['main']['temp']
    humidity = weather_response['main']['humidity']
    wind_speed = weather_response['wind']['speed']
    description = weather_response['weather'][0]['description']

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(
        f"<h3 style='text-align:center; color:#FFD700;'>{temp}°C 🌡️<br><small>Temperature</small></h3>",
        unsafe_allow_html=True
    )
    col2.markdown(
        f"<h3 style='text-align:center; color:#FFD700;'>{humidity}% 💧<br><small>Humidity</small></h3>",
        unsafe_allow_html=True
    )
    col3.markdown(
        f"<h3 style='text-align:center; color:#FFD700;'>{wind_speed} m/s 🌬️<br><small>Wind Speed</small></h3>",
        unsafe_allow_html=True
    )
    col4.markdown(
        f"<h3 style='text-align:center; color:#FFD700;'>{description.title()} ☁️<br><small>Condition</small></h3>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Real-Time Air Quality Cards (Dynamic)
    st.subheader("📋 Live Air Quality Readings")
    card1, card2, card3 = st.columns(3)
    with card1:
        st.markdown(
            f"<div class='card'><h2>{pollutants['pm2_5']} μg/m³</h2><p>PM2.5</p></div>",
            unsafe_allow_html=True
        )
    with card2:
        st.markdown(
            f"<div class='card'><h2>{pollutants['pm10']} μg/m³</h2><p>PM10</p></div>",
            unsafe_allow_html=True
        )
    with card3:
        st.markdown(
            f"<div class='card'><h2>{pollutants['co']} μg/m³</h2><p>CO</p></div>",
            unsafe_allow_html=True
        )

    card4, card5, card6 = st.columns(3)
    with card4:
        st.markdown(
            f"<div class='card'><h2>{pollutants['so2']} μg/m³</h2><p>SO₂</p></div>",
            unsafe_allow_html=True
        )
    with card5:
        st.markdown(
            f"<div class='card'><h2>{pollutants['no2']} μg/m³</h2><p>NO₂</p></div>",
            unsafe_allow_html=True
        )
    with card6:
        st.markdown(
            f"<div class='card'><h2>{pollutants['o3']} μg/m³</h2><p>O₃</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # AQI Levels and Colors
    aqi_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
    aqi_colors = ["#009966", "#FFDE33", "#FF9933", "#CC0033", "#660099"]
    aqi_label = aqi_levels[aqi-1]
    aqi_color = aqi_colors[aqi-1]

    # AQI Gauge
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        gauge={
            'axis': {'range': [1, 5]},
            'bar': {'color': aqi_color},
            'steps': [
                {'range': [1, 2], 'color': "#009966"},
                {'range': [2, 3], 'color': "#FFDE33"},
                {'range': [3, 4], 'color': "#FF9933"},
                {'range': [4, 5], 'color': "#CC0033"}
            ],
        },
        title={'text': f"AQI: {aqi_label}", 'font': {'size': 24, 'color': "#FFD700"}},
    ))
    st.plotly_chart(gauge, use_container_width=True)

    # Pollutant Bar Chart
    bar = go.Figure(data=[go.Bar(
        x=list(pollutants.keys()),
        y=list(pollutants.values()),
        marker_color=['#FFD700', '#FF9933', '#CC0033', '#FFDE33', '#FF9933', '#CC0033', '#FFD700', '#FFDE33']
    )])
    bar.update_layout(
        title="Pollutant Concentration (μg/m³)",
        xaxis_title="Pollutants",
        yaxis_title="Concentration",
        paper_bgcolor='#222222',
        font_color='#FFD700',
        title_font=dict(size=22, color='#FFD700'),
        xaxis=dict(title_font=dict(size=18, color='#FFD700')),
        yaxis=dict(title_font=dict(size=18, color='#FFD700')),
        font=dict(color='#FFFFFF')
    )
    st.plotly_chart(bar, use_container_width=True)

    # Pollutant Pie Chart
    pie = go.Figure(data=[go.Pie(
        labels=list(pollutants.keys()),
        values=list(pollutants.values()),
        hole=0.4
    )])
    pie.update_layout(
        title="Pollutant Contribution (%)",
        paper_bgcolor='#222222',
        font_color='#FFD700',
        title_font=dict(size=22, color='#FFD700'),
        font=dict(color='#FFFFFF'),
        legend=dict(
            font=dict(
                color='#FFFFFF'
            )
        )
    )
    st.plotly_chart(pie, use_container_width=True)

    # Map Preview
    st.subheader("🗺️ Location Map")
    st.map(pd.DataFrame({'lat': [latitude], 'lon': [longitude]}))

    # Simulated AQI Trend
    st.subheader("📊 Simulated AQI Trend (Last 5 Readings)")
    aqi_history = [aqi-1, aqi-0.5, aqi, aqi+0.5, aqi]
    trend = pd.DataFrame({'Time': ['-4 min', '-3 min', '-2 min', '-1 min', 'Now'], 'AQI': aqi_history})
    st.line_chart(trend.set_index('Time'))

    st.success("✅ Data fetched successfully!")
