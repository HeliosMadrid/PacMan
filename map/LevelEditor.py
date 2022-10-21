import math
from enum import Enum

import pgzrun
from pgzero.rect import *
from pgzero.constants import *

# Dimensions de l'éditeur
WIDTH = 800
HEIGHT = 800

# Objet encapsulant la map
level = []


# Énumération contenant les différents états pour les cases
class CaseState(Enum):
    VOID = '.'
    OBSTACLE = 'x'
    GUM = 'o'


# Fonction en charge de charger la map depuis le fichier (initialise level)
def loadLevel():
    with open('./level1.map', 'r') as levelFile:
        for line in levelFile:
            row = []
            for c in line:
                if c == CaseState.VOID.value:
                    row.append(CaseState.VOID)
                elif c == CaseState.OBSTACLE.value:
                    row.append(CaseState.OBSTACLE)
                elif c == CaseState.GUM.value:
                    row.append(CaseState.GUM)
            level.append(row)


# Fonction qui écrit la map définit dans le fichier
def saveLevel():
    with open('./level1.map', 'w') as levelFile:
        for line in level:
            for c in line:
                levelFile.write(c.value)
            levelFile.write('\r')


def on_key_down(key):
    # Touche à utiliser pour enregister des modifications
    if key == keys.RETURN:
        saveLevel()


# Fonction qui permet à l'utilisateur de modifier la map
def on_mouse_down(pos, button):
    if level:
        step = WIDTH / len(level)
        x, y = math.floor(pos[0] / step), math.floor(pos[1] / step)
        if button == mouse.LEFT:
            level[y][x] = CaseState.OBSTACLE if level[y][x] != CaseState.OBSTACLE else CaseState.VOID
        elif button == mouse.RIGHT:
            level[y][x] = CaseState.GUM if level[y][x] != CaseState.GUM else CaseState.VOID


# Charge le niveau au début
def update():
    if not level:
        loadLevel()


# Déduit la couleur d'une case en fontion de son état
def getCaseColor(state):
    return 'green' if state == CaseState.VOID else 'red' if state == CaseState.OBSTACLE else 'blue' if state == CaseState.GUM else 'black'


# Affiche la grille
def drawGrid(screen):
    step = WIDTH / len(level)
    for y in range(len(level)):
        for x in range(len(level[0])):
            screen.draw.filled_rect(Rect((x * step, y * step), (x * step + step, y * step + step)),
                                    getCaseColor(level[y][x]))

    for y in range(len(level)):
        screen.draw.line((0, y * step), (WIDTH, y * step), 'black')
        screen.draw.line((y * step, 0), (y * step, WIDTH), 'black')


def draw():
    screen.clear()
    screen.fill('gray')
    if level:
        drawGrid(screen)


pgzrun.go()
