# BulkYtDl
Bulk youtube to mp3 download tool

## Setup
First clone the repository and navigate to it. I recommend building a virtual environment to manage dependencies easier:

```
python -m venv venv
source venv/bin/activate
```

Now we install the dependencies:
```
pip install openpyxl
pip install yt-dlp
```

There is one more that is quite chunky, not 100% sure you need it but feel free to install it if you run into issues:
```
brew install ffmpeg
```

To download the list of videos, add your list of youtube URLs to an xlsx file in column A.

To run, navigate to the directory and run:
```
python3 bulkytdl.py
```
