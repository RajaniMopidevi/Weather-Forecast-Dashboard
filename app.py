import requests
import streamlit as st
import pandas as pd
from datetime import datetime

# 🌈 Bright background
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #2b5876, #4e4376);
}
</style>
""", unsafe_allow_html=True)

st.title("🌦 Weather Forecast Dashboard")
st.caption("Real-time & forecast weather dashboard using OpenWeather API")

API_KEY = "a142f5b410c4de1723204d01be94a523"

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if city == "":
        st.warning("Please enter a city name")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        with st.spinner("Fetching weather..."):
            response = requests.get(url)
            data = response.json()

        if data.get("cod") != 200:
            st.error(data.get("message"))
        else:
            st.subheader(f"📍 Weather in {data['name']}")

            # 🌈 COLORFUL CARDS
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div style="
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:black;">
                🌡<br><b>Temperature</b>
                <h2>{data['main']['temp']}°C</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div style="
                background: linear-gradient(135deg, #a1c4fd, #c2e9fb);
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:black;">
                💧<br><b>Humidity</b>
                <h2>{data['main']['humidity']}%</h2>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div style="
                background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
                padding:20px;
                border-radius:15px;
                text-align:center;
                color:black;">
                🌬<br><b>Wind</b>
                <h2>{data['wind']['speed']} m/s</h2>
                </div>
                """, unsafe_allow_html=True)

            # ☁ Weather description box
            st.markdown(f"""
            <div style="
            background:white;
            padding:15px;
            border-radius:12px;
            margin-top:20px;
            text-align:center;
            color:black;
            font-weight:500;">
            ☁ {data["weather"][0]["description"].capitalize()}
            </div>
            """, unsafe_allow_html=True)

            # 🕒 Date time
            dt = datetime.fromtimestamp(data["dt"])
            st.caption(f"📅 {dt.strftime('%d %B %Y, %I:%M %p')}")

            # 📊 FORECAST
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if "list" not in forecast_data:
                st.error("Forecast data not available")
            else:
                dates = []
                temps = []

                for item in forecast_data["list"]:
                    date = datetime.fromtimestamp(item["dt"]).date()
                    dates.append(date)
                    temps.append(item["main"]["temp"])

                df = pd.DataFrame({
                    "Date": dates,
                    "Temperature (°C)": temps
                })

                daily_df = df.groupby("Date", as_index=True).mean()
                daily_df.index = pd.to_datetime(daily_df.index).strftime("%b %d")

                st.subheader("📈 5-Day Temperature Forecast")
                st.line_chart(daily_df, use_container_width=True)