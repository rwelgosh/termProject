from cmu_cs3_graphics import *
import pandas as pd
import pickle

def onAppStart(app):
    app.setMaxShapeCount(400*400)

    app.pixels = set()
    app.spellsData = pd.DataFrame(columns=['label', 'drawling'])
    app.point = 0
    app.spellList = [[0 for col in range(400)] for row in range(400)]


def redrawAll(app):
    for pos in app.pixels:
        row, col = pos[0], pos[1]
        drawRect(row, col, 1, 1, fill='black')


def onMouseDrag(app, mouseX, mouseY):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            app.pixels.add((mouseX+dc, mouseY+dr, app.point))
            app.spellList[mouseY][mouseX] = 100 + (-1*abs(dr)*20) + (-1*abs(dc)*20)
    app.point += 1


def resetPixels(app, spell):
    app.pixels = set()
    curSpell = pd.DataFrame([[spell, app.spellList]], columns=['label', 'drawling'])
    print(curSpell)
    app.spellsData = pd.concat([app.spellsData, curSpell], ignore_index=True)
    app.spellList = [[0 for col in range(400)] for row in range(400)]
    dataFile = open('spellsDict', 'wb')
    pickle.dump(app.spellsData, dataFile)
    dataFile.close()


def onKeyPress(app, key):
    if key == 'b':
        #bombarda
        resetPixels(app, 'b')
    elif key == 'e':
        #expelliarmus
        resetPixels(app, 'e')
    elif key == 'l':
        #lum
        resetPixels(app, 'l')
    elif key == 'n':
        #nox
        resetPixels(app, 'n')
    elif key == 'c':
        app.pixels = set()
        app.spellList = [[0 for col in range(400)] for row in range(400)]


def main():
    runApp(width=400, height=400)
    

main()
