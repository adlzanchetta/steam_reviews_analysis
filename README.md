## Authors 
Andre Zanchetta (https://github.com/adlzanchetta/steam_reviews_analysis)

Dennis Nguyen-Do (https://github.com/SJHH-Nguyen-D/steam_reviews_analysis)

Tiger Liu (https://github.com/uilregit/steam_reviews_analysis)


# Using Sentiment Analysis using Steam Game Reviews

This is a machine-learning based culminating group project for our Neural Network/Deep Learning Course (SEP 788-C01, SEP 789-C02) at McMaster University. The goal of this project is to use text analysis techniques on a corpus of Steam game reviews to predict the maximum concurrent number of players, given a sliding window. The model architecture and technique that we primarily employ is the Word2Vec model with word embeddings using skip-gram. We performed our modeling and evalutation using rented compute nodes on Amazon's EC2 cloud computing platform for faster model training and inference.

The model architecture diagram can be seen below: (subject to change)


![Architecture of Word2Vec](https://github.com/adlzanchetta/steam_reviews_analysis/word2vec_skipgram_architecture.png)



## Data

Our data for this project is collected using Steam's API and using a data harvester script of parse, read and do some initial pre-processing of player reviews, given a look-up table for Steam app IDs, Steam app tags and genres. The steam game reviews, which were identified by Steam IDs that were 'legal', 'games' and 'indie', were read, processed, loaded and written out as individual comma-separated-value files (CSV). Each .csv file represented X many reviews for a particular game during a period of Y intervals. A total of 773 steam game review .csv files were saved onto disk and loaded into our project AWS S3 bucket.

The link to the AWS S3 bucket containing the steam game review data for our project is listed below, however it requires a canonical AWS ID for authenticated access:
* [Project AWS S3 Steam Review Bucket](https://s3.console.aws.amazon.com/s3/buckets/steamreviewbucket/reviews/?region=us-east-1)


## Code
The code for our project is partitioned into the following segments:

* The [utils](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/) folder contains the necessary functions to read the datasets and visualize the plots, as well as the constants, abstracted from the main file for a cleaner script. 
* The [utils.py](https://github.com/adlzanchetta/steam_reviews_analysis/master/utils/utils.py) file inside folder of that namesake that contains the necessary functions to read the datasets and visualize the plots.
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