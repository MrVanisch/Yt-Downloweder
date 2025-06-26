# YouTube Downloader

A simple GUI application for downloading YouTube videos as MP4 or MP3.

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`
- Tkinter (bundled with most Python installs)

## Installation

```bash
# Clone the repository
git clone https://github.com/username/youtube_downloader.git
cd youtube_downloader

# Install dependencies
pip install -r requirements.txt
```
##Usage

Run the application:

python main.py

Paste a YouTube URL.

Select format (MP4 or MP3).

Choose an output folder and click Download.

Wait for the download (and conversion, if MP3) to complete.

##Project Structure

youtube_downloader/
├── requirements.txt
├── main.py
├── README.md
└── modules/
    ├── __init__.py
    ├── converter.py
    ├── downloader.py
    ├── gui.py
    └── utils.py

Future Improvements

##Download queue support.

Command-line interface (CLI) version.

Support for additional video platforms.
