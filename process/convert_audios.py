import os
import subprocess
import concurrent.futures
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *


if not os.path.isdir(processed_audios_dir):
    os.mkdir(processed_audios_dir)

f = []
for (dirpath, dirnames, filenames) in os.walk(audios_dir):
    f.extend(filenames)
    break

args = [
    "-ar", "16000",  # convert to 16k sample rate
    "-sample_fmt", "s16",  # convert to 16 bit depth
    "-ac", "1",  # convert to mono channel
    "-loglevel", "quiet"
]


def handle_audio(file):
    output = os.path.join(processed_audios_dir, file.split('.')[0] + '.wav')
    if os.path.isfile(output):
        return
    subprocess.call(['ffmpeg', '-i', os.path.join(audios_dir, file)
                     ] + args + [output])


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(handle_audio, file) for file in f
        ]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(f)):
            pass
