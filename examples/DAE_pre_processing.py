#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:40:52 2017

@author: Jean Zagdoun
"""

try:
    import tensorflow as tf
except ImportError:
    print 'Need to install the "tensorflow" module (available on Linux and MacOS only for python 2.7) : "pip install tensorflow" or with Anaconda "conda install tensorflow"'
    exit()

import sys
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods')

from utils.DAE import DAE

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True) 

learning_rate=0.01
log_path = '/tmp/y101'

x = tf.placeholder(tf.float32,[None,784])
Y = tf.placeholder(tf.float32,[None,10])



data = mnist.train.next_batch(50000)[0]
W1, B1 = DAE(data,[400,102,10])



Weights1, Biases1 = W1.copy(), B1.copy()

#it is important you get the session of DAE.py 
sess=tf.get_default_session()

#tensorboard
tf.summary.histogram('RN1_W1',Weights1['W1'])
tf.summary.histogram('RN1_W2',Weights1['W2'])
tf.summary.histogram('RN1_W2',Weights1['W3'])


tf.summary.histogram('RN1_B1',Biases1['B1'])
tf.summary.histogram('RN1_B2',Biases1['B2'])
tf.summary.histogram('RN1_B2',Biases1['B2'])


def RN1(x):
    L1 = tf.sigmoid(tf.add(tf.matmul(x,Weights1['W1']),Biases1['B1']))
    L2 = tf.sigmoid(tf.add(tf.matmul(L1,Weights1['W2']),Biases1['B2']))
    l3 = tf.sigmoid(tf.add(tf.matmul(L2,Weights1['W3']),Biases1['B3']))
    return l3



loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y,logits=RN1(x)))
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)
correct_prediction = tf.equal(tf.argmax(Y,1), tf.argmax(RN1(x),1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

tf.summary.scalar('perte',loss)
tf.summary.scalar('accuracy',accuracy)


merge_op = tf.summary.merge_all()
writer = tf.summary.FileWriter(log_path)
writer.add_graph(sess.graph)

init = tf.global_variables_initializer()
sess.run(init)


W_aux = Weights1['W1'].eval()
print("\nstarting trainging")
for i in range(1000):
  batch = mnist.train.next_batch(100)
  _,s = sess.run([optimizer,merge_op ],feed_dict={x: batch[0], Y: batch[1]})
  writer.add_summary(s,i)
test = mnist.test.next_batch(10000)
acc = sess.run(accuracy, feed_dict={x: test[0], Y: test[1]})

print("your accuracy on the testing set is : " + str(acc))