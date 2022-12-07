# PIP COMMANDS
# cs.runPipCommand('install', 'soundfile')
# cs.runPipCommand('install', 'sounddevice') 

import math
from cmu_cs3_graphics import *
import soundfile as sf
import sounddevice as sd

class movableObject:
    def __init__(self, x, y):
        self.type = None
        self.ID = None
        self.x = x
        self.y = y
        self.spellList = [False, False, False, False]

    def leviosa(self):
        pass

    def bombarda(self):
        pass

    def lumos(self):
        pass

    def nox(self):
        pass

    def checkPicked(self, mouseX, mouseY):
        pass

    def draw(self):
        pass

    def __eq__(self, other):
        if isinstance(other, movableObject):
            if self.type == other.type and self.ID == other.ID:
                return True
        return False

class Ball(movableObject):
    balls = 0

    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.type = 'ball'
        self.ID = Ball.balls
        Ball.balls += 1
        self.r = r
        self.spellList = [True, True, False, False]
        self.activeAnimation = None
        self.destroy = False
        self.selected = False

    def leviosa(self):
        self.y -= 5
        if self.y <= 50:
            self.activeAnimation = None

    def bombarda(self):
        self.r += 1
        self.y -= 1
        if self.r >= 50:
            self.activeAnimation = None

    def draw(self):
        drawCircle(self.x, self.y, self.r, fill='red', border='blue' if self.selected else None)

    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    def checkPicked(self, mouseX, mouseY):
        if Ball.distance(mouseX, mouseY, self.x, self.y) <= self.r:
            return True
        return False

class Candle(movableObject):
    candles = 0

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'candle'
        self.ID = Candle.candles
        Candle.candles += 1
        self.spellList = [True, True, True, True]
        self.activeAnimation = None
        self.destroy = False
        self.selected = False

        self.lit = False

    def leviosa(self):
        self.y -= 5
        if self.y <= 100:
            self.activeAnimation = None

    def bombarda(self):
        self.activeAnimation = None

    def lumos(self):
        self.lit = True
        self.activeAnimation = None

    def nox(self):
        self.lit = False
        self.activeAnimation = None

    def draw(self):
        drawRect(self.x, self.y, 25, 60, fill='white', border='black' if not self.selected else 'blue')
        drawLine(self.x + 25/2, self.y, self.x + 25/2, self.y - 15)
        if self.lit:
            drawCircle(self.x + 25/2, self.y - 20, 5, fill='orange')

    def checkPicked(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x + 25 and self.y <= mouseY <= self.y + 60:
            return True
        return False

class musicBox(movableObject):
    musicBoxes = 0

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = 'musicBox'
        self.ID = musicBox.musicBoxes
        musicBox.musicBoxes += 1
        self.spellList = [True, True, True, True]
        self.activeAnimation = None
        self.destroy = False
        self.selected = False
        self.musicOn = False

    def leviosa(self):
        self.y -= 5
        if self.y <= 100:
            self.activeAnimation = None

    def bombarda(self):
        self.activeAnimation = None

    def lumos(self):
        data, fs = sf.read('NN/beep-01a.wav', dtype='float32')
        sd.play(data, fs)
        self.activeAnimation = None

    def nox(self):
        self.musicOn = False
        self.activeAnimation = None

    def draw(self):
        drawRect(self.x, self.y, 70, 25, fill='red', border='black' if not self.selected else 'blue')
        drawCircle(self.x+20, self.y, 15, fill='gray', border='black' if not self.selected else 'blue')

    def checkPicked(self, mouseX, mouseY):
        if self.x <= mouseX <= self.x + 70 and self.y <= mouseY <= self.y + 25:
            return True
        return False