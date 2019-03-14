from collections import deque
import requests
import argparse
import sys
import csv
import os

# ## BASIC CHECK ##################################################################################################### #

if int(sys.version[0]) != 3:
    sys.exit("You are not using Python 3. You don't deserve to use this script. Shame on you.")

# ## ARGS ############################################################################################################ #

parser = argparse.ArgumentParser(description='This script harvests textual reviews from Valve\'s Steam API.')

# list of Steam app ids (440: Team Fortress 2, 221380: Age of Empires 2, 26800: Braid, 582660: Black Desert Online)
parser.add_argument('app_ids', metavar='APP_ID', type=int, nargs='+',
                    help="Steam's app IDs to be downloaded. Each one given as integer and separated by spaces.")

parser.add_argument('-type', type=str, default='all', required=False, metavar='T',
                    help="Type of reviews to be retrieved. Expects: 'positive', 'negative' or 'all'. Default: 'all'.")
parser.add_argument('-max', type=int, default=None, required=False, metavar='M',
                    help="Maximum number of reviews to be harvested - integer. Default: retrieve as much as possible.")
parser.add_argument('-output_folder', type=str, required=True, metavar='O',
                    help="Mandatory. Path of the output folder where .csv files will be written.")
args = parser.parse_args()

# reading arguments
review_type = args.type
max_reviews = args.max
output_folder_path = args.output_folder
app_ids = args.app_ids

# post-processing: date constrain (self explain)
timesamp_min = None
timesamp_max = None

# post-processing: language
language = 'english'

# ## CONS ############################################################################################################ #

REVIEW_URL_FRAME = "https://store.steampowered.com/appreviews/%d?json=1&review_type=%s&num_per_page=%d&start_offset=%d"
REVIEW_URL_FRAME = "{0}{1}".format(REVIEW_URL_FRAME, "&day_range=9223372036854775807")  # tweak to get all data
OFFSET_SIZE = 100


# ## DEFS ############################################################################################################ #

def pass_filter(review):
    """
    Checks if a review passes all post-processing constraints
    :param review: Review object
    :return: True if the review passes the filter, False otherwise
    """
    if (language is not None) and (language != review['language']):
        return False
    if (timesamp_min is not None) and (timesamp_min > review['timestamp_updated']):
        return False
    if (timesamp_max is not None) and (timesamp_max < review['timestamp_updated']):
        return False
    return True


def retrieve_review_data_batch(app_id, step):
    """
    Perform a single call to Steam Store API.
    :param app_id: Integer. Steam App id.
    :param step: Integer. Associated to the start offset. Should have values of 0, 1, 2, ...
    :return: A list of review objects if any element was retrieved. None otherwise.
    """
    st_offs = step * OFFSET_SIZE
    url_address = REVIEW_URL_FRAME % (app_id, review_type, OFFSET_SIZE, st_offs)
    all_entries = requests.get(url_address).json()
    try:
        all_entries = [e for e in all_entries['reviews'] if pass_filter(e)]
        return all_entries if len(all_entries) > 0 else None
    except KeyError:
        print("Unable to retrieve reviews for app %d." % app_id)
        return None


def clean_repeated_reviews(all_data):
    """
    Remove repeated objects from the list
    :param all_data: List of review objects.
    :return: List of unique review objects (by recommendationid)
    """
    return list(dict((dt['recommendationid'], dt) for dt in all_data).values())


def retrieve_review_data(app_id):
    """
    Retrieve all reviews for a given app given the constraints defined globally.
    :param app_id: Integer. Steam app id.
    :return: A list of review objects.
    """

    # vanilla loop to get the data
    print("Getting reviews for app %d..." % app_id)
    all_data, data_batch, step, repeated = [], retrieve_review_data_batch(app_id, 0), 0, 0
    while data_batch is not None:
        print("  at step %d, adding %d to %d." % (step, len(data_batch), len(all_data)))
        all_data += data_batch
        step += 1
        old_size = len(all_data)
        all_data = clean_repeated_reviews(all_data)
        repeated += old_size - len(all_data)
        if (max_reviews is not None) and (len(all_data) > max_reviews):
            print(" Reached the maximum number of reviews.")
            break
        elif repeated >= len(all_data):
            print(" Found %d repeated reviews." % repeated)
            break
        data_batch = retrieve_review_data_batch(app_id, step)

    #
    all_data = all_data if (max_reviews is not None) and len(all_data) < max_reviews else all_data[0:max_reviews]
    print("Got %d reviews for app %d." % (len(all_data), app_id))
    return all_data


def write_review_csv(app_id, all_reviews):
    """
    Write retrieved reviews into a CSV file - if at least one review is given
    :param app_id: Integer. App id.
    :param all_reviews: List of reviews.
    :return: Boolean. True if file was written, False otherwise
    """

    # write the output file if more than one entry was retrieved
    if len(all_reviews) <= 0:
        print("No reviews retrieved for app %d, no file writen." % app_id)
        return False
    out_file_path = os.path.join(output_folder_path, "%d.csv" % app_id)
    with open(out_file_path, 'w', newline='', encoding="utf-8") as w_file:
        csv_w = csv.writer(w_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csv_w.writerow(('recommendationid', 'timestamp_created', 'timestamp_updated', 'playtime_forever',
                        'steam_purchase', 'received_for_free', 'voted_up', 'written_during_early_access', 'review'))
        wr = lambda dt: csv_w.writerow((dt['recommendationid'], dt['timestamp_created'], dt['timestamp_updated'],
                                        dt['author']['playtime_forever'], dt['steam_purchase'],
                                        dt['received_for_free'], dt['voted_up'], dt['written_during_early_access'],
                                        dt['review'].replace('\n', ' ')))
        deque(map(wr, all_reviews))
    print("Wrote %d reviews at: %s" % (len(all_reviews), out_file_path))
    return True


def main():
    """
    C-style main function.
    :return: None.
    """

    if not (os.path.isdir(output_folder_path) or os.access(output_folder_path, os.W_OK)):
        sys.exit('Output folder does not exist or is not writable. Existing.')

    harvest_reviews = lambda app_id: write_review_csv(app_id, retrieve_review_data(app_id))
    deque(map(harvest_reviews, app_ids))


# ## CALL ############################################################################################################ #

if __name__ == '__main__':
    main()
