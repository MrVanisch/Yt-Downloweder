
import os
from yt_dlp import YoutubeDL
from .utils import ensure_dir

def download_video(url: str, out_dir: str, format: str = 'mp4', progress_hook=None) -> str:
    ensure_dir(out_dir)
    opts = {
        'format': format,
        'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook] if progress_hook else [],
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
