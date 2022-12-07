# ========================================= CITATIONS ============================================================================================ #
# from https://www.youtube.com/watch?v=pauPCy_s0Ok                                                                                                 #
# from https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-from-scratch-for-mnist-handwritten-digit-classification/   #
# ================================================================================================================================================ # 

import sys, os
def runPipCommand(pipCommand, pipPackage=None):
    # first upgrade pip:
    command = f"'{sys.executable}' -m pip -q install --upgrade pip"
    os.system(command)
    # input the package from the user if it's not supplied in the call:
    if pipPackage == None:
        pipPackage = input(f'Enter the pip package for {pipCommand} --> ')
    # then run pip command:
    command = f"'{sys.executable}' -m pip {pipCommand} {pipPackage}"
    os.system(command)

runPipCommand('install', 'numpy')
runPipCommand('install', 'keras')
runPipCommand('install', 'pickle')

import numpy as np
from keras.datasets import mnist
from keras.utils import np_utils
import pickle

from dense import Dense
from activations import Tanh
from losses import mse, msePrime

def preprocessData(x, y):
    # reshape and normalize input data
    x = x.reshape(x.shape[0], 28 * 28, 1)
    x = x.astype("float32") / 255
    # encode output which is a number in range [0,9] into a vector of size 10
    y = np_utils.to_categorical(y)
    y = y.reshape(y.shape[0], 10, 1)
    return x, y

def train(model, trainX, trainY, epoch=500, trainingRate=0.01):
    for e in range(epoch):
        print(f'=============== EPOCH: {e} ==================')
        error = 0
        for x, y in zip(trainX, trainY):
            # Forward through the model
            output = x
            for layer in model:
                output = layer.forward(output)

            # Add Error
            error += mse(y, output)

            # Calculate gradient and backwards propogation
            grad = msePrime(y, output)
            for layer in reversed(model):
                grad = layer.backward(grad, trainingRate)
        
        print(f'{e+1}/{epoch} - Error: {error/len(trainX)}')
        if e == 200:
            trainingRate /= 10
        elif e == 400:
            trainingRate /= 10

def getTrainedModel():
    # load MNIST from server
    (trainX, trainY), (testX, testY) = mnist.load_data()
    trainX, trainY = preprocessData(trainX, trainY)
    testX, testY = preprocessData(testX, testY)

    # Define model
    model = [Dense(28*28, 40),
            Tanh(),
            Dense(40, 10),
            Tanh()]

    # Train
    train(model, trainX, trainY)

    # Test
    correct = 0
    for x, y in zip(testX, testY):
        output = x
        for layer in model:
            output = layer.forward(output)
        print('pred:', np.argmax(output), '\ttrue:', np.argmax(y))
        if np.argmax(output) == np.argmax(y):
            correct += 1
    print('Percent Correct: ', (correct/len(testX)))

    return model

model = getTrainedModel()
modelFile = open('NN-mnist', 'wb')
pickle.dump(model, modelFile)
modelFile.close()
            