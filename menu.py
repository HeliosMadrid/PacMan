import pgzrun
from pgzero.keyboard import keyboard

import subprocess
import sys

from Entity import *


class Menu:
    def __init__(self):
        self.buttons = []
        self.title = "pac_man_title"
        self.window_width = 720
        self.window_height = 480

    def create_button(self, xpos, ypos, image, callback_function):
        button = Actor(image)
        button.topright = xpos, ypos
        self.buttons.append((button, callback_function))
        return button

    def add_button(self, button, callback_function):
        self.buttons.append((button, callback_function))

    def draw(self):
        # dessin de tous les boutons
        for button in self.buttons:
            button[0].draw()

        # dessin du tire
        screen.blit(self.title, (300,
                                 self.window_height/3))


menu = Menu()

# fonction pour lancer la fenêtre du pac_man


def launch_game():
    subprocess.run("python PacMan.py")


button_solo = menu.create_button(
    menu.window_width/2+55, menu.window_height*(2/3), 'play_button', launch_game)


def on_mouse_down(pos, button):
    if button_solo.collidepoint(pos):
        menu.buttons[0][1]()


on_button = False


def on_mouse_move(pos):
    global on_button
    on_button = bool(button_solo.collidepoint(pos))


def draw():
    screen.clear()
    menu.draw()
    if on_button:
        screen.draw.circle(
            (menu.window_width/2-10, menu.window_height*(2/3)+8), 5, (200, 200, 0))


pgzrun.go()
