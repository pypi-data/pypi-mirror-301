import yt_dlp, os, sys

def download_audio(url):
    dir = os.path.dirname(os.path.abspath(__file__)) + '/audio'
    options = {
        'format': 'bestaudio',
        'extractaudio': True,
        'audioformat': 'flac',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
        'outtmpl': f'{dir}/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"\n\n[Download] - Error: {e}")
        sys.exit(1)

    print("\n\n[Download] - Downloaded audio successfully")