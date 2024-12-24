import os
import threading
from yt_dlp import YoutubeDL
from moviepy.audio.io.AudioFileClip import AudioFileClip
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def download_youtube_video_as_mp4(url, output_directory, progress_callback=None):
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_callback] if progress_callback else [],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info_dict)

        return video_path
    except Exception as e:
        raise Exception(f"Error downloading video: {e}")

def convert_mp4_to_mp3(video_path):
    try:
        base, ext = os.path.splitext(video_path)
        mp3_path = base + ".mp3"

        with AudioFileClip(video_path) as audio:
            audio.write_audiofile(mp3_path)

        return mp3_path
    except Exception as e:
        raise Exception(f"Error converting video to MP3: {e}")

def download_and_process(url, output_directory, convert_to_mp3, progress_callback):
    try:
        video_path = download_youtube_video_as_mp4(url, output_directory, progress_callback)

        if convert_to_mp3:
            mp3_path = convert_mp4_to_mp3(video_path)
            os.remove(video_path)  # Remove MP4 file after conversion
            return mp3_path
        else:
            return video_path
    except Exception as e:
        raise e

def start_download_thread():
    threading.Thread(target=start_download).start()

def start_download():
    url = url_entry.get()
    output_directory = filedialog.askdirectory(title="Select Output Directory")

    if not url or not output_directory:
        messagebox.showerror("Error", "URL and output directory are required!")
        return

    progress_bar.start()

    def progress_callback(d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 1)
            percent = int(downloaded / total * 100)
            progress_bar['value'] = percent
            root.update_idletasks()

    try:
        if format_var.get() == "MP3":
            file_path = download_and_process(url, output_directory, convert_to_mp3=True, progress_callback=progress_callback)
        else:
            file_path = download_and_process(url, output_directory, convert_to_mp3=False, progress_callback=progress_callback)

        messagebox.showinfo("Success", f"File saved: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        progress_bar.stop()
        progress_bar['value'] = 0

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x250")

frame = tk.Frame(root)
frame.pack(pady=20)

url_label = tk.Label(frame, text="YouTube URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = tk.Entry(frame, width=40)
url_entry.grid(row=0, column=1, padx=5, pady=5)

format_label = tk.Label(frame, text="Format:")
format_label.grid(row=1, column=0, padx=5, pady=5)

format_var = tk.StringVar(value="MP4")
format_mp4 = tk.Radiobutton(frame, text="MP4", variable=format_var, value="MP4")
format_mp3 = tk.Radiobutton(frame, text="MP3", variable=format_var, value="MP3")

format_mp4.grid(row=1, column=1, sticky="w", padx=5, pady=5)
format_mp3.grid(row=1, column=1, sticky="e", padx=5, pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

download_button = tk.Button(root, text="Download", command=start_download_thread)
download_button.pack(pady=10)

root.mainloop()
