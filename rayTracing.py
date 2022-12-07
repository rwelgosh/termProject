import pickle
import cmu_cs3_graphics as cs
import random
from PIL import Image
import numpy as np
import copy

from mazeGenerator import Maze
from setScreens import runAppWithScreens, setActiveScreen

def restartMaze(app):
    app.setMaxShapeCount(400*400)
    modelFile = open('NN-mnist', 'rb')
    app.model = pickle.load(modelFile)
    modelFile.close()

    app.spellList = [[0 for col in range(400)] for row in range(400)]
    app.pixels = set()

    app.maze = Maze(21, 10, 10)
    app.maze.generateMaze()
    app.mazeRep = app.maze.convertMaze()
    app.mazeSize = app.maze.size
    app.stepsPerSecond = 100
    app.stepCounter = 0

    app.rx, app.ry = None, None
    while app.rx == None or app.ry == None:
        app.rx = random.randint(1, len(app.mazeRep)-1)
        app.ry = 1
        if app.mazeRep[app.rx][app.ry] == True:
            app.rx = None
            app.ry = None
    app.blockSize = 700/len(app.mazeRep)
    app.cx, app.cy = 50+(app.blockSize*app.rx)+app.blockSize/2, 50+(app.blockSize*app.ry)+app.blockSize/2

    app.direction = 'U'
    app.directions = ['U', 'R', 'D', 'L']
    app.directionsIndex = 0

    app.over = False
    app.win = False
    app.lose = False
    app.onEnemy = False
    app.fightingEnemy = False
    app.defeatedEnemy = False
    app.enemyX, app.enemyY = None, None
    app.enemyAnimation2R = 1

    app.enemies2Gif = loadAnimatedGif(app, 'NN/troll.gif')
    app.enemyCounter = 0

    app.enemies3Gif = loadAnimatedGif(app, 'NN/lock.gif')
    app.enemies3GifFrame = app.enemies3Gif[0]

    app.enemies = {}
    for i in range(0):
        position = random.randint(0, len(app.mazeRep)-1), random.randint(0, len(app.mazeRep)-1)
        while position in app.enemies or position == (10, 10) or app.mazeRep[position[0]][position[1]]:
            position = random.randint(0, 20), random.randint(0, 20)
        obsticle = random.randint(1, 3)
        app.enemies[position] = obsticle
    app.counter = 10

    app.house = None
    app.hovering = None
    image = cs.CMUImage(Image.open('NN/ravenclaw.png'))
    img = image.image
    app.imageWidth, app.imageHeight = 162.5, img.height * (162.5/img.width)

def maze_onScreenStart(app):
    restartMaze(app)

def maze_redrawAll(app):
    cs.drawLine(800, 0, 800, 800)
    cs.drawLine(800, 400, 1200, 400)
    cs.drawLine(0,800, 1200, 800)
    cs.drawLabel('Draw 1 for Wingardium Leviosa', 1000, 450, size=14, align='center')
    cs.drawLabel('Draw 2 for Bombarda', 1000, 475, size=14, align='center')
    cs.drawLabel('Draw 3 for Alohamora', 1000, 500, size=14, align='center')
    cs.drawLabel('Draw 4 for Lumos', 1000, 525, size=14, align='center')
    cs.drawLabel('Press c to process drawling', 1000, 575, size=14, align='center')
    blockSize = 700/len(app.mazeRep)
    for row in range(len(app.mazeRep)):
        for col in range(len(app.mazeRep[0])):
            if row == 21 and col == 21:
                    cs.drawRect(50+(blockSize*row), 50+(blockSize*col), blockSize, blockSize, fill='blue')
            if app.mazeRep[row][col]:
                cs.drawRect(50+(blockSize*row), 50+(blockSize*col), blockSize, blockSize, fill='black')

    if app.house == 'r': playerColor = 'blue'
    elif app.house == 'g': playerColor = 'red'
    elif app.house == 'h': playerColor = 'yellow'
    elif app.house == 's': playerColor = 'green'
    else: playerColor = None
    cs.drawCircle(app.cx, app.cy, (blockSize/2)-1, fill=playerColor)

    if app.direction == 'U':
        cs.drawCircle(app.cx, app.cy-2, 3, fill='white')
    elif app.direction == 'D':
        cs.drawCircle(app.cx, app.cy+2, 3, fill='white')
    elif app.direction == 'L':
        cs.drawCircle(app.cx-2, app.cy, 3, fill='white')
    elif app.direction == 'R':
        cs.drawCircle(app.cx+2, app.cy, 3, fill='white')

    if app.win:
        drawWinScreen(app)
    if app.lose:
        drawLoseScreen(app)
    if app.onEnemy:
        drawEnemyScreen(app)

    for pos in app.pixels:
        row, col = pos[0], pos[1]
        cs.drawRect(row, col, 20, 20, fill='black', align='center')

    homeIcon = cs.CMUImage(Image.open('NN/home.png'))
    cs.drawImage(homeIcon, 5, 5, width=40, height=40)

    if app.house == None:
        drawHouseSelection(app)

