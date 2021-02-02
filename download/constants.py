import os
current_dir = os.path.dirname(os.path.realpath(__file__))
results_dir = os.path.join(current_dir, 'download_results')
logs_dir = os.path.join(results_dir, 'logs')
substitle_dir = os.path.join(results_dir, 'substitles')
audios_dir = os.path.join(results_dir, 'audios')
results_file = os.path.join(results_dir, 'results.csv')
processed_channels_file = os.path.join(results_dir, 'processed_channels.txt')
channel_file = os.path.join(current_dir, 'channels.txt')
