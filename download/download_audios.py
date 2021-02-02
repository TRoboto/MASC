from __future__ import unicode_literals
import youtube_dl
import os
import concurrent.futures
import pandas as pd
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

df = pd.read_csv(results_file)

if not os.path.isdir(audios_dir):
    os.mkdir(audios_dir)


def is_processeed(filename):
    return os.path.isfile(filename)


ydl_opts = {
    # 'subtitleslangs': ['ar'],
    # 'writesubtitles': True,
    "ignoreerrors": True,
    "outtmpl": "{}/%(id)s.%(ext)s".format(audios_dir),
    # 'skip_download': True
    "format": "bestaudio/best",
    "prefer_ffmpeg": True,
    # 'quiet': True
    # "postprocessors": [
    #     {
    #         "key": "FFmpegExtractAudio",
    #         # "preferredcodec": "wav",
    #         # "preferredquality": "192",
    #     }
    # ],
    # "postprocessor_args": [
    #     "-ar", "16000",  # convert to 16k sample rate
    #     "-sample_fmt", "s16",  # convert to 16 bit depth
    #     "-ac", "1",  # convert to mono channel
    # ],
    # "keepvideo": True,
}

VIDEO_URL = "https://www.youtube.com/watch?v={}"


def process_video(id):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VIDEO_URL.format(id)])


# process_video(df.iloc[0, 0])
if __name__ == "__main__":
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [
    #         executor.submit(process_video, arg["video_id"]) for i, arg in tqdm(df.iterrows(), total=len(df))
    #     ]
    #     for future in tqdm(concurrent.futures.as_completed(futures), total=len(df)):
    #         pass
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_video, arg["video_id"]) for i, arg in df.iterrows()
        ]
        for future in concurrent.futures.as_completed(futures):
            pass
