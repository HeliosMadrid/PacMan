import random
from enum import Enum

#Fonction qui renvoie l'interpolation linéaire entre les points (x1, y1) et (x2, y2) selon d qui est entre 0 et 1, voir https://www.aquaportail.com/pictures2208/interpolation-lineaire.jpg
def lerp(x1, y1, x2, y2, d):
    x = x1 + ((x2 - x1) * d)
    y = y1 + ((y2 - y1) * d)
    return x, y

#Class modélisant une entité sur une grille
class GridEntity:
    #fonction d'initialisation, definissant la position de départ ainsi que l'acteur
    def __init__(self, xPos, yPos, width, gridWidth):
        self.xSpeed = 0
        self.ySpeed = 0
        self.xPos = xPos
        self.yPos = yPos
        self.prevXPos = xPos
        self.prevYPos = yPos
        self.actor = Actor(pac_man_right_0)

        deltaWidth = (width / gridWidth)
        self.actor.topright = ((xPos + 1) * deltaWidth, yPos * deltaWidth)
    
    #fonction de dessein de l'entité 
    def draw(self, dt):
        self.actor.topright = lerp((self.prevXPos + 1) * (WIDTH / 30), self.prevYPos * (WIDTH / 30),
                                   (self.xPos + 1) * (WIDTH / 30), self.yPos * (WIDTH / 30), dt)
        self.actor.draw()
    
    #met à jour le vecteur de déplacement
    def up(self):
        if self.yPos < len(grid) - 1 and grid[self.yPos - 1][self.xPos] != CaseState.OBSTACLE:
            self.xSpeed = 0
            self.ySpeed = -1
    
    #met à jour le vecteur de déplacement
    def down(self):
        if self.yPos > 0 and grid[self.yPos + 1][self.xPos] != CaseState.OBSTACLE:
            self.xSpeed = 0
            self.ySpeed = 1
    
    #met à jour le vecteur de déplacement
    def right(self):
        if self.xPos < len(grid[0]) - 1 and grid[self.yPos][self.xPos + 1] != CaseState.OBSTACLE:
            self.xSpeed = 1
            self.ySpeed = 0
    
    #met à jour le vecteur de déplacement
    def left(self):
        if self.xPos > 0 and grid[self.yPos][self.xPos - 1] != CaseState.OBSTACLE:
            self.xSpeed = -1
            self.ySpeed = 0

    #met à jour l'image pour faire l'animation
    def updateImage(self):
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

    #Fonction update qui ramasse les points
    def update(self):
        global points, grid
        if grid[self.yPos][self.xPos] == CaseState.POINT:
            points += 1
            grid[self.yPos][self.xPos] = CaseState.VOID
        elif grid[self.yPos][self.xPos] == CaseState.GUM:
            points += 5
            grid[self.yPos][self.xPos] = CaseState.VOID

    #fonction déplacement qui met à jour la position et gère les collisions
    def move(self):
        newX = self.xPos + self.xSpeed
        newY = self.yPos + self.ySpeed

        self.prevXPos = self.xPos
        self.prevYPos = self.yPos
        if 0 < newX < len(grid[0]) and 0 < newY < len(grid):
            if grid[newY][newX] != CaseState.OBSTACLE:
                self.xPos = newX
                self.yPos = newY


#banque d'image
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
# top_left_corner_path = "tiles/top_left_corner.png"
# top_right_corner_path = "tiles/top_right_corner.png"
# bottom_right_corner_path = "tiles/bottom_right_corner.png"
# bottom_left_corner_path = "tiles/bottom_left_corner.png"
# vertical_right_path = "tiles/vertical_right.png"
# vertical_left_path = "tiles/vertical_left.png"
# horizontal_top_path = "tiles/horizontal_top.png"
# horizontal_bottom_path = "tiles/horizontal_bottom.png"


#Enumeration des valeurs possible pour chaque point de la grille
class CaseState(Enum):
    VOID = 0
    POINT = 1
    OBSTACLE = 2
    GUM = 3


