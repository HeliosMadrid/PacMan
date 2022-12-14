# Class modélisant une entité sur une grille
import math
from enum import Enum
import random

from pgzero.actor import Actor


# Enumeration des valeurs possible pour chaque point de la grille
class CaseState(Enum):
    VOID = 0
    POINT = 1
    OBSTACLE = 2
    GUM = 3


# banque d'image
clyde_right_0 = 'tiles/clyde_right_0'
clyde_right_1 = 'tiles/clyde_right_1'
clyde_left_0 = 'tiles/clyde_left_0'
clyde_left_1 = 'tiles/clyde_left_1'
clyde_up_0 = 'tiles/clyde_up_0'
clyde_up_1 = 'tiles/clyde_up_1'
clyde_down_0 = 'tiles/clyde_down_0'
clyde_down_1 = 'tiles/clyde_down_1'
blinky_right_0 = 'tiles/blinky_right_0'
blinky_right_1 = 'tiles/blinky_right_1'
blinky_left_0 = 'tiles/blinky_left_0'
blinky_left_1 = 'tiles/blinky_left_1'
blinky_up_0 = 'tiles/blinky_up_0'
blinky_up_1 = 'tiles/blinky_up_1'
blinky_down_0 = 'tiles/blinky_down_0'
blinky_down_1 = 'tiles/blinky_down_1'
pac_man_left_0 = 'tiles/pac_man_left_0'
pac_man_right_0 = 'tiles/pac_man_right_0'
pac_man_down_0 = 'tiles/pac_man_down_0'
pac_man_up_0 = 'tiles/pac_man_up_0'
pac_man_left_1 = 'tiles/pac_man_left_1'
pac_man_right_1 = 'tiles/pac_man_right_1'
pac_man_down_1 = 'tiles/pac_man_down_1'
pac_man_up_1 = 'tiles/pac_man_up_1'
pac_man_dying_anim = ['tiles/pac_man_dying_0', 'tiles/pac_man_dying_2', 'tiles/pac_man_dying_3',
                      'tiles/pac_man_dying_4', 'tiles/pac_man_dying_5', 'tiles/pac_man_dying_6',
                      'tiles/pac_man_dying_7', 'tiles/pac_man_dying_8', 'tiles/pac_man_dying_9',
                      'tiles/pac_man_dying_10', 'tiles/pac_man_dying_11']
point_path = "tiles/point.png"
gum_path = "tiles/gum.png"


# Fonction qui renvoie l'interpolation linéaire entre les points (x1, y1) et (x2, y2) selon d qui est entre 0 et 1,
# voir https://www.aquaportail.com/pictures2208/interpolation-lineaire.jpg
def lerp(x1, y1, x2, y2, d):
    x = x1 + ((x2 - x1) * d)
    y = y1 + ((y2 - y1) * d)
    return x, y


# Choisit le meilleur choix parmi les choix possibles
def chooseTheBest(set_):
    bestIndex = 0
    for i in range(len(set_)):
        if set_[i][2] < set_[bestIndex][2]:
            bestIndex = i
    return set_[bestIndex]


# Calcule la distance entre 2 points
def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Fonction qui porte un nom peut pertinent, en réalité la fonction calcul si une position est dans un ensemble et
# renvoie aussi si oui l'index dans l'ensemble
def isInSet(set_, cell):
    for i in range(len(set_)):
        c = set_[i]
        if c[0] == cell[0] and c[1] == cell[1]:
            return True, i
    return False, None


# Fonction qui renvoie l'ensemble des voisins valides d'une case
def neighbors(grid, cell, targetX, targetY):
    x, y, g = cell[0], cell[1], cell[3]
    res = []
    if y > 0:
        if grid[y - 1][x] != CaseState.OBSTACLE:
            res.append(
                (x, y - 1, dist(x, y - 1, targetX, targetY), g + 1, cell))
    if y < len(grid) - 1:
        if grid[y + 1][x] != CaseState.OBSTACLE:
            res.append(
                (x, y + 1, dist(x, y + 1, targetX, targetY), g + 1, cell))
    if x > 0:
        if grid[y][x - 1] != CaseState.OBSTACLE:
            res.append(
                (x - 1, y, dist(x - 1, y, targetX, targetY), g + 1, cell))
    if x < len(grid[0]) - 1:
        if grid[y][x + 1] != CaseState.OBSTACLE:
            res.append(
                (x + 1, y, dist(x + 1, y, targetX, targetY), g + 1, cell))
    return res


