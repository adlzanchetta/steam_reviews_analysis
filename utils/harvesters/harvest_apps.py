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
parser.add_argument('-output_path', type=str, required=True, metavar='O',
                    help="Mandatory. Path of the output file or folder where .csv files will be written.")
args = parser.parse_args()

# reading arguments
output_path = args.output_path

# ## CONS ############################################################################################################ #

ALLAPPS_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
DEFAULT_FILE_NAME = "steam_apps.json"


# ## DEFS ############################################################################################################ #

def set_up_output_file_path(path):
    """
    Just ensure we end up with a correct .json file path to write in.
    :param path: String. A system path that can be either a folder path of a .json file path.
    :return: String. The ultimate output file path.
    """
    if os.path.isdir(path):
        return os.path.join(path, DEFAULT_FILE_NAME)
    elif path.endswith('.json'):
        return path
    else:
        sys.exit("Output path is not a valid directory and is not a .json file path.")


def main():
    """
    C-style main function.
    :return: None.
    """
    with open(set_up_output_file_path(output_path), "w") as w_file:
        print("Performing HTTP request...")
        json.dump(requests.get(ALLAPPS_URL).json(), w_file, indent=4, sort_keys=True)
    print("Wrote file: %s" % output_path)


# ## CALL ############################################################################################################ #

if __name__ == '__main__':
    main()
