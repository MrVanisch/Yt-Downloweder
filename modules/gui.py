import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from .downloader import download_video
from .converter import mp4_to_mp3

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("400x200")
        self._build_widgets()

    def _build_widgets(self):
        # URL
        tk.Label(self, text="URL YouTube:").pack(pady=(10,0))
        self.url_var = tk.StringVar()
        tk.Entry(self, textvariable=self.url_var, width=50).pack(pady=5)

        # Format
        tk.Label(self, text="Format: ").pack()
        self.format_var = tk.StringVar(value="MP4")
        formats = ("MP4", "MP3")
        ttk.Combobox(self, values=formats, textvariable=self.format_var, state="readonly").pack(pady=5)

        # Przyciski
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Wybierz folder", command=self._choose_folder).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Pobierz", command=self._start_download).pack(side=tk.LEFT, padx=5)

        # Pasek postępu
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

    def _choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder = folder

    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Uwaga", "Podaj URL!")
            return
        threading.Thread(target=self._download_thread, args=(url,), daemon=True).start()

    def _download_thread(self, url):
        try:
            # pobierz video
            path = download_video(url, out_dir=getattr(self, 'download_folder', None), progress_hook=self._progress_hook)  # użycie parametru out_dir zgodnie z sygnaturą funkcji
            # konwertuj, jeśli MP3
            if self.format_var.get() == "MP3":
                path = mp4_to_mp3(path)
            messagebox.showinfo("Gotowe", f"Zapisano plik: {path}")
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
        finally:
            self.progress_bar.stop()
            self.progress_bar['value'] = 0

    def _progress_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes', 1)
            downloaded = d.get('downloaded_bytes', 0)
            pct = int(downloaded / total * 100)
            self.progress_bar['value'] = pct
            self.update_idletasks()