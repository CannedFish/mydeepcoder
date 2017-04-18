# -*- coding: utf-8 -*-
# NOTE: need python 3.5 and tenflow 1.01

import tensorflow as tf

# nn's paramters
type_length = 2
array_length = 20 # NOTE: L in paper
embedding_width = 20 # NOTE: E in paper
hidden_width_1 = 2*(type_length+embedding_width)
hidden_width_2 = 256
output_width = 34

# training parameters
learning_rate = 0.01
training_epochs = 20
batch_size = 256
display_step = 1
examples_to_show = 10

X = tf.placeholder('float', [None, input_width])

weights = {
    'encoder_embedding': tf.Variable(tf.random_normal(array_length, embedding_width)),
    'encoder_h1': tf.Variable(tf.random_normal(hidden_width_1, hidden_width_2)),
    'encoder_h2': tf.Variable(tf.random_normal(hidden_width_2, hidden_width_2)),
    'encoder_h3': tf.Variable(tf.random_normal(hidden_width_2, hidden_width_2))
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b2': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b3': tf.Variable(tf.random_normal([hidden_width_2]))
}

def encoder(input_type, input_array, output_type, output_array):
    # TODO: embedding
    # embed_input = 1
    # embed_output = 2
    # layer_1 = concatenate input_type, embed_input, output_type, embed_output
    layer_2 = tf.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h1']), \
            biases['encoder_b1']))
    layer_3 = tf.sigmoid(tf.add(tf.matmul(layer_2, weights['encoder_h2']), \
            biases['encoder_b2']))
    layer_4 = tf.sigmoid(tf.add(tf.matmul(layer_3, weights['encoder_h3']), \
            biases['encoder_b3']))
    return layer_3

def decoder(x):
    pass

