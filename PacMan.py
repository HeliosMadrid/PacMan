import random

import pgzrun
from pgzero.keyboard import keyboard

from Entity import *

top_left_corner_path = "tiles/top_left_corner.png"
top_right_corner_path = "tiles/top_right_corner.png"
bottom_right_corner_path = "tiles/bottom_right_corner.png"
bottom_left_corner_path = "tiles/bottom_left_corner.png"
vertical_right_path = "tiles/vertical_right.png"
vertical_left_path = "tiles/vertical_left.png"
horizontal_top_path = "tiles/horizontal_top.png"
horizontal_bottom_path = "tiles/horizontal_bottom.png"
bottom_left_corner_in_path = "tiles/bottom_left_corner_in.png"
bottom_right_corner_in_path = "tiles/bottom_right_corner_in.png"
top_left_corner_in_path = "tiles/top_left_corner_in.png"
top_right_corner_in_path = "tiles/top_right_corner_in.png"
bottom_right_joint_path = "tiles/bottom_right_joint.png"
bottom_left_joint_path = "tiles/bottom_left_joint.png"
top_right_joint_path = "tiles/top_right_joint.png"
top_left_joint_path = "tiles/top_left_joint.png"

WIDTH = 480
HEIGHT = 480

# fréquence à laquelle les personnages sont update(move), 30 équivaut à 2 fois par seconde
frame_rate = 30

# variable qui compte les frames, et retourne à 0 toutes les 30 frames
frame = 0

# valeur indiquant à quelle distance est on de la prochaine update, entre 0 et 1
deltaTime = 0

# objet encapsulant pac man
pac_man = None

# compteur de points
points = 0

# variable contenant la map
grid = []


# fonction qui charge la variable grid à partir du fichier map/level1.map
def loadGrid():
    with open('map/level1.map', 'r') as levelFile:
        for line in levelFile:
            row = []
            for c in line:
                if c == '.':
                    # 1 chance sur 50 que la case soit un super gum sinon c'est un point
                    if random.randint(0, 50) == 0:
                        row.append(CaseState.GUM)
                    else:
                        row.append(CaseState.POINT)
                elif c == 'x':
                    row.append(CaseState.OBSTACLE)
            grid.append(row)


def update():
    global frame, deltaTime, pac_man, grid, points

    # charge la grid si elle n'est pas déjà chargée
    if not grid:
        loadGrid()
        pac_man = PacMan(13, 13, WIDTH, HEIGHT, len(grid[0]), len(grid))

    # gère les inputs du joueur
    if keyboard.UP:
        pac_man.up(grid)
    if keyboard.DOWN:
        pac_man.down(grid)
    if keyboard.RIGHT:
        pac_man.right(grid)
    if keyboard.LEFT:
        pac_man.left(grid)

    # actualise l'animation
    pac_man.updateImage(frame)

    # actualise la logique du jeu
    if frame % frame_rate == 0:
        grid, points = pac_man.update(grid, points)
        pac_man.move(grid)
        frame = 0

    # calcul delta time
    deltaTime = (frame % frame_rate) / frame_rate
    # augmente frame de 1
    frame += 1


# fonction qui dessine la grid, juste en affichant des carrés bleus ou noir ou des points ou des gums
def drawGrid():
    gridWidth = len(grid[0])
    gridHeight = len(grid)

    deltaWidth = WIDTH / gridWidth
    deltaHeight = HEIGHT / gridHeight

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == CaseState.OBSTACLE:
                # screen.draw.filled_rect(Rect((x * deltaWidth, y * deltaHeight), (16, 16)), (33, 33, 255))
                up = grid[y - 1][x] == CaseState.OBSTACLE if y > 0 else False
                down = grid[y + 1][x] == CaseState.OBSTACLE if y < len(grid) - 1 else False
                right = grid[y][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 else False
                left = grid[y][x - 1] == CaseState.OBSTACLE if x > 0 else False
                up_right = grid[y - 1][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 and y > 0 else False
                up_left = grid[y - 1][x - 1] == CaseState.OBSTACLE if x > 0 and y > 0 else False
                down_right = grid[y + 1][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 and y < len(grid) - 1 else False
                down_left = grid[y + 1][x - 1] == CaseState.OBSTACLE if x > 0 and y < len(grid) - 1 else False

                if down and right and (not up and not left):
                    screen.blit(top_left_corner_path, (x * deltaWidth, y * deltaHeight))
                elif left and down and (not up and not right):
                    screen.blit(top_right_corner_path, (x * deltaWidth, y * deltaHeight))
                elif left and up and (not down and not right):
                    screen.blit(bottom_right_corner_path, (x * deltaWidth, y * deltaHeight))
                elif up and right and (not left and not down):
                    screen.blit(bottom_left_corner_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and not left and down_right and not up_right:
                    screen.blit(bottom_left_joint_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and not right and left and down_left and not up_left:
                    screen.blit(bottom_right_joint_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and not right and left and not down_left and up_left:
                    screen.blit(top_right_joint_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and not left and not down_right and up_right:
                    screen.blit(top_left_joint_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and left and not right:
                    screen.blit(vertical_right_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and not left:
                    screen.blit(vertical_left_path, (x * deltaWidth, y * deltaHeight))
                elif left and right and up and not down:
                    screen.blit(horizontal_bottom_path, (x * deltaWidth, y * deltaHeight))
                elif left and right and down and not up:
                    screen.blit(horizontal_top_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and left and up_right and up_left and down_right and not down_left:
                    screen.blit(top_right_corner_in_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and left and up_right and up_left and down_left and not down_right:
                    screen.blit(top_left_corner_in_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and left and up_right and not up_left and down_right and down_left:
                    screen.blit(bottom_right_corner_in_path, (x * deltaWidth, y * deltaHeight))
                elif up and down and right and left and not up_right and up_left and down_right and down_left:
                    screen.blit(bottom_left_corner_in_path, (x * deltaWidth, y * deltaHeight))
            elif grid[y][x] == CaseState.POINT:
                screen.blit(point_path, (x * deltaWidth, y * deltaHeight))
            elif grid[y][x] == CaseState.GUM:
                screen.blit(gum_path, (x * deltaWidth, y * deltaHeight))

        # quadrillage
        #for y in range(gridHeight):
            #screen.draw.line((0, y * deltaHeight), (WIDTH, y * deltaHeight), 'white')
        #for x in range(gridWidth):
            #screen.draw.line((x * deltaWidth, 0), (x * deltaWidth, HEIGHT), 'white')


# fonction de dessin
def draw():
    screen.clear()
    screen.fill('black')

    drawGrid()
    # dessine pas man
    pac_man.draw(deltaTime)


pgzrun.go()
