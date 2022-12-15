from config import DOWNLOAD_BASE_PATH, CONVERT_BASE_PATH
import subprocess
import os
from timer import Timer

path_to_webm_files = DOWNLOAD_BASE_PATH


# iterate over files in
# that directory
# for filename in os.listdir(DOWNLOAD_BASE_PATH):
#     f = os.path.join(DOWNLOAD_BASE_PATH, filename)
#     # checking if it is a file
#     if os.path.isfile(f):
#         mp3_filename = filename.replace(".webm", ".mp3")
#         output_path = DOWNLOAD_BASE_PATH + "converted/"+mp3_filename
#         print(subprocess.run(f'ffmpeg -i \"{f}\" \"{output_path}\"',shell=True,capture_output=True))
#         # print(subprocess.run('ffmpeg -i "path/filename".mp4 "filename".mp3',shell=True,capture_output=True))]

root_timer = Timer()
for root, dirs, files in os.walk(DOWNLOAD_BASE_PATH, topdown=False):
    for i, name in enumerate(files):
        # print(os.path.join(root, name))
        f = os.path.join(os.path.join(root, name))
        if os.path.isfile(f):
            mp3_filename = name.replace(".webm", ".mp3")
            playlist_name_from_root = root.split("/")[-1]
            output_path = CONVERT_BASE_PATH + f"/{playlist_name_from_root}"
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            mp3_output_path = output_path + "/" + mp3_filename
            if not os.path.exists(mp3_output_path):
                file_timer = Timer()
                print(subprocess.run(f'ffmpeg -i \"{f}\" \"{mp3_output_path}\"',shell=True,capture_output=True))
                file_timer.end("Converting into mp3")
                print("File {}/{} from playlist {}".format(i+1, len(files), playlist_name_from_root))
            else:
                print(mp3_filename + "is already present in the drive.")
                print("File {}/{} from playlist {}".format(i+1, len(files), playlist_name_from_root))
root_timer.end("Entire Conversion")