import streamlit as st
from pytube import YouTube, Playlist
import os
import re

def sanitize_filename(filename):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized

def download_playlist(playlist_url, output_directory, selected_quality):
    playlist = Playlist(playlist_url)
    video_urls = playlist.video_urls

    for index, video_url in enumerate(video_urls, start=1):
        try:
            yt = YouTube(video_url)
            available_streams = yt.streams.filter(progressive=True, file_extension='mp4')
            stream = available_streams.get_by_resolution(selected_quality)
            title = sanitize_filename(yt.title)
            output_filename = f"{index}){title}.mp4"
            video_path = os.path.join(output_directory, output_filename)
            stream.download(output_path=output_directory, filename=output_filename)
            st.write(f"Downloaded {index}){yt.title}.")
        except Exception as e:
            st.write(f"Error Downloading {index}){video_url}: {e}")
            import traceback
            traceback.print_exc()

    st.write("All Videos Downloaded Successfully")

def main():
    st.title("YouTube Playlist Downloader")

    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    output_directory = st.text_input("Enter Output Directory:")
    quality_options = ['720p', '480p', '360p']  # Add more quality options if needed
    selected_quality = st.selectbox("Select Video Quality:", quality_options)

    if st.button("Download"):
        if playlist_url.strip() == "" or output_directory.strip() == "":
            st.error("Please enter both Playlist URL and Output Directory.")
        else:
            download_playlist(playlist_url, output_directory, selected_quality)

if __name__ == "__main__":
    main()
