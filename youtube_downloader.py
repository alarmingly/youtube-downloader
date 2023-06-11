import tkinter as tk
from tkinter import filedialog
import yt_dlp as youtube_dl
import os

def download_video():
    link = link_entry.get()

    # Get the selected video resolution
    resolution = resolution_var.get()

    # Construct the command to download the video
    ydl_opts = {
        'outtmpl': output_directory.get() + '/%(title)s.%(ext)s',
        'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
        'merge_output_format': 'mp4',
        'ffmpeg_location': 'C:/ffmpeg/ffmpeg.exe'  # Custom FFmpeg path
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
            status_label.config(text="Video downloaded successfully!")
        except Exception as e:
            status_label.config(text="An error occurred while downloading the video.")
            print(e)

def download_audio():
    link = link_entry.get()

    # Get the selected audio format
    audio_format = audio_format_var.get()

    # Construct the command to download the audio
    ydl_opts = {
        'outtmpl': output_directory.get() + '/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': audio_format,
            'preferredquality': '192',
            'nopostoverwrites': False,
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe'  # Custom FFmpeg path
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
            status_label.config(text="Audio downloaded successfully!")
        except Exception as e:
            status_label.config(text="An error occurred while downloading the audio.")
            print(e)

def choose_output_directory():
    # Open a dialog box to choose the output directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        output_directory.set(selected_directory)

def update_mode(dummy):
    # Show or hide the format dropdowns based on the selected mode
    mode = mode_var.get()
    if mode == "Video":
        resolution_label.pack()
        resolution_dropdown.pack()
        audio_format_label.pack_forget()
        audio_format_dropdown.pack_forget()
    elif mode == "Audio":
        resolution_label.pack_forget()
        resolution_dropdown.pack_forget()
        audio_format_label.pack()
        audio_format_dropdown.pack()

# Create the main window
window = tk.Tk()
window.title("YouTube Downloader")
window.geometry("300x300")

# Output directory
output_directory = tk.StringVar(value=os.path.expanduser("~/Downloads/yt"))


# Download mode variable
mode_var = tk.StringVar()
mode_var.set("Video")

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

mode_label = tk.Label(window, text="Download Mode:")
mode_label.pack()

mode_dropdown = tk.OptionMenu(window, mode_var, "Video", "Audio", command=update_mode)
mode_dropdown.pack()

resolution_label = tk.Label(window, text="Resolution:")
resolution_var = tk.StringVar()
resolution_var.set("1080")
resolution_dropdown = tk.OptionMenu(window, resolution_var, "240", "360", "480", "720", "1080")

audio_format_label = tk.Label(window, text="Audio Format:")
audio_format_var = tk.StringVar()
audio_format_var.set("mp3")
audio_format_dropdown = tk.OptionMenu(window, audio_format_var, "mp3", "wav", "m4a")

output_button = tk.Button(window, text="Choose Directory", command=choose_output_directory)
output_button.pack()

download_button = tk.Button(window, text="Download", command=download_video)
download_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

# Start the GUI event loop
window.mainloop()
