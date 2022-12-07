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

# runPipCommand('install', 'numpy')

import numpy as np
from layer import Layer

class Dense(Layer):
    def __init__(self, inputSize, outputSize):
        self.weights = np.random.randn(outputSize, inputSize)
        self.bias = np.random.randn(outputSize, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    def backward(self, outputGradient, learningRate):
        weightsGradient = np.dot(outputGradient, self.input.T)
        inputGradient = np.dot(self.weights.T, outputGradient)
        self.weights -= learningRate * weightsGradient
        self.bias -= learningRate * outputGradient
        return inputGradient