WIDTH = 480
HEIGHT = 480

#fréquence à laquelle les personnages sont update(move), 30 équivaut à 2 fois par seconde
frame_rate = 30
#variable qui compte les frames, et retourne à 0 toutes les 30 frames
frame = 0
#valeur indiquant à quelle distance est on de la prochaine update, entre 0 et 1
deltaTime = 0

#objet encapsulant pac man
pac_man = GridEntity(13, 12, WIDTH, 30)
#compteur de points
points = 0

#variable contenant la map
grid = []

#fonction qui charge la variable grid à partir du fichier map/level1.map
def loadGrid():
    with open('map/level1.map', 'r') as levelFile:
        for line in levelFile:
            row = []
            for c in line:
                if c == '.':
                    #1 chance sur 50 que la case soit un super gum sinon c'est un point
                    if random.randint(0, 50) == 0:
                        row.append(CaseState.GUM)
                    else:
                        row.append(CaseState.POINT)
                elif c == 'x':
                    row.append(CaseState.OBSTACLE)
            grid.append(row)


def update():
    global frame, deltaTime

    #charge la grid si elle n'est pas déjà chargée
    if not grid:
        loadGrid()

    #gère les inputs du joueur
    if keyboard.UP:
        pac_man.up()
    if keyboard.DOWN:
        pac_man.down()
    if keyboard.RIGHT:
        pac_man.right()
    if keyboard.LEFT:
        pac_man.left()

    #actualise l'animation
    pac_man.updateImage()

    #actualise la logique du jeu
    if frame % frame_rate == 0:
        pac_man.update()
        pac_man.move()
        frame = 0

    #calcul delta time
    deltaTime = (frame % frame_rate) / frame_rate
    #augmente frame de 1
    frame += 1


#fonction qui dessine la grid, juste en affichant des carrés bleus ou noir ou des points ou des gums
def drawGrid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == CaseState.OBSTACLE:
                screen.draw.filled_rect(Rect((x * (WIDTH / 30), y * (WIDTH / 30)), (16, 16)), (33, 33, 255))
            elif grid[y][x] == CaseState.POINT:
                screen.blit(point_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
            elif grid[y][x] == CaseState.GUM:
                screen.blit(gum_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # up = grid[y - 1][x] == CaseState.OBSTACLE if y > 0 else False
                # down = grid[y + 1][x] == CaseState.OBSTACLE if y < len(grid) - 1 else False
                # right = grid[y][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 else False
                # left = grid[y][x - 1] == CaseState.OBSTACLE if x > 0 else False
                # up_right = grid[y - 1][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 and y > 0 else False
                # up_left = grid[y - 1][x - 1] == CaseState.OBSTACLE if x < 0 and y > 0 else False
                # down_right = grid[y + 1][x + 1] == CaseState.OBSTACLE if x < len(grid[0]) - 1 and y < len(grid) - 1 else False
                # down_left = grid[y + 1][x - 1] == CaseState.OBSTACLE if x > 0 and y < len(grid) - 1 else False
                #
                # if down and right and ((not up and not left) or down_right):
                #     screen.blit(top_left_corner_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif left and down and ((not up and not right) or down_left):
                #     screen.blit(top_right_corner_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif left and up and ((not down and not right) or up_left):
                #     screen.blit(bottom_right_corner_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif up and right and ((not left and not down) or up_right):
                #     screen.blit(bottom_left_corner_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif up and down and left and not right:
                #     screen.blit(vertical_right_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif up and down and right and not left:
                #     screen.blit(vertical_left_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif left and right and up and not down:
                #     screen.blit(horizontal_bottom_path, (x * (WIDTH / 30), y * (WIDTH / 30)))
                # elif left and right and down and not up:
                #     screen.blit(horizontal_top_path, (x * (WIDTH / 30), y * (WIDTH / 30)))


#fonction de dessin
def draw():
    screen.clear()
    screen.fill('black')

    drawGrid()
    #dessine pas man
    pac_man.draw(deltaTime)
