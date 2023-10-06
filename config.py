import os 

def get_path(foldername):
    cwd = os.getcwd()
    input_path = cwd +"/"+foldername
    
    def check_path(input_path):
        return True if os.path.exists(input_path) else False 
    
    if check_path(input_path):
        path = input_path  
    else:
        os.mkdir(foldername)
        if check_path(input_path):
            path = input_path 
    return path 

DOWNLOAD_BASE_PATH = get_path("downloaded_new")
CONVERT_BASE_PATH = get_path("converted")
INPUT_PLAYLIST_URLS = os.getcwd() + "/playlist_urls.txt"        