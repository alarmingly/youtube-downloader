import subprocess
import importlib.util
import requests

# Check if yt_dlp module is installed
spec = importlib.util.find_spec("yt_dlp")
if spec is None:
    print("yt_dlp module not found. Installing...")
    subprocess.check_call(["pip", "install", "yt-dlp"])

# Import yt_dlp module
import yt_dlp

# Fetch the code from the URL
url = "https://raw.githubusercontent.com/alarmingly/youtube-downloader/main/youtube_downloader.py"
response = requests.get(url)
code = response.text

# Execute the code without saving the downloaded files
with yt_dlp.YoutubeDL({'nooverwrites': True}) as ydl:
    exec(code)
