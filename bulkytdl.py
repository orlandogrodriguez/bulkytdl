import yt_dlp as youtube_dl
import openpyxl
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def read_excel_to_tuples(filename):
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active

    urls = []

    for row in sheet.iter_rows(values_only=True): 
        url = row[0]
        urls.append(url)

    return urls

def download_audio(youtube_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_title = info_dict.get("title", "Unknown")

    sanitized_title = sanitize_filename(video_title)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': sanitized_title,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def clean_video_url(url):
    """
    Removes 'list' and 'index' query parameters from the URL.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    query_params.pop('list', None)
    query_params.pop('index', None)

    parsed_url = parsed_url._replace(query=urlencode(query_params, doseq=True))
    return urlunparse(parsed_url)

filename = "bulk_youtube_download.xlsx"
urls = read_excel_to_tuples(filename)
for idx, url in enumerate(urls):
    print(f"===========Downloading {idx} of {len(urls)}=============")
    clean_url = clean_video_url(url)
    download_audio(clean_url)
