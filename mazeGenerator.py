# ================== SOURCES ===================== #
# from https://www.baeldung.com/cs/maze-generation #
# ================================================ #

import random

class Cell:
    wallPairs = {'U': 'D', 'D': 'U', 'R': 'L', 'L': 'R'}

    def __init__(self, row, col):
        self.row, self.col = row, col
        self.connections = {'U': False, 'D': False, 'R': False, 'L': False}

    def isUnvisited(self):
        for val in self.connections.values():
            if val:
                return False
        return True

    def addConnection(self, other, wall):
        self.connections[wall] = True
        other.connections[Cell.wallPairs[wall]] = True


class Maze:
    def __init__(self, size, startRow, startCol):
        self.size = size
        self.row, self.col = startRow, startCol
        self.maze = [[Cell(x, y) for y in range(size)] for x in range(size)]

    def cellAt(self, row, y):
        return self.maze[row][y]

    def convertMaze(self):
        mazeArray = [[True for _ in range(self.size * 2 + 1)]]
        for row in range(self.size):
            mazeRow = [True]
            for col in range(self.size):
                mazeRow.append(False)
                if self.maze[row][col].connections['R']:
                    mazeRow.append(False)
                else:
                    mazeRow.append(True)
            mazeArray.append(mazeRow)
            mazeRow = [True]
            for col in range(self.size):
                if self.maze[row][col].connections['D']:
                    mazeRow.append(False)
                else:
                    mazeRow.append(True)
                mazeRow.append(True)
            mazeArray.append(mazeRow)
        return mazeArray


    def findValidNeighbors(self, cell):
        delta = [('L', (0, -1)),
                 ('R', (0, 1)),
                 ('D', (1, 0)),
                 ('U', (-1, 0))]
        neighbours = []
        for direction, (drow, dcol) in delta:
            row2, col2 = cell.row + drow, cell.col + dcol
            if (0 <= row2 < self.size) and (0 <= col2 < self.size):
                neighbour = self.maze[row2][col2]
                if neighbour.isUnvisited():
                    neighbours.append((direction, neighbour))
        return neighbours

    def generateMaze(self, currentCell=None):
        if currentCell==None: currentCell = self.maze[self.row][self.col]
        neighbors = self.findValidNeighbors(currentCell)

        while neighbors != []:
            neighbors = self.findValidNeighbors(currentCell)
            if neighbors != []: 
                direction, nextCell = random.choice(neighbors)
            currentCell.addConnection(nextCell, direction)
            self.generateMaze(nextCell)
            if (direction, nextCell) in neighbors:
                neighbors.remove((direction, nextCell))