# Fonction qui permet de calculer le meilleur chemin pour aller d'un point à un autre
# Voir A* algorithm : https://en.wikipedia.org/wiki/A*_search_algorithm
def A_star(grid, x, y, targetX, targetY):
    # Termine l'algorithme si on est déjà à l'objectif
    if x == targetX and y == targetY:
        return x, y

    # Ensemble qui contient toutes les possibilités à étudier
    open_set = [(x, y, 0, 0, None)]
    # Ensemble qui contient toutes les possibilités qui ont déjà été étudiées
    closed_set = []

    # compteur d'itération pour éviter une éventuelle boucle infinie
    anti_freeze_counter = 0

    # Répéter tant qu'il reste des possibilités à traiter
    while len(open_set) > 0 and anti_freeze_counter < 50:
        # Choisit la case à traiter
        current = chooseTheBest(open_set)

        # Vérifie si on est arrivé
        if current[0] == targetX and current[1] == targetY:
            while current[4] is not None:
                if current[4][4] is None:
                    # Renvoie la position ou aller
                    return current[0], current[1]
                current = current[4]

        # Enregister current en tant que case traitée
        open_set.remove(current)
        closed_set.append(current)

        # Ajoute à l'open set tous les voisins de current
        for neighbor in neighbors(grid, current, targetX, targetY):
            if not isInSet(closed_set, neighbor)[0]:
                test = isInSet(open_set, neighbor)
                if test[0]:
                    if neighbor[3] < open_set[test[1]][3]:
                        open_set[test[1]] = neighbor
                else:
                    open_set.append(neighbor)
        anti_freeze_counter += 1

    return x, y


# Class qui modélise une entitée sur une grille
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

        self.actor.topright = (
            (xPos + 1) * self.deltaWidth, yPos * self.deltaHeight)

    # fonction de dessein de l'entité
    def draw(self, dt):
        self.actor.topright = lerp((self.prevXPos + 1) * self.deltaWidth, self.prevYPos * self.deltaHeight,
                                   (self.xPos + 1) * self.deltaWidth, self.yPos * self.deltaHeight, dt)
        self.actor.draw()


class PacMan(GridEntity):

    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        self.xSpeed = 0
        self.ySpeed = 0
        self.deathTime = -1
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
        if self.deathTime < 0:
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
        else:
            if self.deathTime < len(pac_man_dying_anim):
                self.actor.image = pac_man_dying_anim[self.deathTime]
            else:
                ...  # Game over
            if frame % 5 == 0:
                self.deathTime += 1

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


# Fantôme rouge
class Blinky(GridEntity):
    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        super().__init__(xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight)
        self.actor.image = blinky_right_0

    # met à jour l'image pour faire l'animation
    def updateImage(self, frame):
        right = blinky_right_0 if frame < 15 else blinky_right_1
        left = blinky_left_0 if frame < 15 else blinky_left_1
        down = blinky_down_0 if frame < 15 else blinky_down_1
        up = blinky_up_0 if frame < 15 else blinky_up_1

        if self.xPos - self.prevXPos > 0:
            self.actor.image = right
        elif self.xPos - self.prevXPos < 0:
            self.actor.image = left
        elif self.yPos - self.prevYPos > 0:
            self.actor.image = down
        elif self.yPos - self.prevYPos < 0:
            self.actor.image = up

    # Fonction qui permet à Blinky de traquer Pac Man
    def track(self, targetX, targetY, grid):
        self.prevXPos = self.xPos
        self.prevYPos = self.yPos
        self.xPos, self.yPos = A_star(
            grid, self.xPos, self.yPos, targetX, targetY)


# Fantôme orange
class Clyde(GridEntity):

    def __init__(self, xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight):
        super().__init__(xPos, yPos, screenWidth, screenHeight, gridWidth, gridHeight)
        self.actor.image = clyde_right_0

    # met à jour l'image pour faire l'animation
    def updateImage(self, frame):
        right = clyde_right_0 if frame < 15 else clyde_right_1
        left = clyde_left_0 if frame < 15 else clyde_left_1
        down = clyde_down_0 if frame < 15 else clyde_down_1
        up = clyde_up_0 if frame < 15 else clyde_up_1

        if self.xPos - self.prevXPos > 0:
            self.actor.image = right
        elif self.xPos - self.prevXPos < 0:
            self.actor.image = left
        elif self.yPos - self.prevYPos > 0:
            self.actor.image = down
        elif self.yPos - self.prevYPos < 0:
            self.actor.image = up

    # Fonction de déplacement de Clyde décrite dans README.md
    def move(self, grid, pac_man_xPos, pac_man_yPos):
        self.prevXPos = self.xPos
        self.prevYPos = self.yPos
        if self.xPos != 2 and self.yPos != 2 and dist(self.xPos, self.yPos, pac_man_xPos, pac_man_yPos) < 7:
            self.xPos, self.yPos = A_star(grid, self.xPos, self.yPos, 2, 2)
        else:
            pos1 = (self.xPos + 1, self.yPos) if self.xPos < len(grid[0]) - 1 and grid[self.yPos][
                self.xPos + 1] != CaseState.OBSTACLE else None
            pos2 = (self.xPos - 1, self.yPos) if self.xPos > 0 and grid[self.yPos][
                self.xPos - 1] != CaseState.OBSTACLE else None
            pos3 = (self.xPos, self.yPos - 1) if self.yPos > 0 and grid[self.yPos - 1][
                self.xPos] != CaseState.OBSTACLE else None
            pos4 = (self.xPos, self.yPos + 1) if self.yPos < len(grid) - 1 and grid[self.yPos + 1][
                self.xPos] != CaseState.OBSTACLE else None

            possibilities = []

            if pos1 is not None:
                possibilities.append(pos1)
            if pos2 is not None:
                possibilities.append(pos2)
            if pos3 is not None:
                possibilities.append(pos3)
            if pos4 is not None:
                possibilities.append(pos4)

            v = random.randint(0, len(possibilities) - 1)
            self.xPos, self.yPos = possibilities[v]
