import streamlit as st
import requests

# Function to fetch radio stations from RadioBrowser API
def fetch_radio_stations():
    url = "https://de1.api.radio-browser.info/json/stations/topclick/500"  # Fetching top 500 stations
    response = requests.get(url)
    return response.json()

# Streamlit App
st.set_page_config(page_title="Radio FM App", page_icon=":radio:", layout="wide")

st.title("Radio FM App :radio:")
st.write("Listen to thousands of radio stations worldwide.")

# Fetch stations
stations = fetch_radio_stations()

# Search box in the sidebar
search_term = st.sidebar.text_input("Search for a Radio Station")

# Filter stations based on search term
filtered_stations = [station for station in stations if search_term.lower() in station['name'].lower()]
filtered_station_names = [station['name'] for station in filtered_stations]

# Select a radio station from filtered results
selected_station = st.sidebar.selectbox("Select a Radio Station", filtered_station_names)

# Find the URL and logo of the selected station
selected_station_url = None
selected_station_logo = None
for station in filtered_stations:
    if station['name'] == selected_station:
        selected_station_url = station['url_resolved']
        selected_station_logo = station.get('favicon')
        break

# Display the selected station's details and embed the player
if selected_station_url:
    st.subheader(f"Playing {selected_station}")
    
    if selected_station_logo:
        st.image(selected_station_logo, width=100)

    st.markdown(
        f'<iframe src="{selected_station_url}" width="100%" height="300" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )
else:
    st.write("Select a station from the sidebar to start listening.")
