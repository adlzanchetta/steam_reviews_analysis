import argparse
import requests
import json
import sys
import os


# ## BASIC CHECK ##################################################################################################### #

if int(sys.version[0]) != 3:
    sys.exit("You are not using Python 3. You don't deserve to use this script. Shame on you.")

# ## ARGS ############################################################################################################ #

parser = argparse.ArgumentParser(description='This script harvests apps meta information from Valve\'s Steam API.')
parser.add_argument('-genre', metavar='G', type=str, required=True,
                    help="Steam's tag to be used as filter.")
parser.add_argument('-steam_apps_file_path', type=str, required=True, metavar='I',
                    help="Mandatory. Path of the input .json file that has all available steam app ids.")
parser.add_argument('-app_id_offset', type=int, metavar='A',
                    help="Steam App ID from where to start.")
parser.add_argument('-output_path', type=str, required=True, metavar='O',
                    help="Mandatory. Path of the output file or folder where .csv files will be written.")
parser.add_argument('-max', type=int, default=None, required=False, metavar='M',
                    help="Maximum number of apps to be harvested - integer. Default: retrieve as much as possible.")
args = parser.parse_args()

# ## CONS ############################################################################################################ #

REVIEW_URL_FRAME = "https://store.steampowered.com/api/appdetails?appids=%d"

# ## DEFS ############################################################################################################ #


def load_all_steam_app_ids():
    """

    :return:
    """
    if not os.path.exists(args.steam_apps_file_path):
        sys.exit('File not found: %s' % args.steam_apps_file_path)
    with open(args.steam_apps_file_path, "r") as w_file:
        return json.load(w_file)['applist']['apps']


def main():
    """
    C-style main function.
    :return: None.
    """
    all_steam_apps = load_all_steam_app_ids()
    after_offset = True if args.app_id_offset is None else False
    count = len(all_steam_apps)
    check_genre = lambda g: True if (g['id'] == args.genre) or (g['description'] == args.genre) else False
    remaining = args.max if args.max is not None else len(all_steam_apps) + 1
    harvested_apps = {}
    last_app_added = None

    # go app by app
    for i, app in enumerate(all_steam_apps):
        # skip previous to the offset and after download limit is reached
        if app['appid'] == args.app_id_offset:
            after_offset = True
            continue
        elif not after_offset:
            continue

        # http request one by one
        print("Exploring app %d out of %d apps..." % (i, count))
        url_address = REVIEW_URL_FRAME % app['appid']
        try:
            all_content = requests.get(url_address).json()[str(app['appid'])]['data']
            if True not in map(check_genre, all_content['genres']):
                print('...out...')
                continue
            harvested_apps[app['appid']] = {
                "type": all_content['type'],
                "name": all_content['name']}
            last_app_added = app['appid']
            print('...in!')
        except Exception:
            print('...out: strange result from "%s"' % url_address)
            continue

        # check if it reached its limit
        remaining -= 1
        if remaining <= 0:
            break

    print("Last app added: %d" % last_app_added)

    with open(args.output_path, "w") as w_file:
        json.dump(harvested_apps, w_file, indent=4, sort_keys=True)
    print("Wrote file: %s" % args.output_path)

    return


# ## CALL ############################################################################################################ #

if __name__ == '__main__':
    main()
