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

def get_best_video_stream(streams):
    required_stream = None
    for stream in streams:
        if stream.mime_type == "video/mp4" and stream.resolution is not None:
            if stream.resolution == "1080p":
                required_stream = stream
                break
    return required_stream

def get_best_audio_stream(streams):
    required_abr = 0
    required_stream = None
    for stream in streams:
        if stream.mime_type == "audio/webm" and stream.abr is not None:
            abr = int(str(stream.abr).replace("kbps", ""))
            if abr > required_abr:
                required_abr = abr
                required_stream = stream
    return required_stream

def get_video_streams(video_url):    
    video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    try:
        streams = video.streams.filter(adaptive=True)
    except Exception as e:
        return None
    return streams

def get_audio_streams(video_url):
    video = YouTube(video_url, use_oauth=True, allow_oauth_cache=True)
    try:
        streams = video.streams.filter()
    except Exception as e:
        return None
    return streams

def download_audio(stream, playlist_name, path=DOWNLOAD_BASE_PATH, vid_audio=False):
    download_path = path + playlist_name if vid_audio else path + playlist_name
    if stream:
        print("Started downloading {}".format(stream.title))
        stream.download(download_path)
        print("Finished downloading Song.")
    
def download_single_mp4(youtube_url, playlist_name="/Mix"):
    download_timer = Timer() 
    streams = get_video_streams(youtube_url)
    if streams is not None:
        best_stream = get_best_video_stream(streams)
        download_audio(best_stream, playlist_name)
        best_audio_stream = get_best_audio_stream(streams)
        download_audio(best_audio_stream, playlist_name, vid_audio=True)
        download_timer.end(text="Downloading")


def clear_downloads_folder():
    for folder in os.listdir(DOWNLOAD_BASE_PATH):
        existing_folder_path = DOWNLOAD_BASE_PATH+"/"+folder
        shutil.rmtree(existing_folder_path, ignore_errors=False, onerror=None)
        return None

if __name__ == "__main__":
    clear_downloads = False 
    if clear_downloads:
        clear_downloads_folder()
    playlist_list = get_playlist(INPUT_PLAYLIST_URLS)
    root_timer = Timer()
    for j, playlist_url in enumerate(playlist_list):
        playlist = Playlist(playlist_url)
        for i, video in enumerate(playlist):
            playlist_name = "/"+playlist.title if playlist.title else "/Mix"
            download_single_mp4(video, playlist_name)
            print("Downloaded Song {}/{} \n Playlist {}/{}".format(i+1, len(playlist),j+1, len(playlist_list)))
    root_timer.end(text="Entire")
    