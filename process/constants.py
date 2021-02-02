import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{current_dir[:current_dir.rindex("/")]}')
print(sys.path)
from download.constants import audios_dir, results_file, substitle_dir
processed_audios_dir = os.path.join(current_dir, 'processed_audios')
chunks_dir = os.path.join(current_dir, 'chunks')
chunks_file = os.path.join(current_dir, 'chunks.csv')

chars = 'دجحإﻹﻷأآﻵخهعغفقثصضذطكمنتالبيسشظزوةىﻻرؤءئ0123456789'
