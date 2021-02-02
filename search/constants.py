import os
current_dir = os.path.dirname(os.path.realpath(__file__))
results_dir = os.path.join(current_dir, 'search_results')
logs_dir = os.path.join(results_dir, 'logs')
results_file = os.path.join(results_dir, 'results.csv')
preprocessed_words_file = os.path.join(results_dir, 'processed_words.txt')
found_channels_file = os.path.join(results_dir, 'found_channels.txt')
need_check_file = os.path.join(results_dir, 'need_check.txt')
