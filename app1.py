from io import BytesIO
from pathlib import Path

import streamlit as st
from pytube import YouTube

st.set_page_config(page_title="Tejverter", page_icon="🎵", layout="centered", initial_sidebar_state="collapsed")

@st.cache_data(show_spinner=False)
def download_audio_to_buffer(url):
    buffer = BytesIO()
    youtube_video = YouTube(url)
    audio = youtube_video.streams.get_audio_only()
    default_filename = audio.default_filename
    audio.stream_to_buffer(buffer)
    return default_filename, buffer

def main():
    st.title("Tejas's YT to Audio Converter")
    url = st.text_input("Insert Youtube URL:")
    if url:
        with st.spinner("Downloading Audio Stream from Youtube..."):
            default_filename, buffer = download_audio_to_buffer(url)
        st.subheader("Title")
        st.write(default_filename)
        title_vid = Path(default_filename).with_suffix(".mp3").name
        st.subheader("Listen to Audio")
        st.audio(buffer, format='audio/mpeg')
        st.subheader("Download Audio File")
        st.download_button(
            label="Download mp3",
            data=buffer,
            file_name=title_vid,
            mime="audio/mpeg")

if __name__ == "__main__":
    main()
