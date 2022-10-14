# Class modélisant une entité sur une grille
from enum import Enum

from pgzero.actor import Actor


# Enumeration des valeurs possible pour chaque point de la grille
class CaseState(Enum):
    VOID = 0
    POINT = 1
    OBSTACLE = 2
    GUM = 3


# banque d'image
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
