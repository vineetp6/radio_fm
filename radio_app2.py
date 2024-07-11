import streamlit as st
import requests

# Function to fetch radio stations from RadioBrowser API
def fetch_radio_stations():
    url = "https://de1.api.radio-browser.info/json/stations/bycountry/united%20states"
    response = requests.get(url)
    return response.json()

# Streamlit App
st.title("Radio FM App")
st.markdown("<h2 style='text-align: center;'>Listen to thousands of radio stations worldwide</h2>", unsafe_allow_html=True)

stations = fetch_radio_stations()
station_names = [station['name'] for station in stations]

# Search box for filtering stations
search_term = st.text_input("Search for a Radio Station", "")

# Filter stations based on search term
filtered_stations = [station for station in stations if search_term.lower() in station['name'].lower()]
filtered_station_names = [station['name'] for station in filtered_stations]

# Select a radio station from filtered results
selected_station = st.selectbox("Select a Radio Station", filtered_station_names)

# Find the URL of the selected station
selected_station_url = None
for station in filtered_stations:
    if station['name'] == selected_station:
        selected_station_url = station['url_resolved']
        break

# Display and play the selected station
if selected_station_url:
    st.write(f"Playing {selected_station}...")
    st.audio(selected_station_url)

    # Embed the selected station's web player
    st.markdown(
        f'<iframe src="{selected_station_url}" width="100%" height="300" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )
else:
    st.write("Select a station to play.")
