import yt_dlp
import os, random, vlc, time

#Mostly AI, next refactor should take care of that
def download_best_audio(url):
    if not os.path.exists('./media'):
        os.makedirs('./media')
        
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',  # Prefer m4a, fallback to anything
        'outtmpl': './media/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '0',  # Best quality
        }],
        'merge_output_format': 'm4a',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


