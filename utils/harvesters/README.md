# Harvesting scripts

4 plain Python scripts were developed for harvesting the data needed for this project. Each of them are described in the expected use sequence as follows.

## harvest_apps.py

This script has the sole purpose of retrieving the basic information of EVERY app currently available in the Valve's STEAM database.

As there is an endpoint in our source API that already returns the whole data in a single request, the execution of this script is expected to not be time consuming.

**Source:** Valve's Steam API

**Input:** None

**Output:** A .json file with a list of the ID and Title of each app in Steam.

## app_selector.py

This script has the sole purpose of identifying the Steam apps that fit an specific criteria.

As the endpoint in the API used only returns the necessary information for one app at a time, the procedure followed by this script is to sequentially process every existing app and checking it against the required criteria are met. This way, it is expected that the execution of this script takes a considerable amount of time (mainly determined by the *max* argument).

**Source:** Valve's Steam Store API

**Inputs:**

- A .json file with a list of all Steam apps available (as the output of the *harvest_apps.py* script);

- *Genre* of interest (filter-in). Example: 'Indie';

- *Type* of interest (filter-in). Example: 'game';

- *Tags* to avoid (filter-out). Example: 'Nudity';

- Maximum (*Max*) number of apps to be retrieved.

**Output:** A .json file with a detailed list of all apps that matched the specified criteria.

## harvest_reviews.py

This script has the sole purpose of retrieving the public reviews associated to an Steam app. It is expected to be executed by a batch call that iterates over a set of Steam API IDs (as the output of *harvest_apps.py* or *app_selector.py*).

**Source:** Valve's Steam Store API

**Inputs:**

- *App ID* of the game to be harvested. Example: 221380 ;

- *Type* of reviews to be harvested. Expected 'positive', 'negative' or 'all' ;

- Maximum (*Max*) number reviews to be harvested.

**Output:** A .csv file containing all the reviews harvested.

## harvest_concurrentplayers.py

This script has the sole purpose of retrieving the complete daily timeseries of concurrent players.

**Source:** SteamDB API

**Input:** A .json file with a list of all Steam apps available (as the output of the *harvest_apps.py* script)

**Outputs:** A .json file with the complete timeseries of concurrent players of each app in the input argument.

## preprocess_count_reviews.py

This script has the sole purpose of counting the reviews retrieved each day for each app and synthesise into a series of timeseries.

**Input:** A folder full of .json files with reviews from apps (as the output of the *harvest_concurrentplayers.py* script)

**Outputs:** A .json file with the timeseries of total daily review counts, separated by app Id.
