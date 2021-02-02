from __future__ import unicode_literals
import requests
import youtube_dl
import json
import os
import concurrent.futures
from bs4 import BeautifulSoup
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

if not os.path.isdir(results_dir):
    os.mkdir(results_dir)

if not os.path.isdir(substitle_dir):
    os.mkdir(substitle_dir)

if not os.path.isdir(logs_dir):
    os.mkdir(logs_dir)


def has_arabic_subtitle(info_dict, lang='ar'):
    if info_dict and 'subtitles' in info_dict:
        return lang in info_dict['subtitles']
    return False


def get_savefile():
    if os.path.isfile(results_file):
        savefile = open(results_file, 'a')
    else:
        savefile = open(results_file, 'w')
        savefile.write('video_id,category,duration,channel_id\n')
    return savefile


def get_preprocessed_channels():
    if os.path.isfile(processed_channels_file):
        savefile = open(processed_channels_file, 'a')
    else:
        savefile = open(processed_channels_file, 'w')
    return savefile


def is_processeed(channel, channels):
    return channel in channels


def get_channel_id(channel):
    if not channel:
        return
    req = requests.get(channel)
    if not req:
        return
    soup = BeautifulSoup(req.text, 'html.parser')
    elm = soup.find("meta", {"itemprop": "channelId"})
    if not elm:
        with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
            info_dict = ydl.extract_info(
                channel, download=False, process=False)
        return info_dict['id'] if info_dict else None
    return elm['content']


ydl_opts = {
    'subtitleslangs': ['ar'],
    'writesubtitles': True,
    'ignoreerrors': True,
    'outtmpl': os.path.join(substitle_dir, '%(id)s.%(ext)s'),
    'skip_download': True
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],

}

VIDEOS_URL = 'https://www.youtube.com/channel/{}/videos'
savefile = get_savefile()
processed_channels_handler = get_preprocessed_channels()
processed_channels = open(processed_channels_file).read().split('\n')


def process_channel(id):
    logfile = os.path.join(logs_dir, id + '.json')
    try:
        if os.path.isfile(logfile):
            info_dict = json.load(open(logfile))
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(VIDEOS_URL.format(id))
            if not info_dict:
                print(f'Cannot download from channel {VIDEOS_URL.format(id)}')
                return
            with open(logfile, 'w', encoding='utf8') as file:
                file.write(json.dumps(info_dict, indent=4, sort_keys=True))
    except youtube_dl.utils.DownloadError as e:
        print(
            f'Cannot download from channel {VIDEOS_URL.format(id)}, error: {e}')
        return
    if 'entries' not in info_dict:
        print(f'Entries not found for channel {VIDEOS_URL.format(id)}')
        return
    for entry in info_dict['entries']:
        if has_arabic_subtitle(entry):
            savefile.write(
                f"{entry['webpage_url_basename']},{entry['categories']},{entry['duration']},{entry['channel_id']}\n")
            savefile.flush()
    return info_dict


if not os.path.isfile(channel_file):
    raise ValueError("Please add channels.txt file.")
all_channels = open(channel_file).read().split('\n')


def handle_channel(channel):
    id = get_channel_id(channel)
    if not id or not channel or is_processeed(id, processed_channels):
        return
    out = process_channel(id)
    if out is None:
        return
    all_channels.append(id)
    processed_channels_handler.write(id + '\n')
    processed_channels_handler.flush()


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(handle_channel, arg)                   : arg for arg in all_channels}
        for future in concurrent.futures.as_completed(futures):
            pass
