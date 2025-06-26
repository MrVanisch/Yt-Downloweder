import os
from moviepy.audio.io.AudioFileClip import AudioFileClip

def mp4_to_mp3(video_path: str) -> str:
    base, _ = os.path.splitext(video_path)
    mp3 = base + '.mp3'
    with AudioFileClip(video_path) as clip:
        clip.write_audiofile(mp3)
    os.remove(video_path)
    return mp3
