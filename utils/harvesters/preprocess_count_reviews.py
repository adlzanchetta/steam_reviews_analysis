from datetime import datetime
from datetime import timedelta
import argparse
import json
import csv
import sys
import os

# ## BASIC CHECK ##################################################################################################### #

if int(sys.version[0]) != 3:
    sys.exit("You are not using Python 3. You don't deserve to use this script. Shame on you.")

# ## ARGS ############################################################################################################ #

parser = argparse.ArgumentParser(description='This script harvests textual reviews from Valve\'s Steam API.')
parser.add_argument('-input_folder', type=str, metavar='I', required=True,
                    help="Path for the folder containing all .csv files with all reviews to be read.")
parser.add_argument('-output_file', type=str, metavar='O', required=True,
                    help="Path to the .json file to be written.")
args = parser.parse_args()

# ## CONS ############################################################################################################ #


# ## DEFS ############################################################################################################ #

def convert_csv_obj(csv_obj):
    """

    :param csv_obj:
    :return:
    """
    dict_retn = {"date": [], "positive": [], "negative": [], "empty": [], "total": []}
    min_date, max_date = str(min([int(k) for k in csv_obj.keys()])), str(max([int(k) for k in csv_obj.keys()]))
    cur_date = min_date
    while cur_date <= max_date:
        dict_retn["date"].append(cur_date)
        if cur_date in csv_obj.keys():
            dict_retn["positive"].append(csv_obj[cur_date]["positive"])
            dict_retn["negative"].append(csv_obj[cur_date]["negative"])
            dict_retn["empty"].append(csv_obj[cur_date]["empty"])
            dict_retn["total"].append(csv_obj[cur_date]["total"])
        else:
            dict_retn["positive"].append(0)
            dict_retn["negative"].append(0)
            dict_retn["empty"].append(0)
            dict_retn["total"].append(0)

        # get next date
        cur_date = str(cur_date)
        cur_date = datetime(int(cur_date[0:4]), int(cur_date[4:6]), int(cur_date[6:8])) + timedelta(days=1)
        cur_date = cur_date.strftime('%Y%m%d')

    return dict_retn


def read_csv_file(file_path):
    """
    Read a csv file and returns a dictionary
    :param file_path:
    :return: Dictionary with date in [YYYYMMDD], positive reviews, negative reviews, total reviews
    """

    # read file content into a dictionary
    dict_temp = {}
    with open(file_path, 'r') as r_file:
        csv_file = csv.DictReader(r_file, delimiter=',')
        for line in csv_file:
            date = datetime.utcfromtimestamp(int(line['timestamp_updated'])).strftime('%Y%m%d')
            if date not in dict_temp.keys():
                dict_temp[date] = {'positive': 0, 'negative': 0, 'empty': 0, 'total': 0}
            if line['voted_up']:
                dict_temp[date]['positive'] += 1
            else:
                dict_temp[date]['negative'] += 1
            if line['review'].strip() == "":
                dict_temp[date]['total'] += 1
            dict_temp[date]['total'] += 1

    dict_retn = convert_csv_obj(dict_temp)

    return dict_retn


def main(inp_fdpa, out_fipa):
    """
    C-style main function.
    :return: None.
    """

    all_files = [os.path.join(inp_fdpa, fina) for fina in os.listdir(inp_fdpa)]
    all_dicts = [read_csv_file(fipa) for fipa in all_files]
    big_dict = dict([(os.path.basename(os.path.splitext(fd[0])[0]), fd[1]) for fd in zip(all_files, all_dicts)])
    with open(out_fipa, 'w') as w_file:
        # json.dump(big_dict, w_file, indent=4)
        json.dump(big_dict, w_file)
    print("Wrote %d keys at: %s" % (len(big_dict.keys()), out_fipa))

    return


# ## CALL ############################################################################################################ #

if __name__ == '__main__':
    main(args.input_folder, args.output_file)
