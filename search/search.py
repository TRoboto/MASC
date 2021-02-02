from __future__ import unicode_literals
import youtube_dl
import json
import os
import re
import requests
import concurrent.futures
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

if not os.path.isdir(results_dir):
    os.mkdir(results_dir)

if not os.path.isdir(logs_dir):
    os.mkdir(logs_dir)

youtubeApi = "https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={{video_id}}&key={key}".format(
    key=os.environ['API_KEY'])


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


def get_preprocessed_words():
    if os.path.isfile(preprocessed_words_file):
        savefile = open(preprocessed_words_file, 'a', encoding='utf8')
    else:
        savefile = open(preprocessed_words_file, 'w', encoding='utf8')
    return savefile


def is_arabic(video_id):
    link = youtubeApi.format(video_id=video_id)
    data = requests.get(link).json()
    # with open(video_id + '.json', 'w', encoding='utf8') as file:
    #     file.write(json.dumps(data, indent=4, sort_keys=True))
    snip = data['items'][0]['snippet']
    # return 'defaultAudioLanguage' not in snip or ('ar' in snip['defaultAudioLanguage'])
    return re.search(r'[\u0621-\u064A]+', snip['title']) or \
        re.search(r'[\u0621-\u064A]+', snip['description']) or \
        ('defaultAudioLanguage' in snip and (
            'ar' in snip['defaultAudioLanguage']))


def is_processeed(word, words):
    return word in words


ydl_opts = {
    'subtitleslangs': ['ar'],
    'ignoreerrors': True,
    'cachedir': os.path.join(results_dir, 'cache'),
    "writesubtitles": True,
    'outtmpl': os.path.join(results_dir, 'tmp/%(id)s.%(ext)s'),
    "xargs": "-P 8",
    'skip_download': True
}
savefile = get_savefile()
processed_words_handler = get_preprocessed_words()
processed_words = open(os.path.join(
    results_dir, "processed_words.txt"), 'r', encoding='utf8').read().split('\n')


def process_word(word):
    logfile = os.path.join(logs_dir, word + '.json')
    if os.path.isfile(logfile):
        return False
    else:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                f"ytsearchall:{word}", download=False)
        if not info_dict:
            return False
        with open(logfile, 'w', encoding='utf8') as file:
            file.write(json.dumps(info_dict, indent=4, sort_keys=True))
    if 'entries' not in info_dict:
        return False
    for entry in info_dict['entries']:
        if has_arabic_subtitle(entry) and is_arabic(entry['webpage_url_basename']):
            savefile.write(
                f"{entry['webpage_url']},{entry['categories']},{entry['duration']},{entry['channel_id']}\n")
            savefile.flush()
    return True


search_file = os.path.join(current_dir, 'search_words.txt')
if os.path.isfile(search_file):
    raise ValueError("Please add search_words.txt file.")
all_words = open(os.path.join(current_dir, 'search_words.txt'),
                 'r', encoding='utf8').read().split('\n')


def handle_word(word):
    word = word.strip()
    if is_processeed(word, processed_words):
        return
    out = process_word(word)
    if not out:
        return
    processed_words.append(word)
    processed_words_handler.write(word + '\n')
    processed_words_handler.flush()


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {executor.submit(handle_word, word): word for word in all_words}
        for future in concurrent.futures.as_completed(futures):
            pass
    # for word in all_words:
    #     handle_word(word)
