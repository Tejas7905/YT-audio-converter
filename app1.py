import streamlit as st
from pytube import YouTube
from io import BytesIO
import os

def download_audio_from_youtube(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # Create a temporary file to store the downloaded audio
    temp_file_path = "temp_audio.mp4"
    
    try:
        # Download the audio to a temporary file
        audio_stream.download(output_path=".", filename=temp_file_path)
        
        # Read the temporary file into a BytesIO object
        audio_file = BytesIO()
        with open(temp_file_path, "rb") as f:
            audio_file.write(f.read())
        
        # Reset the buffer's position to the beginning
        audio_file.seek(0)
        
        return audio_file
    finally:
        # Cleanup: Remove the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

st.title("Tejas's YouTube to MP3 Converter")

url = st.text_input("Paste the YouTube video URL here:")

# Variable to track conversion state
if 'convert' in st.session_state:
    if st.session_state.convert:
        st.write("Processing...")
        try:
            audio_data = download_audio_from_youtube(url)
            st.download_button(
                label="Download Audio",
                data=audio_data.getvalue(),  # Convert to bytes
                file_name="audio.mp4",
                mime="audio/mp4"  # MIME type for MP4 audio
            )
            st.session_state.convert = False  # Reset the button state
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.convert = False  # Reset the button state
else:
    st.session_state.convert = False

# Convert button
if st.button("Convert"):
    if url:
        st.session_state.convert = True
    else:
        st.error("Please enter a YouTube URL.")
