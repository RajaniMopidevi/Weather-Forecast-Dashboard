import requests
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Weather Forecast Dashboard")
st.caption("Real-time & forecast weather dashboard using OpenWeather API")


API_KEY = "a142f5b410c4de1723204d01be94a523"

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if city == "":
        st.warning("Please enter a city name")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            st.error(data.get("message"))
        else:
            st.subheader(f"Weather in {data['name']}")
            col1, col2 = st.columns([1, 2],gap = "small")

            
            st.metric("Temperature (°C)", data["main"]["temp"])
            st.metric("Humidity (%)", data["main"]["humidity"])
            st.metric("Wind Speed (m/s)", data["wind"]["speed"])


            st.write("**Weather Description:**", data["weather"][0]["description"].capitalize())

            dt = datetime.fromtimestamp(data["dt"])
            st.caption(f"Data&Time: {dt}")
            
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]


            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast?"
                f"q={city}&appid={API_KEY}&units=metric"
            )

            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()

            if "list" not in forecast_data:
                st.error("Forecast data not available")
            else:
                st.success("Forecast data fetched successfully")
                    

            
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
                

                st.subheader("Daily Average Temperature (Next 5 Days)")
                st.line_chart(daily_df)






            



