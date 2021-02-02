import os
import csv
import pandas as pd
import subprocess
from collections import Counter
from tqdm import tqdm
import webvtt
import concurrent.futures
import re
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *


df = pd.read_csv(results_file)

if not os.path.isdir(chunks_dir):
    os.mkdir(chunks_dir)

csvfile = open(chunks_file, "w", encoding="utf-8")
csvwriter = csv.writer(csvfile)
csvwriter.writerow(["wav_filename", "wav_filesize",
                    "transcript", "start", "end", "video_id"])

counts = Counter()


def keep_arabic_and_numbers_only(text):
    # remove tashkeel
    text = re.sub("[ًٌٍَُِّ~ْ]", "", text)
    spaced_text = re.sub(f"[^{chars}]", " ", text)
    cleaned = re.sub(' +', ' ', ''.join(spaced_text))
    return cleaned.strip()


def process_chunk(video_id, start, end, transcipt):
    if not transcipt:
        return
    vid = os.path.join(processed_audios_dir, video_id + ".wav")
    counts.update({video_id: 1})
    filename = os.path.join(
        chunks_dir, f"{video_id}_chunk{counts[video_id]}.wav")
    if not os.path.isfile(filename):
        cmd = ['sox', vid, filename, 'trim', str(start), f"={end}"]
        subprocess.run(cmd)
    csvwriter.writerow(
        [filename, os.path.getsize(filename), transcipt, round(start, 3), round(end, 3), video_id])


def time_to_sec(time_str):
    return sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(time_str.split(":"))))


def process_row(row):
    video_id = row['video_id']
    file = os.path.join(substitle_dir, '{}.ar.vtt'.format(video_id))
    for caption in webvtt.read(file):
        text = keep_arabic_and_numbers_only(caption.text)
        start = time_to_sec(caption.start)
        end = time_to_sec(caption.end)
        length = row['duration']
        if text and length >= end:
            process_chunk(video_id, start, end, text)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_row, row)
                   for _, row in tqdm(df.iterrows(), total=len(df))]
        for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            pass
