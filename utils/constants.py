import numpy as np

# Harvestor Constants
harvest_reviews_script_file_path = "E:\\GoogleDrive\\2019_01a_NeuralNetworks\\chemeng788_project\\harvesting_script\\harvest_reviews.py"
games_reviews_json_file_path = "E:\\GoogleDrive\\2019_01a_NeuralNetworks\\chemeng788_project\\harvested_data\\Indies_pure_1100.json"
game_reviews_data_output_directory = os.path.join(os.path.abspath(__file__), "out_data", "indies")

# Word2Vec Model Constants
window_size = 3 # window size for number of candidate context words proximal to the target word
vector_dim = 300 # 
epochs = 1e6 # number of 
valid_size = 16     # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
model_architecture_name = 'Word2Vec'
model_weights_directory = os.path.join(os.path.abspath(__file__), 'model_weights')