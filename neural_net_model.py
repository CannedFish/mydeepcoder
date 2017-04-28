# -*- coding: utf-8 -*-
# NOTE: need python 3.5 and tenflow 1.01

import tensorflow as tf
import numpy as np
import pickle

# nn's paramters
sample_num = 5 # number of input-output samples for each program
type_length = 2 # length of one-hot vector for input-output type
array_length = 20 # NOTE: L in paper
embedding_index = 513 # NOTE: [-256, 255] + None
embedding_width = 20 # NOTE: E in paper
hidden_width_1 = 2*(type_length+array_length*embedding_width)
hidden_width_2 = 256 # NOTE: K in paper
output_width = 34 # NOTE: C in paper

# training parameters
learning_rate = 0.01
training_epochs = 20
batch_size = 256
display_step = 1
examples_to_show = 10

weights = {
    # 'encoder_embedding': tf.Variable(tf.random_normal([array_length, embedding_width])),
    'encoder_h1': tf.Variable(tf.random_normal([hidden_width_1, hidden_width_2])),
    'encoder_h2': tf.Variable(tf.random_normal([hidden_width_2, hidden_width_2])),
    'encoder_h3': tf.Variable(tf.random_normal([hidden_width_2, hidden_width_2])),
    'decoder': tf.Variable(tf.random_normal([hidden_width_2, output_width]))
}

biases = {
    'encoder_b1': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b2': tf.Variable(tf.random_normal([hidden_width_2])),
    'encoder_b3': tf.Variable(tf.random_normal([hidden_width_2])),
    'decoder': tf.Variable(tf.random_normal([output_width]))
}

def _prev_process(input_type, input_array, output_type, output_array):
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
        return np.array(ret)

    i_type = type_to_one_hot(input_type)
    input_data = to_array(input_array, array_length)
    inputs = tf.reshape(tf.nn.embedding_lookup(embedding, input_data), \
            [input_array*array_length])

    o_type = type_to_one_hot(output_type)
    output_data = to_array(output_array, array_length)
    outputs = tf.reshape(tf.nn.embedding_lookup(embedding, output_data), \
            [input_array*array_length])

    return np.concatenate([i_type, inputs, o_type, outputs])

def prev_process(samples):
    """
    :param samples: 3-D python array, [batch_size, sample_num, hidden_width_1]
    :return: 3-D Tensor, [batch_size, sample_num, hidden_width_1]
    """
    input_mat = np.array([[_prev_process(*s) for s in ss] for ss in samples])
    return tf.reshape(input_mat, [batch_size, sample_num, hidden_width_1])

def __encoder(x):
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

def _encoder(x):
    """
    :param x: 2-D tensor, shape is [sample_num, hidden_width_1]
    :return: 1-D tensor, shape is [hidden_width_2]
    """
    layer_5 = tf.map_fn(__encoder, x)
    return tf.reduce_mean(layer_5, 0)

def encoder(x):
    """
    :param x: 3-D tensor, shape is [batch_size, sample_num, hidden_width_1]
    :return: 2-D tensor, shape is [batch_size, hidden_width_2]
    """
    return tf.map_fn(_encoder, x)

def _decoder(x):
    return tf.sigmoid(tf.add(tf.matmul(x, weights['decoder']), \
            biases['decoder']))

def decoder(x):
    """
    :param x: 2-D tensor, shape is [batch_size, hidden_width_2]
    :return: 2-D tensor, shape is [batch_size, output_width]
    """
    return tf.map_fn(_decoder, x)

def input_samples(input_file):
    """A generator
    :return: [batch_size, 5, 4], [batch_size]
    """
    samples = {'x':[], 'y':[]}
    with open(input_file, 'r') as fd:
        sample = pickle.loads(fd.readline())
        samples['y'].append(sample[1])
        samples['x'].append(sample[2])
        samples.append(pickle.loads(fd.readline()))
        if len(samples) == batch_size:
            yield samples['x'], samples['y']
            samples = {x:[], y:[]}

    yield samples['x'], samples['y']

X = tf.placeholder("float32", [batch_size, sample_num, hidden_width_1])
Y = tf.placeholder("float32", [batch_size, output_type])

def main(input_file):
    # construct computing flow
    encoder_op = encoder(X)
    decoder_op = decoder(encoder_op)
    
    y_pred = decoder_op
    y_true = Y
    loss = tf.reduce_mean(-y_true * tf.log(y_pred) - (1-y_true) * tf.log(1-y_pred))
    optimizer = tf.train.RMSPropOptimizer(learning_rate).minimize(loss)

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)

        # train
        for epoch in range(training_epochs):
            for batch_x, batch_y in input_samples(input_file):
                _, c = sess.run([optimizer, loss], feed_dict={\
                        X: prev_process(batch_x), \
                        Y: batch_y})
            if epoch % display_step == 0:
                print("Epoch:", "%04d" % (epoch+1), "cost=", "%.9f" % c)

        print("Optimization Finished!")

        # TODO: Test