def drawHouseSelection(app):
    cs.drawRect(0, 0, app.width, app.height, fill='gray', opacity=90)
    images = ['gryffndor.png', 'ravenclaw.png', 'slytherin.png', 'hufflepuff.png']
    for i in range(4):
        image = cs.CMUImage(Image.open('NN/'+images[i]))
        img = image.image
        x, y = 200 + (212.5*i), app.height/2 - (img.height * (162.5/img.width))/2
        cs.drawRect(x-1.5, y-1.5, 162.5 + 3, img.height * (162.5/img.width) + 3, fill='white', border='black' if not app.hovering==i else 'blue')
        cs.drawImage(image, x, y, width=162.5, height=img.height * (162.5/img.width))

def drawEnemy1(app):
    # Wingardrum Leviosa
    image1 = cs.CMUImage(Image.open('NN/rock.png'))
    img = image1.image
    cs.drawImage(image1, app.enemyX, app.enemyY, align='center', width=300, height=img.height * (300/img.width))
    cs.drawLabel("There's a rock in your way, use Wingardrum Leviosa to get through", 400, 625, size=18, align='center')
    cs.drawLabel(str(app.counter), 400, 675)

def loadAnimatedGif(app, path):
    pilImages = Image.open(path)
    if pilImages.format != 'WEBP' and pilImages.format != 'GIF':
        raise Exception(f'{path} is not an animated image!')
    if not pilImages.is_animated:
        raise Exception(f'{path} is not an animated image!')
    cmuImages = [ ]
    for frame in range(pilImages.n_frames):
        pilImages.seek(frame)
        pilImage = pilImages.copy()
        cmuImages.append(cs.CMUImage(pilImage))
    return cmuImages

def drawEnemy2(app):
    enemy = app.enemies2Gif[app.enemyCounter]
    enm = enemy.image
    cs.drawImage(enemy, app.enemyX, app.enemyY, width=400, height=enm.height * (400/enm.width), align='center')
    cs.drawLabel("A Troll is in your way, use Bombarda to get through", 400, 625, size=18, align='center')
    cs.drawLabel(str(app.counter), 400, 675)
    if app.defeatedEnemy:
        r1 = app.enemyAnimation2R
        r2 = app.enemyAnimation2R - 20 if app.enemyAnimation2R > 20 else 1
        r3 = app.enemyAnimation2R - 35 if app.enemyAnimation2R > 35 else 1
        cs.drawStar(app.enemyX, app.enemyY, r1, 12, fill='red')
        cs.drawStar(app.enemyX, app.enemyY, r2, 12, fill='orange')
        cs.drawStar(app.enemyX, app.enemyY, r3, 12, fill='yellow')

def drawEnemy3(app, enemy):
    enm = enemy.image
    cs.drawImage(enemy, app.enemyX, app.enemyY, width=600, height=enm.height * (600/enm.width), align='center')
    cs.drawLabel("A locked door is in your way, use Alohamora to get through", 400, 625, size=18, align='center')
    cs.drawLabel(str(app.counter), 400, 675)

