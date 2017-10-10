#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:40:52 2017

@author: Jean Zagdoun
"""
import sys
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods')

import numpy as np
try:
    import tensorflow as tf
except ImportError:
    print 'Need to install the "tensorflow" module (available on Linux and MacOS only for python 2.7) : "pip install tensorflow" or with Anaconda "conda install tensorflow"'
    exit()

tf.reset_default_graph()

import matplotlib.pyplot as plt

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)

examples_to_show = 10
from utils.DAE import DAE



data = mnist.train.next_batch(50000)[0]
P , M, S, T = DAE(data, [225,121], batch_size=500, pre_pross=False, decoder=True)

#you want to recover the session from DAE to be able to use the weights and train them if you want to
sess = tf.get_default_session()




""" 
    every line of code bellow this is to print the result of denoising autoencoder
    You can check the exactutude of the method by seeing a cost decreasing in each optimization step
    But DAE allows to check visually how close you were to the solution
    the plot between input and reconstructed output is what your compressed image looks like
    I left it for the curiosity of the user
    
"""

E_W = P['W1'].eval()
E_B = M['B1'].eval()    

D_W = S['W1'].eval()
D_B = T['B1'].eval()   

data = mnist.test.images

E1 = tf.nn.sigmoid(tf.add(tf.matmul(data,E_W),E_B)).eval(session=sess)
D1 = tf.nn.sigmoid(tf.add(tf.matmul(E1,D_W),D_B)).eval(session=sess)
# Compare original images with their reconstructions
f, a = plt.subplots(3, 10, figsize=(10, 3))
for i in range(10):
    a[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
    a[1][i].imshow(np.reshape(E1[i], (15, 15)))
    a[2][i].imshow(np.reshape(D1[i], (28, 28)))

f.show()
plt.draw()



E_W = P['W2'].eval()
E_B = M['B2'].eval()    

D2_W = S['W2'].eval()
D2_B = T['B2'].eval()   

E2 = tf.nn.sigmoid(tf.add(tf.matmul(E1,E_W),E_B)).eval(session=sess)
D2 = tf.nn.sigmoid(tf.add(tf.matmul(E2,D2_W),D2_B)).eval(session=sess)
D3 = tf.nn.sigmoid(tf.add(tf.matmul(D2,D_W),D_B)).eval(session=sess)

f, a = plt.subplots(5, 10, figsize=(10,5))
for i in range(10):
    a[0][i].imshow(np.reshape(mnist.test.images[i], (28, 28)))
    a[1][i].imshow(np.reshape(E1[i], (15, 15)))
    a[2][i].imshow(np.reshape(E2[i], (11, 11)))
    a[3][i].imshow(np.reshape(D2[i], (15,15)))
    a[4][i].imshow(np.reshape(D3[i], (28, 28)))
f.show()
plt.draw()

raw_input("Push ENTER key to exit.")
    
