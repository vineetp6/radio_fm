import streamlit as st
import requests
from pydub import AudioSegment
from pydub.playback import play
import io

# Function to fetch radio stations from RadioBrowser API
def fetch_radio_stations():
    url = "https://de1.api.radio-browser.info/json/stations/bycountry/united%20states"
    response = requests.get(url)
    return response.json()

# Function to play audio from a URL
def play_audio(url):
    audio = AudioSegment.from_file(io.BytesIO(requests.get(url).content))
    play(audio)
    return audio

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

# Audio control buttons
col1, col2, col3, col4 = st.columns(4)

if selected_station_url:
    if col1.button("Play"):
        audio = play_audio(selected_station_url)
        st.session_state['audio'] = audio

    if col2.button("Stop"):
        st.session_state['audio'] = None

    if col3.button("Forward") and 'audio' in st.session_state and st.session_state['audio']:
        audio = st.session_state['audio']
        audio = audio[10000:]  # Skip first 10 seconds
        play(audio)
        st.session_state['audio'] = audio

    if col4.button("Back") and 'audio' in st.session_state and st.session_state['audio']:
        audio = st.session_state['audio']
        audio = audio[:-10000]  # Go back last 10 seconds
        play(audio)
        st.session_state['audio'] = audio

    # Option to save the audio file
    if st.button("Save Audio"):
        audio.export(f"{selected_station}.mp3", format="mp3")
        st.success(f"Saved {selected_station}.mp3")

    # Embed the selected station's web player
    st.write(f"Playing {selected_station}...")
    st.markdown(
        f'<iframe src="{selected_station_url}" width="100%" height="300" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )
else:
    st.write("Select a station to play.")
