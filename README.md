## Authors 

Andre Zanchetta (https://github.com/adlzanchetta/steam_reviews_analysis)
Dennis Nguyen-Do (https://github.com/SJHH-Nguyen-D/steam_reviews_analysis)
Tiger Liu (https://github.com/uilregit/steam_reviews_analysis)


# Using Sentiment Analysis using Steam Game Reviews

This is a machine-learning based culminating group project for our Neural Network/Deep Learning Course (SEP 788-C01, SEP 789-C02) at McMaster University. The goal of this project is to use text analysis techniques on a corpus of Steam game reviews to predict the maximum concurrent number of players, given a sliding window. The model architecture and technique that we primarily employ is the Word2Vec model with word embeddings using skip-gram. We performed our modeling and evalutation using rented compute nodes on Amazon's EC2 cloud computing platform for faster model training and inference.

The model architecture diagram can be seen below: (subject to change)


![Architecture of Word2Vec](https://github.com/adlzanchetta/steam_reviews_analysis/word2vec_skipgram_architecture.png)


## Dataset

### Data description

Each game in the Valve's Steam's Catalog is an Steam App of type 'game'. Each Steam App has a set of attributes, among which:

- ID: unique numeric identifier of the app;

- Title: public name title of the game;

- Genres: list of genres associated to the game ('Action', 'Strategy', etc.);

- Tags: list of tags associated to the game ('Violence', 'Educational', 'History rich', etc.)

- Concurrent maximum daily players history: a timeseries of concurrent players observed;

In addition, each game is associated to a set of reviews that were submitted by the players. Each review has a set of attributes, among which:

- ID: unique numeric identifier of the review;

- Type: boolean review of the type 'thumbs up'/'thumbs down';

- Review text: open text field in which the user freely describes its opinion.

### Collected data

Our data for this project was collected from different sources directly or indirectly associated with Steam's database, as described [the following section](##Harvesting-scripts). A total number of 773 games of the 'Indie' genre and not tagged with 'nudity' or 'sexual content' were explored. All public reviews submitted to each of those games were retrieved, totallizing **TODO** review entries. All of those data was uploaded into our project AWS S3 bucket.

The link to the AWS S3 bucket containing the steam game review data for our project is listed below, however it requires a canonical AWS ID for authenticated access:
* [Project AWS S3 Steam Review Bucket](https://s3.console.aws.amazon.com/s3/buckets/steamreviewbucket/reviews/?region=us-east-1)

### Harvesting scripts

4 plain Python scripts were developed for harvesting the data needed for this project. Each of them are described in the expected use sequence as follows.

#### harvest_apps.py

This script has the sole purpose of retrieving the basic information of EVERY app currently available in the Valve's STEAM database.

As there is an endpoint in our source API that already returns the whole data in a single request, the execution of this script is expected to not be time consumming.

**Source:** Valve's Steam API

**Input:** None

**Output:** A .json file with a list of the ID and Title of each app in Steam.

#### app_selector.py

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

#### harvest_reviews.py

This script has the sole purpose of retrieving the public reviews associated to an Steam app. It is expected to be executed by a batch call that iterates over a set of Steam API IDs (as the output of *harvest_apps.py* or *app_selector.py*).

**Source:** Valve's Steam Store API

**Inputs:**

- *App ID* of the game to be harvested. Example: 221380 ;

- *Type* of reviews to be harvested. Expected 'positive', 'negative' or 'all' ;

- Maximum (*Max*) number reviews to be harvested.

**Output:** A .csv file containing all the reviews harvested.

#### harvest_concurrentplayers.py

This script has the sole purpose of retrieving the complete daily timeseries of concurrent players.

**Source:** SteamDB API

**Input:** A .json file with a list of all Steam apps available (as the output of the *harvest_apps.py* script)

**Outputs:** A .json file with the complete timeseries of concurrent players of each app in the input argument.


## Code
The code for our project is partitioned into the following segments:

* The [utils](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/) folder contains the necessary functions to read the datasets and visualize the plots, as well as the constants, abstracted from the main file for a cleaner script.
* The [utils.py](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/utils.py) file inside folder of that namesake that contains the necessary functions to read the datasets and visualize the plots.
* The [harvesters](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/harvesters/) This directory contains the scripts that were required to request, pull and parse Steam game reviews from the Steam API and parse them into loadable formats for our analysis and modeling. The individual functions of the scripts are explained above.
* The [constants.py](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/constants.py) file inside folder of that namesake that contains the necessary functions to read the datasets and visualize the plots.
* The [main.py](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/main.py) This contains the main file for running our model. We use argparse to pass in the model hyperparameters and saving/loading options.

## Prerequisites
All python packages needed are listed in utils/requirements.txt file and can be installed simply using the pip command for python3.6.

* [numpy](http://www.numpy.org/)  
* [pandas](https://pandas.pydata.org/)  
* [sklearn](http://scikit-learn.org/stable/)  
* [matplotlib](https://matplotlib.org/)  
* [tensorflow-gpu](https://www.tensorflow.org/)  
* [keras](https://keras.io/)


## Docker Instructions

To run this project as a Docker image, in the terminal, use these instructions to build the Dockerfile and run it. So long as you are in the same director, Docker will know which file is the dockerfile and run it, without you having to specify which file is the Dockerfile:
```bash
docker build -t steamreviewprojectcontainer .
```
To run this command below to run the container (assuming group_project_final directory is cloned into ~/steam_reviews_analysis in the terminal:
```bash
docker run --runtime=nvidia \
-it \
-v  ~/steam_reviews_analysis:/tmp \
-w /tmp \
--rm steamreviewprojectcontainer:latest \
bash
```
This command lists all the containers that are running at the moment:
```bash
sudo docker ps -a
```
This command also lists all the containers that are running at the moment:
```bash
sudo docker container ls
```
If you haven't used the --rum option at run to remove the container upon termination of the program, you can remove the running container with this command:
```bash
sudo docker -rm <container_id>
```
This command lists all the images that are saved by Docker:
```bash
sudo docker image ls
```
This command removes the docker image:
```bash
sudo docker rmi -f <docker_image_id>
```