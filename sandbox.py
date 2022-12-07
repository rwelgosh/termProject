# from cmu_cs3_graphics import *
# import pandas as pd
# import pickle
# import numpy as np
# import copy
# import matplotlib.pyplot as plt
# from keras.datasets import mnist

# def onAppStart(app):
#     app.setMaxShapeCount(400*400)
#     modelFile = open('NN-mnist', 'rb')
#     app.model = pickle.load(modelFile)
#     modelFile.close()

#     app.pixels = set()
#     app.spellList = [[0 for col in range(400)] for row in range(400)]


# def redrawAll(app):
#     for pos in app.pixels:
#         row, col = pos[0], pos[1]
#         drawRect(row, col, 20, 20, fill='black', align='center')


# def onMouseDrag(app, mouseX, mouseY):
#     app.pixels.add((mouseX, mouseY))
#     for i in range(-10, 11):
#         for j in range(-10, 11):
#             app.spellList[mouseY+i][mouseX+j] = 255 + (-1*abs(i)*10) + (-1*abs(j)*10)


# def predict(app):
#     # reshape and normalize input data
#     x = copy.deepcopy(app.spellList)
#     app.spellList = [[0 for col in range(400)] for row in range(400)]
#     app.pixels = set()
#     newX = []
#     for row in range(len(x)//14):
#         newRow = []
#         for col in range(len(x[0])//14):
#             val = 0
#             for i in range(14):
#                 for j in range(14):
#                     val += x[14*row+i][14*col+j]
#             newRow.append(val)
#         newX.append(newRow)
#     newX = np.array(newX)
#     plt.imshow(np.array(newX), interpolation='nearest')
#     plt.show()

#     newX = newX.reshape(28 * 28, 1)
#     newX = newX.astype("float32") / 255

#     output = newX
#     for layer in app.model:
#         output = layer.forward(output)
#     return np.argmax(output)


# def onKeyPress(app, key):
#     if key == 'c':
#         answer = predict(app)
#         print(answer)


# def main():
#     runApp(width=400, height=400)

# main()

from mazeGenerator import Maze
from cmu_cs3_graphics import *

# Maze dimensions (ncols, nrows)
nx, ny = 10, 10
# Maze entry position
ix, iy = 0, 0

maze = Maze(10, ix, iy)
maze.generateMaze()

print(maze)