def drawEnemyScreen(app):
    cs.drawRect(0, 0, 800, 800, opacity=40, fill='gray')
    cs.drawRect(400, 400, 600, 600, fill='white', align='center')
    cs.drawLine(100, 600, 700, 600)
    if app.enemies[(app.rx, app.ry)] == 1:
        drawEnemy1(app)
    elif app.enemies[(app.rx, app.ry)] == 2:
        drawEnemy2(app)
    elif app.enemies[(app.rx, app.ry)] == 3:
        drawEnemy3(app, app.enemies3GifFrame)
    elif app.enemies[(app.rx, app.ry)] == 4:
        pass

def maze_onStep(app):
    if app.fightingEnemy:
        app.stepCounter += 1
        app.enemyCounter = (1+app.enemyCounter) % len(app.enemies2Gif)
        if app.stepCounter % 25 == 0:
            app.counter -= 1
            if app.counter == 0:
                app.onEnemy = False
                app.fightingEnemy = False
                app.lose = True
                app.over = True
    elif app.defeatedEnemy:
        if app.enemies[(app.rx, app.ry)] == 1:
            app.enemyY -= 5
            if app.enemyY <= 250:
                app.onEnemy = False
                app.defeatedEnemy = False
                app.enemies.pop((app.rx, app.ry), None)
        elif app.enemies[(app.rx, app.ry)] == 2:
            app.enemyAnimation2R += 2
            if app.enemyAnimation2R >= 150:
                app.onEnemy = False
                app.defeatedEnemy = False
                app.enemies.pop((app.rx, app.ry), None)
        elif app.enemies[(app.rx, app.ry)] == 3:
            app.enemies3GifFrame = app.enemies3Gif[app.enemyCounter]
            app.enemyCounter += 1
            if app.enemyCounter >= len(app.enemies3Gif)//3:
                app.onEnemy = False
                app.defeatedEnemy = False
                app.enemies.pop((app.rx, app.ry), None)
                app.enemyCounter = 0
                app.enemies3GifFrame = app.enemies3Gif[0]

