import subprocess
import importlib.util
import requests
import sys
import os

# Check if yt_dlp module is installed
spec = importlib.util.find_spec("yt_dlp")
if spec is None:
    print("yt_dlp module not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])

# Import yt_dlp module
import yt_dlp

# Check if ffmpeg.exe already exists in the working directory
ffmpeg_filename = "ffmpeg.exe"
if os.path.exists(ffmpeg_filename):
    print("ffmpeg.exe already exists. Skipping download.")
else:
    # Download ffmpeg.exe in the working directory
    print("Downloading ffmpeg, please wait...")
    ffmpeg_url = "https://cdn-153.anonfiles.com/kaL4b91bz3/372840d7-1688848906/ffmpeg.exe"
    ffmpeg_response = requests.get(ffmpeg_url, stream=True)

    # Get the total file size
    total_size = int(ffmpeg_response.headers.get('content-length', 0))
    bytes_downloaded = 0

    with open(ffmpeg_filename, "wb") as ffmpeg_file:
        for chunk in ffmpeg_response.iter_content(chunk_size=4096):
            ffmpeg_file.write(chunk)
            bytes_downloaded += len(chunk)
            progress = round(bytes_downloaded / total_size * 100, 2)
            sys.stdout.write(f"\rProgress: {progress}%")
            sys.stdout.flush()

    print("\nffmpeg download complete.")

# Fetch the code from the URL
url = "https://raw.githubusercontent.com/alarmingly/youtube-downloader/main/youtube_downloader.py"
response = requests.get(url)
code = response.text

# Execute the code without saving the downloaded files
with yt_dlp.YoutubeDL({'nooverwrites': True, 'ffmpeg_location': './ffmpeg.exe'}) as ydl:
    exec(code)
