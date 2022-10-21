import math

from pgzero.rect import *
from pgzero.constants import *

WIDTH = 800
HEIGHT = 800

level = []


def loadLevel():
    with open('./level1.map', 'r') as levelFile:
        for line in levelFile:
            row = []
            for c in line:
                if c == '.':
                    row.append(True)
                elif c == 'x':
                    row.append(False)
            level.append(row)


def saveLevel():
    with open('./level1.map', 'w') as levelFile:
        for line in level:
            for c in line:
                levelFile.write('.' if c else 'x')
            levelFile.write('\r')


def on_key_down(key):
    if key == keys.SPACE:
        loadLevel()
    elif key == keys.RETURN:
        saveLevel()


def set_case(pos, value):
    if len(level) > 0:
        step = WIDTH / len(level)
        x, y = math.floor(pos[0] / step), math.floor(pos[1] / step)
        level[y][x] = value


def on_mouse_down(pos):
    ...


def on_mouse_move(pos, rel, buttons):
    print(buttons)
    if mouse.LEFT in buttons:
        set_case(pos, False)
    elif mouse.RIGHT in buttons:
        set_case(pos, True)


def drawGrid(screen):
    step = WIDTH / len(level)
    for y in range(len(level)):
        for x in range(len(level[0])):
            screen.draw.filled_rect(Rect((x * step, y * step), (x * step + step, y * step + step)),
                                    'green' if level[y][x] else 'red')
    for y in range(len(level)):
        screen.draw.line((0, y * step), (WIDTH, y * step), 'black')
        screen.draw.line((y * step, 0), (y * step, WIDTH), 'black')


def draw():
    screen.clear()
    screen.fill('gray')
    if len(level) > 0:
        drawGrid(screen)