def predict(app):
    # reshape and normalize input data
    x = copy.deepcopy(app.spellList)
    app.spellList = [[0 for col in range(400)] for row in range(400)]
    app.pixels = set()
    newX = []
    for row in range(len(x)//14):
        newRow = []
        for col in range(len(x[0])//14):
            val = 0
            for i in range(14):
                for j in range(14):
                    val += x[14*row+i][14*col+j]
            newRow.append(val)
        newX.append(newRow)
    newX = np.array(newX)

    newX = newX.reshape(28 * 28, 1)
    newX = newX.astype("float32") / 255

    output = newX
    for layer in app.model:
        output = layer.forward(output)
    return np.argmax(output)

def maze_onKeyPress(app, key):
    if key == 'c':
        value = predict(app)
        if app.enemies[(app.rx, app.ry)] == value:
            app.enemyAnimation2R = 1
            app.fightingEnemy = False
            app.defeatedEnemy = True
            app.counter = 10
            app.enemyCounter = 0
            app.enemies3GifFrame = app.enemies3Gif[0]

def drawWinScreen(app):
    cs.drawRect(0, 0, app.width, app.height, opacity=40, fill='gray')
    cs.drawRect(400, 400, 500, 300, fill='white', align='center')
    cs.drawLabel('You Win!', 400, 300, size=16)
    cs.drawRect(300, 500, 75, 45, fill=None, border='black', align='center')
    cs.drawLabel('Go Home', 300, 500)
    cs.drawRect(500, 500, 75, 45, fill=None, border='black', align='center')
    cs.drawLabel('Play Again', 500, 500)

def drawLoseScreen(app):
    cs.drawRect(0, 0, app.width, app.height, opacity=40, fill='gray')
    cs.drawRect(400, 400, 500, 300, fill='white', align='center')
    cs.drawLabel('You Lose!', 400, 300, size=16)
    cs.drawRect(300, 500, 75, 45, fill=None, border='black', align='center')
    cs.drawLabel('Go Home', 300, 500)
    cs.drawRect(500, 500, 75, 45, fill=None, border='black', align='center')
    cs.drawLabel('Play Again', 500, 500)

def touchesBlock(app):
    r = ((app.blockSize/2)-1)
    if (app.mazeRep[int((app.cx+r-50)//app.blockSize)][int((app.cy-50)//app.blockSize)] or 
        app.mazeRep[int((app.cx-r-50)//app.blockSize)][int((app.cy-50)//app.blockSize)] or 
        app.mazeRep[int((app.cx-50)//app.blockSize)][int((app.cy+r-50)//app.blockSize)] or 
        app.mazeRep[int((app.cx-50)//app.blockSize)][int((app.cy-r-50)//app.blockSize)]):
        return True
    return False

def maze_onKeyHold(app, keys):
    if ((app.cx-50)//app.blockSize, (app.cy-50)//app.blockSize) != (app.rx, app.ry):
        app.rx, app.ry = ((app.cx-50)//app.blockSize, (app.cy-50)//app.blockSize)
        print(app.rx, app.ry)
    if not app.over and not app.onEnemy:
        if 'up' in keys:
            if app.direction == 'U':
                app.cy -= app.blockSize/3
                if touchesBlock(app):
                    app.cy += app.blockSize/3
            elif app.direction == 'R':
                app.cx += app.blockSize/3
                if touchesBlock(app):
                    app.cx -= app.blockSize/3
            elif app.direction == 'D':
                app.cy += app.blockSize/3
                if touchesBlock(app):
                    app.cy -= app.blockSize/3
            elif app.direction == 'L':
                app.cx -= app.blockSize/3
                if touchesBlock(app):
                    app.cx += app.blockSize/3
        elif 'down' in keys:
            if app.direction == 'U':
                app.cy += app.blockSize/3
                if touchesBlock(app):
                    app.cy -= app.blockSize/3
            elif app.direction == 'R':
                app.cx -= app.blockSize/3
                if touchesBlock(app):
                    app.cx += app.blockSize/3
            elif app.direction == 'D':
                app.cy -= app.blockSize/3
                if touchesBlock(app):
                    app.cy += app.blockSize/3
            elif app.direction == 'L':
                app.cx += app.blockSize/3
                if touchesBlock(app):
                    app.cx -= app.blockSize/3
        if 'right' in keys:
            app.directionsIndex = (app.directionsIndex + 1) % 4
            app.direction = app.directions[app.directionsIndex]
        elif 'left' in keys:
            app.directionsIndex = (app.directionsIndex - 1) % 4
            app.direction = app.directions[app.directionsIndex]
        if app.rx == 21 and app.ry == 21:
            app.win = True
            app.over = True
        if (app.rx, app.ry) in app.enemies:
            app.onEnemy = True
            app.fightingEnemy = True
            app.enemyX, app.enemyY = 400, 400

def maze_onMousePress(app, mouseX, mouseY):
    if app.over and (app.lose or app.win):
        if 500-(75/2) <= mouseX <= 500+(75/2) and 500-(45/2) <= mouseY <= 500+(45/2):
            restartMaze(app)
        elif 300-(75/2) <= mouseX <= 300+(75/2) and 500-(45/2) <= mouseY <= 500+(45/2):
            restartMaze(app)
            setActiveScreen('start')
    elif app.house == None:
        houses = ['g', 'r', 's', 'h']
        app.house = houses[app.hovering]
    elif 5 <= mouseX <= 45 and 5 <= mouseY <= 45: setActiveScreen('start')

def maze_onMouseDrag(app, mouseX, mouseY):
    if not app.over:
        if mouseX > 800 and mouseY < 400:
            app.pixels.add((mouseX, mouseY))
            for i in range(-10, 11):
                for j in range(-10, 11):
                    if 0 <= mouseY+i < 400 and 0 <= mouseX-800+j < 400:
                        app.spellList[mouseY+i][mouseX-800+j] = 255 + (-1*abs(i)*5) + (-1*abs(j)*5)

def maze_onMouseMove(app, mouseX, mouseY):
    if app.house == None:
        for i in range(4):
            x, y = 200 + (212.5*i), app.height/2 - (app.imageHeight * (162.5/app.imageWidth))/2
            if x-1.5 < mouseX < x+162.5+1.5 and y-1.5 < mouseY < y+(app.imageHeight * (162.5/app.imageWidth))+1.5:
                app.hovering = i 
        return None

def main():
    runAppWithScreens(initialScreen='maze', width=1200, height = 800)
    
main()