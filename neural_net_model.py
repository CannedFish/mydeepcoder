# -*- coding: utf-8 -*-
# NOTE: need python 3.5 and tenflow 1.01

import tensorflow as tf
import numpy as np

# nn's paramters
type_length = 2
array_length = 20 # NOTE: L in paper
embedding_index = 513 # NOTE: [-256, 255] + None
embedding_width = 20 # NOTE: E in paper
hidden_width_1 = 2*(type_length+array_length*embedding_width)
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
    # 'encoder_embedding': tf.Variable(tf.random_normal([array_length, embedding_width])),
    'encoder_h1': tf.Variable(tf.random_normal([hidden_width_1, hidden_width_2])),
    'encoder_h2': tf.Variable(tf.random_normal([hidden_width_2, hidden_width_2])),
    'encoder_h3': tf.Variable(tf.random_normal([hidden_width_2, hidden_width_2]))
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b2': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b3': tf.Variable(tf.random_normal([hidden_width_2]))
}

def prev_process(input_type, input_array, output_type, output_array):
    """
    :param input_type: integer value, 0 --> int, 1 --> [int]
    :param input_array: integer or list based on input_type
    :param output_type: same as input_type
    :param output_array: same as output_array
    :return: a vector concated by input_type, input_array, output_type, output_array
    """
    # TODO: train an embedding layer
    embedding = tf.Variable(tf.random_normal([embedding_index, embedding_width]))

    def to_array(v, length=20):
        if type(v) == int:
            v = [v]
        if type(v) != list:
            raise TypeError('Must be a list, %s is given' % type(v))
        if len(v) > array_length:
            raise TypeError('Must be shorter than %d, %d is given' \
                    % (array_length, len(v)))
        ret = [0] * (array_length - len(v))
        # 0 is Null's index, so we need add 257 to map -256 to 1
        ret.extend(v, map(lambda x: x+257, v))
        return np.array(ret)

    def type_to_one_hot(t):
        """
        :return: vector, [int, [int]], e.g. [1.0, 0.0] means an int
        """
        if type(t) != int:
            raise TypeError('Must be an int, %s is given' % type(v))
        ret = [.0] * type_length
        ret[t] = 1.
        return ret

    i_type = type_to_one_hot(input_type)
    input_data = to_array(input_array, array_length)
    inputs = tf.reshape(tf.nn.embedding_lookup(embedding, input_data), \
            [input_array*array_length])

    o_type = type_to_one_hot(output_type)
    output_data = to_array(output_array, array_length)
    outputs = tf.reshape(tf.nn.embedding_lookup(embedding, output_data), \
            [input_array*array_length])

    return np.concatenate([i_type, inputs, o_type, outputs])

def encoder(x):
    """
    :param x: vector, with hidden_width_2 dimension
    :return: vector, with hidden_width_2 dimension
    """
    layer_2 = tf.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']), \
            biases['encoder_b1']))
    layer_3 = tf.sigmoid(tf.add(tf.matmul(layer_2, weights['encoder_h2']), \
            biases['encoder_b2']))
    layer_4 = tf.sigmoid(tf.add(tf.matmul(layer_3, weights['encoder_h3']), \
            biases['encoder_b3']))
    return layer_4

def post_process(x):
    """
    :param x: 2-D tensor, shape is [number_of_samples, dim_of_encoder_output]
    :return: vector, with hidden_width_2 dimension
    """
    return tf.reduce_mean(x, 0)

def decoder(x):
    pass

