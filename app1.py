import streamlit as st
from pytube import YouTube
from io import BytesIO
import os

def download_audio_from_youtube(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # Create a BytesIO buffer to hold the downloaded audio
    audio_file = BytesIO()
    
    # Download the audio to a temporary file
    temp_file = "temp_audio.mp4"  # This should match the audio format of the stream
    audio_stream.download(output_path=".", filename=temp_file)
    
    # Read the temporary file into the BytesIO object
    with open(temp_file, "rb") as f:
        audio_file.write(f.read())
    
    # Reset the buffer's position to the beginning
    audio_file.seek(0)
    
    # Clean up the temporary file
    os.remove(temp_file)
    
    return audio_file

st.title("Tejas's YouTube to MP3 Converter")

url = st.text_input("Paste the YouTube video URL here:")

if 'convert' in st.session_state:
    if st.session_state.convert:
        st.write("Processing...")
        try:
            audio_data = download_audio_from_youtube(url)
            st.download_button(
                label="Download Audio",
                data=audio_data,
                file_name="audio.mp3",  # Use mp3 for audio
                mime="audio/mpeg"  # Correct MIME type for mp3
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
