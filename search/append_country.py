import pandas as pd
from tqdm import tqdm
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

YOUTUBE_API = "https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&id={{id}}&key={key}".format(
    key=os.environ['API_KEY'])
UNKOWN_COUNTRY = "UNK"

df = pd.read_csv(results_file)


def add_country(channel_id):
    req = requests.get(YOUTUBE_API.format(id=channel_id)).json()
    res = req['items'][0]['snippet']
    return res['country'] if 'country' in res else UNKOWN_COUNTRY


df['country'] = pd.Series(dtype=str)
countries = {}
for i, row in tqdm(df.iterrows(), total=len(df)):
    if row['channel_id'] not in countries:
        countries[row['channel_id']] = add_country(row['channel_id'])
    df['country'].iloc[i] = countries[row['channel_id']]

df.to_csv(results_file, index=False)
