# Automatically Search YouTube

The automatic search is used here to search for videos with Arabic subtitles by giving the words to search for.

To search for youtube videos:

1- Collect as many words as possible (general words are preferred for collecting many videos).  
2- Save the collected words in a file named `search_words.txt` in this directory.  
3- Run `search.py` python file and wait for it to finish looking for videos with Arabic subtitle:

```
python3 search.py
```

4- Run `append_country.py` if you want to add the country of each channel to the csv file.

```
python3 append_country.py
```

5- Run `remove_duplicates.py' to remove duplicates in the csv file.

```
python3 remove_duplicates.py
```

6- Now find `results.csv` file in `search_results` directory to get the results. If you want to validate channels, move to the next step.

7- Run `filter_search.py` to create `need_check.csv` file. This file will contain one video from each channel for validation.

```
python3 filter_search.py
```

8- Run `add_complete.py` to move the channels inside `need_check.csv` to `processed_channels.txt` file.

9- You can now add more words are repeats all the steps to get more videos.
