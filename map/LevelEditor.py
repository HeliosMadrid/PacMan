import math
from enum import Enum

import pgzrun
from pgzero.rect import *
from pgzero.constants import *

WIDTH = 800
HEIGHT = 800

level = []


class CaseState(Enum):
    VOID = '.'
    OBSTACLE = 'x'
    GUM = 'o'


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


def saveLevel():
    with open('./level1.map', 'w') as levelFile:
        for line in level:
            for c in line:
                levelFile.write(c.value)
            levelFile.write('\r')


def on_key_down(key):
    if key == keys.RETURN:
        saveLevel()


def on_mouse_down(pos, button):
    if level:
        step = WIDTH / len(level)
        x, y = math.floor(pos[0] / step), math.floor(pos[1] / step)
        if button == mouse.LEFT:
            level[y][x] = CaseState.OBSTACLE if level[y][x] != CaseState.OBSTACLE else CaseState.VOID
        elif button == mouse.RIGHT:
            level[y][x] = CaseState.GUM if level[y][x] != CaseState.GUM else CaseState.VOID


# teste pour avoir une troisième option dan l'éditeur de niveau
'''
def edit (pos, rel, buttons):
    if mouse.LEFT in buttons :
        set_case(pos, 1)
    elif mouse.RIGHT in buttons:
        set_case(pos, 2)
    elif mouse.MIDDLE in buttons:
        set_case(pos, 2)
'''


def update():
    if not level:
        loadLevel()


def getCaseColor(state):
    return 'green' if state == CaseState.VOID else 'red' if state == CaseState.OBSTACLE else 'blue' if state == CaseState.GUM else 'black'


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
