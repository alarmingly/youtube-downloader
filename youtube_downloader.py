import tkinter as tk
from tkinter import filedialog
import yt_dlp as youtube_dl
import os

print("Welcome to alarmingly's YouTube downloader")

resolution_var = None  # Define resolution_var as a global variable
audio_var = None       # Define audio_var as a global variable
subtitles_var = None   # Define subtitles_var as a global variable

def download_video():
    link = link_entry.get()

    # Get the selected video resolution
    resolution = resolution_var.get()

    # Remove the 'p' from the resolution to get the actual height value
    height = int(resolution[:-1])

    # Get the selected audio format
    audio_format = audio_var.get()

    # Check if subtitles checkbox is selected
    subtitles = subtitles_var.get()
    subtitle_args = ""
    if subtitles:
        subtitle_args = "--write-sub --write-auto-sub --sub-lang en.*"

    # Construct the command to download the video or audio
    if audio_format == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'extractaudio': True,
            'outtmpl': output_directory.get() + '/%(title)s.%(ext)s',
        }
    else:
        ydl_opts = {
            'outtmpl': output_directory.get() + '/%(title)s.%(ext)s',
            'format': f'bestvideo[height<={height}]+bestaudio/best[height<={height}]',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'subtitleslangs': subtitle_args,
        }

    # Print the command
    print("Downloading command:")
    print(ydl_opts)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
            status_label.config(text="Video downloaded successfully!")
        except Exception as e:
            status_label.config(text="An error occurred while downloading the video.")
            print(e)

def choose_output_directory():
    # Open a dialog box to choose the output directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        output_directory.set(selected_directory)

def create_output_directory():
    # Create the output directory if it doesn't exist
    directory = output_directory.get()
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("400x250")

# Output directory
output_directory = tk.StringVar(value=os.path.expanduser("~/Downloads/yt"))

# Create the widgets
link_label = tk.Label(window, text="YouTube Link:")
link_label.pack()

link_entry = tk.Entry(window)
link_entry.pack()
link_entry.focus_set()

output_label = tk.Label(window, text="Output Directory:")
output_label.pack()

output_entry = tk.Entry(window, textvariable=output_directory)
output_entry.pack()

output_button = tk.Button(window, text="Choose Directory", command=choose_output_directory)
output_button.pack()

download_button = tk.Button(window, text="Download", command=download_video)
download_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

# Resolution variable
resolution_label = tk.Label(window, text="Resolution:")
resolution_var = tk.StringVar()
resolution_var.set("1080p")
resolution_dropdown = tk.OptionMenu(window, resolution_var, "240p", "360p", "480p", "720p", "1080p")
resolution_label.pack()
resolution_dropdown.pack()

# Audio format variable
audio_label = tk.Label(window, text="Audio Format:")
audio_var = tk.StringVar()
audio_var.set("mp4")
audio_dropdown = tk.OptionMenu(window, audio_var, "mp3", "mp4")
audio_label.pack()
audio_dropdown.pack()

# Subtitles checkbox
subtitles_var = tk.BooleanVar()
subtitles_checkbox = tk.Checkbutton(window, text="Subtitles", variable=subtitles_var)
subtitles_checkbox.pack()

# Create the output directory if it doesn't exist
create_output_directory()

# Start the GUI event loop
window.mainloop()
