# Class modélisant une entité sur une grille
import math
from enum import Enum

from pgzero.actor import Actor


# Enumeration des valeurs possible pour chaque point de la grille
class CaseState(Enum):
    VOID = 0
    POINT = 1
    OBSTACLE = 2
    GUM = 3


# banque d'image
blinky_right_0 = 'tiles/blinky_right_0'
pac_man_left_0 = 'tiles/pac_man_left_0'
pac_man_right_0 = 'tiles/pac_man_right_0'
pac_man_down_0 = 'tiles/pac_man_down_0'
pac_man_up_0 = 'tiles/pac_man_up_0'
pac_man_left_1 = 'tiles/pac_man_left_1'
pac_man_right_1 = 'tiles/pac_man_right_1'
pac_man_down_1 = 'tiles/pac_man_down_1'
pac_man_up_1 = 'tiles/pac_man_up_1'
point_path = "tiles/point.png"
gum_path = "tiles/gum.png"


# Fonction qui renvoie l'interpolation linéaire entre les points (x1, y1) et (x2, y2) selon d qui est entre 0 et 1,
# voir https://www.aquaportail.com/pictures2208/interpolation-lineaire.jpg
def lerp(x1, y1, x2, y2, d):
    x = x1 + ((x2 - x1) * d)
    y = y1 + ((y2 - y1) * d)
    return x, y


def chooseTheBest(set_):
    bestIndex = 0
    for i in range(len(set_)):
        if set_[i][2] < set_[bestIndex][2]:
            bestIndex = i
    return set_[bestIndex]


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def isInSet(set_, cell):
    for i in range(len(set_)):
        c = set_[i]
        if c[0] == cell[0] and c[1] == cell[1]:
            return True, i
    return False, None


def neighbors(grid, cell, targetX, targetY):
    x, y, g = cell[0], cell[1], cell[3]
    res = []
    if y > 0:
        if grid[y - 1][x] != CaseState.OBSTACLE:
            res.append((x, y - 1, dist(x, y - 1, targetX, targetY), g + 1, cell))
    if y < len(grid):
        if grid[y + 1][x] != CaseState.OBSTACLE:
            res.append((x, y + 1, dist(x, y + 1, targetX, targetY), g + 1, cell))
    if x > 0:
        if grid[y][x - 1] != CaseState.OBSTACLE:
            res.append((x - 1, y, dist(x - 1, y, targetX, targetY), g + 1, cell))
    if x < len(grid[0]):
        if grid[y][x + 1] != CaseState.OBSTACLE:
            res.append((x + 1, y, dist(x + 1, y, targetX, targetY), g + 1, cell))
    return res


# Fonction qui permet de calculer le meilleur chemin pour aller d'un point à un autre
# Voir A* algorithm : https://en.wikipedia.org/wiki/A*_search_algorithm
def A_star(grid, x, y, targetX, targetY):
    if x == targetX and y == targetY:
        return x, y

    open_set = [(x, y, 0, 0, None)]
    closed_set = []

    while len(open_set) > 0:
        current = chooseTheBest(open_set)

        if current[0] == targetX and current[1] == targetY:
            while current[4] is not None:
                if current[4][4] is None:
                    return current[0], current[1]
                current = current[4]

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in neighbors(grid, current, targetX, targetY):
            if not (neighbor in closed_set):
                test = isInSet(open_set, neighbor)
                if test[0]:
                    if neighbor[3] < open_set[test[1]][3]:
                        open_set[test[1]] = neighbor
                else:
                    open_set.append(neighbor)


class GridEntity:
    # fonction d'initialisation, definissant la position de départ ainsi que l'acteur
    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        self.xPos = xPos
        self.yPos = yPos
        self.prevXPos = xPos
        self.prevYPos = yPos
        self.actor = Actor(pac_man_right_0)
        # self.screenWidth = screenWidth
        # self.screenHeight = screenHeight
        # self.gridWidth = gridWidth
        # self.gridHeight = gridHeight

        self.deltaWidth = screenWidth / gridWidth
        self.deltaHeight = screenHeight / gridHeight

        self.actor.topright = ((xPos + 1) * self.deltaWidth, yPos * self.deltaHeight)

    # fonction de dessein de l'entité
    def draw(self, dt):
        self.actor.topright = lerp((self.prevXPos + 1) * self.deltaWidth, self.prevYPos * self.deltaHeight,
                                   (self.xPos + 1) * self.deltaWidth, self.yPos * self.deltaHeight, dt)
        self.actor.draw()


class PacMan(GridEntity):

    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        self.xSpeed = 0
        self.ySpeed = 0
        super().__init__(xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight)

    # met à jour le vecteur de déplacement
    def up(self, grid):
        if self.yPos < len(grid) - 1 and grid[self.yPos - 1][self.xPos] != CaseState.OBSTACLE:
            self.xSpeed = 0
            self.ySpeed = -1

    # met à jour le vecteur de déplacement
    def down(self, grid):
        if self.yPos > 0 and grid[self.yPos + 1][self.xPos] != CaseState.OBSTACLE:
            self.xSpeed = 0
            self.ySpeed = 1

    # met à jour le vecteur de déplacement
    def right(self, grid):
        if self.xPos < len(grid[0]) - 1 and grid[self.yPos][self.xPos + 1] != CaseState.OBSTACLE:
            self.xSpeed = 1
            self.ySpeed = 0

    # met à jour le vecteur de déplacement
    def left(self, grid):
        if self.xPos > 0 and grid[self.yPos][self.xPos - 1] != CaseState.OBSTACLE:
            self.xSpeed = -1
            self.ySpeed = 0

    # met à jour l'image pour faire l'animation
    def updateImage(self, frame):
        right = pac_man_right_0 if frame < 15 else pac_man_right_1
        left = pac_man_left_0 if frame < 15 else pac_man_left_1
        down = pac_man_down_0 if frame < 15 else pac_man_down_1
        up = pac_man_up_0 if frame < 15 else pac_man_up_1

        if self.xSpeed == 1 and self.ySpeed == 0:
            self.actor.image = right
        elif self.xSpeed == -1 and self.ySpeed == 0:
            self.actor.image = left
        elif self.xSpeed == 0 and self.ySpeed == 1:
            self.actor.image = down
        elif self.xSpeed == 0 and self.ySpeed == -1:
            self.actor.image = up

    # Fonction update qui ramasse les points
    def update(self, grid, points):
        if grid[self.yPos][self.xPos] == CaseState.POINT:
            points += 1
            grid[self.yPos][self.xPos] = CaseState.VOID
        elif grid[self.yPos][self.xPos] == CaseState.GUM:
            points += 5
            grid[self.yPos][self.xPos] = CaseState.VOID

        return grid, points

    # fonction déplacement qui met à jour la position et gère les collisions
    def move(self, grid):
        newX = self.xPos + self.xSpeed
        newY = self.yPos + self.ySpeed

        self.prevXPos = self.xPos
        self.prevYPos = self.yPos
        if 0 < newX < len(grid[0]) and 0 < newY < len(grid):
            if grid[newY][newX] != CaseState.OBSTACLE:
                self.xPos = newX
                self.yPos = newY


class Blinky(GridEntity):
    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        super().__init__(xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight)
        self.actor.image = blinky_right_0

    def track(self, targetX, targetY, grid):
        self.prevXPos = self.xPos
        self.prevYPos = self.yPos
        self.xPos, self.yPos = A_star(grid, self.xPos, self.yPos, targetX, targetY)
