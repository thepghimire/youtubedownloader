import os
import shutil
from pytube import Playlist, YouTube
from config import DOWNLOAD_BASE_PATH, INPUT_PLAYLIST_URLS
from timer import Timer

def get_playlist(path_to_text_file):
    with open(path_to_text_file) as f:
        text = f.read()
        text = text.split("\n")
        return text

def get_best_audio_stream(streams):
    required_abr = 0
    required_stream = None
    for stream in streams:
        if stream.mime_type == "audio/webm":
            abr = int(str(stream.abr).replace("kbps", ""))
            if abr > required_abr:
                required_abr = abr
                required_stream = stream
    return required_stream

def get_audio_streams(video_url):
    video = YouTube(video_url)
    streams = video.streams.filter(only_audio=True)
    return streams

def download_audio(stream, playlist_name, path=DOWNLOAD_BASE_PATH):
    download_path = path + playlist_name
    if stream:
        stream.download(download_path)
    print("Finished downloading {}".format(stream.title))
    
def download_single_mp3(youtube_url, playlist_name="/Mix"):
    download_timer = Timer() 
    streams = get_audio_streams(youtube_url) #(get only audio stream)
    best_stream = get_best_audio_stream(streams)
    download_audio(best_stream, playlist_name)
    download_timer.end(text="Downloading")

def clear_downloads_folder():
    for folder in os.listdir(DOWNLOAD_BASE_PATH):
        existing_folder_path = DOWNLOAD_BASE_PATH+"/"+folder
        shutil.rmtree(existing_folder_path, ignore_errors=False, onerror=None)
        return None

if __name__ == "__main__":
    clear_downloads_folder()
    playlist_list = get_playlist(INPUT_PLAYLIST_URLS)
    root_timer = Timer()
    for j, playlist_url in enumerate(playlist_list):
        playlist = Playlist(playlist_url)
        for i, video in enumerate(playlist):
            playlist_name = "/"+playlist.title if playlist.title else "/Mix"
            # download_single_mp3(video, playlist_name)
            print("Downloaded Song {}/{} \n Playlist {}/{}".format(i+1, len(playlist),j+1, len(playlist_list)))
    root_timer.end(text="Entire")
    