import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from constants import *

df = pd.read_csv(results_file)
print(len(df))
df = df.drop_duplicates()
print(len(df))
df.to_csv(results_file, index=False)
