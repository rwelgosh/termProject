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

class Tanh(Layer):
    def __init__(self):
        self.input = None

    def forward(self, input):
        self.input = input
        return np.tanh(input)
    
    def backward(self, outputGradient, learningRate):
        return np.multiply(outputGradient, 1-np.tanh(self.input)**2)