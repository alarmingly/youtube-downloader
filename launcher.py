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
    print("ffmpeg.exe is in path, starting downloader")
else:
    # Download ffmpeg.exe in the working directory
    print("Downloading ffmpeg, please wait... (please restart launcher after download)")
    ffmpeg_url = "https://doc-0c-3c-docs.googleusercontent.com/docs/securesc/ss7240c9he2j2lodsphjplsgtjals8ie/vhr2uqo24427bkdkktjjpr773ob5ce42/1695752475000/09198439836552388044/09198439836552388044/17tz0XAAfYPQom5poCbyA4TEXDlDqJuZb?e=download"
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
