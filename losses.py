# ========================================= CITATIONS ================================================================================================================ #
# from https://www.simplilearn.com/tutorials/statistics-tutorial/mean-squared-error#:~:text=The%20Mean%20Squared%20Error%20measures,it%20relates%20to%20a%20function.  #
# ==================================================================================================================================================================== # 
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

def mse(yTrue, yPred):
    return np.mean((yTrue-yPred)**2)

def msePrime(yTrue, yPred):
    return 2 * (yPred - yTrue) / np.size(yTrue)