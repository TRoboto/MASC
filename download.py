from __future__ import unicode_literals
import youtube_dl
import json
import os
import pandas as pd

# df = pd.read_csv('results.tsv', sep='\t')
# df_new = df.drop_duplicates('video_id')
# df_new.to_csv('results.tsv', index=False, sep='\t')

CHANNELS = 'processed_channels.json'

if not os.path.isdir('subs'):
    os.mkdir('subs')

if not os.path.isdir('logs'):
    os.mkdir('logs')


def has_arabic_subtitle(info_dict):
    if info_dict and 'subtitles' in info_dict:
        return 'ar' in info_dict['subtitles']
    return False


def get_savefile():
    save_path = 'results.tsv'
    if os.path.isfile(save_path):
        savefile = open(save_path, 'a')
    else:
        savefile = open(save_path, 'w')
        savefile.write('video_id\tcategory\tduration\tchannel_id\n')
    return savefile


def get_preprocessed_channels():
    save_path = 'processed_channels.txt'
    if os.path.isfile(save_path):
        savefile = open(save_path, 'a')
    else:
        savefile = open(save_path, 'w')
    return savefile


def is_processeed(channel, channels):
    return channel in channels


def get_channel_id(channel):
    with youtube_dl.YoutubeDL({'ignoreerrors': True}) as ydl:
        info_dict = ydl.extract_info(channel, download=False, process=False)
    return info_dict['id'] if info_dict else None


ydl_opts = {
    'subtitleslangs': ['ar'],
    'writesubtitles': True,
    'ignoreerrors': True,
    'outtmpl': 'ar_subs/%(id)s.%(ext)s',
    'skip_download': True
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],

}

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info('ytsearch:علم', download=False)
#     print(info_dict['id'])
# s
savefile = get_savefile()
processed_channels = open("processed_channels.txt").read().split('\n')
processed_channels_handler = get_preprocessed_channels()


def process_url(url, id):
    logfile = 'logs/' + id + '.json'
    try:
        if os.path.isfile(logfile):
            info_dict = json.loads(open(logfile).read())
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url)
            if not info_dict:
                return
            with open(logfile, 'w') as file:
                file.write(json.dumps(info_dict, indent=4, sort_keys=True))
    except:
        print(channel, "Not working!")
        return
    if 'entries' not in info_dict:
        return
    for entry in info_dict['entries']:
        if has_arabic_subtitle(entry):
            savefile.write(
                f"{entry['webpage_url_basename']}\t{entry['categories']}\t{entry['duration']}\t{entry['channel_id']}\n")
            savefile.flush()
    return info_dict


all_channels = open('channels.txt').read().split('\n')
for channel in all_channels:
    id = get_channel_id(channel)
    if not id or not channel or is_processeed(id, processed_channels):
        continue
    out = process_url(channel, id)
    if out is None:
        continue
    processed_channels_handler.write(id + '\n')
    processed_channels_handler.flush()
