# Contains the utility functions that we will be using in our project
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import subprocess, json, requests, sys, os, argparse
from constants import *

def load_in_json(games_reviews_json_file_path):
	with open(games_reviews_json_file_path, 'r') as r_file:
	    json_data = json.load(r_file)

	for k in json_data.keys():
	    sp = ['python', harvest_reviews_script_file_path, '-output_folder', game_reviews_data_output_directory, k]
	    subprocess.run(sp)

	print('Done')

def app_selector(genre_in, steam_apps_file_path, output_path, app_id_offset,tags_out, max_out):
    """
    C-style main function.
    :return: None.
    """
	all_steam_apps = load_all_steam_app_ids()
	after_offset = True if app_id_offset is None else False
	count = len(all_steam_apps)
	check_genre = lambda g: True if (g['id'] == args.genre_in) or (g['description'] == args.genre_in) else False
	remaining = max_out if max_out is not None else len(all_steam_apps) + 1
	harvested_apps = {}
	last_app_added = None
	visited, genre_filter, type_filter, tag_filter, parse_fail = 0, 0, 0, 0, 0

def load_all_steam_app_ids():
    if not os.path.exists(apps_file_path):
        sys.exit('File not found: %s' % steam_apps_file_path)
    with open(steam_apps_file_path, "r") as w_file:
        return json.load(w_file)['applist']['apps']

def steam_app_traversal(all_steam_apps):
	 # go app by app
	for i, app in enumerate(all_steam_apps):
	    # skip previous to the offset and after download limit is reached
	    if app['appid'] == app_id_offset:
	        after_offset = True
	        continue
	    elif not after_offset:
	        continue
    # http request one by one
    print("Exploring app %d out of %d apps..." % (i, count))
    visited += 1

def get_genre_details():
        # get details for the genre
        details_url_address, tags_url_address = DETAILS_URL_FRAME % app['appid'], None
        if False:
            print(details_url_address)
            quit()
        try:
            details_all_content = requests.get(details_url_address).json()[str(app['appid'])]['data']
            if True not in map(check_genre, details_all_content['genres']):
                gender_filter += 1
                print('...out: Not in gender')
                continue

            if details_all_content["type"] != "game":
                type_filter += 1
                print('...out: Not a game')
                continue

            # check if pass tags filter
            if args.tags_out is not None:
                tags_url_address = TAGS_URL_FRAME % app['appid']
                tags_list = requests.get(tags_url_address).json()["tags"]
                if isinstance(tags_list, dict) and (len(tags_list) > 0):
                    if len([t for t in args.tags_out if t in tags_list.keys()]) > 0:
                        print('...out: black-list tag')
                        tag_filter += 1
                        continue
            else:
                tags_list = {}

            harvested_apps[app['appid']] = {
                "type": details_all_content['type'],
                "name": details_all_content['name'],
                "tags": tags_list}
            last_app_added = app['appid']
            print('...in! Tags: {0}'.format(tags_list))
        except KeyError as e:
            print('...out: strange result from "%s" or "%s"' % (details_url_address, tags_url_address))
            print("     KeyExcept: {0}".format(e))
            parse_fail += 1
            continue
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print('...out: strange result from "%s" or "%s"' % (details_url_address, tags_url_address))
            print("     Except: {0} -> {1}".format(type(e), e))
            print("     Except: {0} -> {1}".format(exc_obj, exc_tb.tb_lineno))
            parse_fail += 1
            continue

        # check if it reached its limit
        remaining -= 1
        if remaining <= 0:
            break

def summary_printer(harvested_apps, visited, genre_filter, type_filter, tag_filter, 
	parse_fail, last_app_added, summary_output_directory):
    print("Summary:")
    print("      Apps found: %d" % len(harvested_apps.keys()))
    print("         Visited: %d" % visited)
    print(" Genre filtered: %d" % genre_filter)
    print("     Type filter: %d" % type_filter)
    print("      Tag filter: %d" % tag_filter)
    print("      Parse fail: %d" % parse_fail)
    print("  Last app added: %d" % last_app_added)

    with open(summary_output_directory, "w") as w_file:
        json.dump(harvested_apps, w_file, indent=4, sort_keys=True)
    print("Wrote file: %s" % summary_output_directory)

def skipgrammify_data(data, vocab_size, window_size):
	sampling_table = sequence.make_sampling_table(vocab_size)
	couples, labels = skipgrams(data, vocab_size, window_size=window_size, sampling_table=sampling_table)
	word_target, word_context = zip(*couples)
	word_target = np.array(word_target, dtype="int32")
	word_context = np.array(word_context, dtype="int32")

	return word_target, word_context, couples, labels