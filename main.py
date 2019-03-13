import numpy as np 
import pandas as pd

import os, time, argparse

import tensorflow as tf 
from tf.keras.models import Model 
from tf.keras.layers import Input, BatchNormalization, Embedding, Reshape, dot
from tf.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, Tensorboard
from tf.keras.optimizers import SGD, RMSprop, Adam
from tf.keras.experimental import export_saved_model, load_from_saved_model
from tf.keras.initializers import RandomNormal
from tf.keras.utils import plot_model

from utils import utils
from utils import constants

class Word2Vec_Classifier(tf.keras.Model):
	
	model_architecture_name = constants.model_architecture_name
	model_weights_directory = constants.model_weights_directory

	def __init__(self, output_directory, vocab_size, input_target, input_context, vector_dim, verbose=False, load_init_weights=False):
		super(Word2Vec_Classifier, self).__init__(name='Word2Vec_Classifier')
		
		if not os.path.exists(model_weights_directory):
			os.makedirs(model_weights_directory)
		else:
			self.output_directory = output_directory

		if load_init_weights == True:
			self.model.load_from_saved_model(os.path.join(model_weights_directory, 'model_init.hdf5'))
		else:
			self.export_saved_model(os.path.join(self.output_directory, 'model_init.hdf5'))

		self.vocab_size = vocab_size
		self.input_target = input_target
		self.input_context = input_context
		self.vector_dim = vector_dim

		if verbose == True:
			self.model.summary()
		self.verbose = verbose

	def call(self, inputs, training=False):
		target = self.Embedding(self.vocab_size, self.vector_dim, input_length=1, name='embedding', 
			embeddings_initializer=self.RandomNormal(mean=0.0, stddev=1, seed=123), embeddings_regularizer=None, activity_regularizer=None, 
			embeddings_constraint=None, mask_zero=False, input_length=None)(self.input_target)
		target = self.Reshape((vector_dim, 1))(target)
		context = self.Embedding(self.vocab_size, self.vector_dim, input_length=1, name='embedding', 
			embeddings_initializer=self.RandomNormal(mean=0.0, stddev=1, seed=123), embeddings_regularizer=None, activity_regularizer=None, 
			embeddings_constraint=None, mask_zero=False, input_length=None)(self.input_context)
		context = self.Reshape((vector_dim, 1))(context)
		similarity = dot(inputs=[target, context], normalize=True, axes=0)

		# now perform the dot product operation to get a similarity measure
		dot_product = dot([target, context], axes=0, normalize=False)
		dot_product = Reshape((1,))(dot_product)

		# add the sigmoid output layer
		output_layer = Dense(1, activation='sigmoid')(dot_product)

		return self.built_model(self.input_layer, self.output_layer)

	# Model Callbacks
	modelcheckpoint_callback = ModelCheckpoint(
		filepath=,
		monitor='val_loss',
		verbose=0,
		save_best_only=False,
		save_weights_only=False,
		mode='min',
		period=1)

	reducelronplateau_callback = ReduceLROnPlateau(
		monitor='val_loss',
		patience=5, 
		min_lr=1e-5)

	log_dir = '{}/model_logs'.format(self.directory)
	# in CLI, use this to open up tensorboard:
	# tensorboard --log_dir=/full/path/to/logs

	tb_callback = Tensorboard(log_dir=log_dir)

	callbacks = [modelcheckpoint_callback, reducelronplateau_callback, tb_callback]

	def save_weights(self, saved_model_path):
		export_saved_model(model, saved_model_path)

	def load_weights(self, save_model_path):
		load_from_saved_model(saved_model_path)

	@staticmethod
	def write_out_model_architecture_diagram():
		plot_model(self.model, to_file=os.path.join(os.path.abspath(__file__), 'model_architecture_diagrams','model.png'))

# Creating and fitting the model
word_target, word_context, couples, labels = skipgrammify_data(data, constants.vocab_size, constants.window_size)
model = Word2Vec_Classifier().fit()
model.compile(run_eagerly=True)

# embedding layer constants
input_target = ((1,))
input_context = ((1,))
vocab_size = 10000 # number of rows or size of our dictionary 
vector_dim = 300 # size of our embedding vector weights
input_length = 1 # this matches your input target size
name = "embedding" # goes into the name scope for when we use tensorboard


# Parse Arguments
parser = argparse.ArgumentParser(description="Specify the hyperparameters and configuration of the model")
parser.add_argument("-msp",
	"--model_save_path", 
	help="provide the full path for where you want to save the model",
	type=str,
	metavar="",
	default=model_weights_directory)
parser.add_argument("-lw",
	"--load_weights",
	help="if you have previous model weights, provide the full path to where the model weights are located",
	type=str,
	metavar="",
	default="./model_weights")
parser.add_argument("-sw", 
	"--save_weights",
	help="provide the full path to where to want to save the model weights",
	type=str,
	metavar="",
	default="./model_weights")
parser.add_argument("-lr", 
	"--learning_rate"
	help="changes the learning rate", 
	type=float,
	metavar="",
	default=0.0001)
parser.add_argument("-b", 
	"--batch_size",
	help="changes the batch size. it is useful to pick a batch size that is a base of 2.",
	type=int,
	metavar="",
	default=64)
parser.add_argument("-e",
	"--epochs",
	help="specify the number of epochs to train on. because of the nature of the problem, 1M is typically required to trian from scatch",
	type=int,
	metavar="",
	default=1e6)
parser.add_argument("-o",
	"--optimizer",
	help="select optimizer",
	type=str,
	metavar="",
	default='adam')
parser.add_argument("-l",
	"--loss_function",
	type=str,
	metavar="",
	default="mse")
parser.add_argument("-m",
	"--metric",
	help="metric to use",
	type=str,
	metavar="",
	default='val_loss')
group = parser.add_mutually_exclusive_group()
group.add_argument("-v",
	"--verbose",
	action="store_true",
	help="print verbose")
group.add_argument("-q",
	"--quiet",
	action="store_true",
	help="print quiet")
args = parser.parse_args()


if __name__== "__main__":
	model = Word2Vec_Classifier(epochs=args.epochs, batch_size=args.batch_size)
	model.compile(optimizer=args.optimizer, loss=args.loss_function, metric=args.metric)
	# self.model_save_path = args.model_save_path
	print("The model has been run and completed. The model HDF5 file is saved here: {}".format(args.model_save_path))
	print("\nThe model's performance is as follows: Accuracy: {}, Val Accuracy: {}, Loss: {}, Val Loss: {}".format(history.))