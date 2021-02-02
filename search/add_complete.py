import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *


if not os.path.isfile(found_channels_file):
    raise ValueError("Please run filter_search.py first.")
found_channels = open(found_channels_file).read().split('\n')
df = pd.read_csv(need_check_file)
channels = list(set(df['channel_id'].unique().tolist() + found_channels))
open(found_channels_file, 'w').write('\n'.join(channels))
