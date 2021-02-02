import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

if not os.path.isfile(found_channels_file):
    found_channels = open(found_channels_file, 'w')
else:
    found_channels = open(found_channels_file, 'a')

df = pd.read_csv(results_file)
processed_channels = open(found_channels_file).read().split('\n')

print('all:', len(df))
df = df[~df['channel_id'].isin(processed_channels)]
print('not processed:', len(df))

df = df.drop_duplicates()
# keep only 1 video from each channel
df = df.groupby('channel_id').head(1).sort_values('channel_id')
print('videos:', len(df))

df.to_csv(need_check_file, index=False)
