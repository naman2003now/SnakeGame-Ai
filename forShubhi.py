

import pygame
from pygame.locals import *
import sys
from time import sleep

#bpVariables
direction = "L"
change = True

# Colours
SnakeColor = (250, 250, 255)
BGColor = (50, 50, 50)
FoodColor = (255, 60, 60)

#Global bp Variables
windowHeight, windowWidth = 600, 600
gridHeight, gridWidth = 20, 20

# pyGame Init
window = pygame.display.set_mode((windowHeight, windowWidth))
pygame.display.set_caption("SnakeGame")

def drawRect(Color, Coord):  # Draw Function
    xCoord = Coord[0] * gridHeight
    yCoord = Coord[1] * gridWidth
    pygame.draw.rect(window, Color, (yCoord, xCoord, 20, 20))

def refreshScreen():
    window.fill(BGColor)

def gameLoop():
    sleep(0.1)
    refreshScreen()
    global direction

    drawRect(SnakeColor, (10, 10))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_w and change:
                if not direction == "D":
                    change = False
                    direction = "U"
            if event.key == pygame.K_s and change:
                if not direction == "U":
                    change = False
                    direction = "D"
            if event.key == pygame.K_a and change:
                if not direction == "R":
                    change = False
                    direction = "L"
            if event.key == pygame.K_d and change:
                if not direction == "L":
                    change = False
                    direction = "R"
    gameLoop()
    pygame.display.update()
