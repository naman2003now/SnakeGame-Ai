
import pygame
from pygame.locals import *
import numpy as np
import time
import random
import sys

# Colours
SnakeColor = (250, 250, 255)
BGColor = (50, 50, 50)
FoodColor = (255, 60, 60)

# pyGame Init
windowHeight, windowWidth = 600, 600
window = pygame.display.set_mode((windowHeight, windowWidth))
pygame.display.set_caption("SnakeGame")


def drawRect(Color, Coord):  # Draw Function
    xCoord = Coord[0] * 20
    yCoord = Coord[1] * 20
    pygame.draw.rect(window, Color, (yCoord, xCoord, 20, 20))


class Snake:
    def __init__(self):
        self.array = np.zeros((30, 30))
        self.head = (14, 14)
        self.food = (14, 25)
        self.tail = [(14, 14), (14, 13), (14, 12), (14, 11)]
        self.moving = {
            "Left": False,
            "Right": True,
            "Up": False,
            "Down": False
        }

    # Rendering
    def showFood(self):
        drawRect(FoodColor, self.food)

    def showSnake(self):
        for pos in self.tail:
            drawRect(SnakeColor, pos)

    def showFrame(self):
        window.fill(BGColor)
        self.showFood()
        self.showSnake()
        pygame.display.update()

    # PathFinding
    def getArray(self):
        self.array = np.zeros((30, 30))
        for pos in self.tail:
            self.array[pos] = 1;
        return self.array

    # Movement
    def moveLeft(self):
        self.head = (self.head[0], self.head[1] - 1)
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()
        self.showFrame()

    def moveRight(self):
        self.head = (self.head[0], self.head[1] + 1)
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()
        self.showFrame()

    def moveUp(self):
        self.head = (self.head[0] - 1, self.head[1])
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()
        self.showFrame()

    def moveDown(self):
        self.head = (self.head[0] + 1, self.head[1])
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()
        self.showFrame()

    # Game Essentials
    def foodEaten(self):
        if self.head == self.food:
            self.tail.append((self.tail[-1][0], self.tail[-1][1]))
            self.getFood()

    def checkDeath(self):
        if not 0 <= self.head[0] < 30 or not 0 <= self.head[1] < 30:
            return True
        for i in range(1, len(self.tail)):
            if self.tail[i] == self.head:
                return True
        return False

    def getFood(self):
        available = []
        self.getArray()
        for x in range(30):
            for y in range(30):
                if self.array[(x, y)] == 0:
                    available.append((x, y))

        random.shuffle(available)
        self.food = available[0]

    # Taking Input
    def move(self, direction):
        self.moving["Left"] = False
        self.moving["Right"] = False
        self.moving["Up"] = False
        self.moving["Down"] = False
        self.moving[direction] = True


def ShowText():
    for line in open("HighScore.txt", "r"):
        highScore = int(line)
    score = len(snake.tail)
    menu = "Your score: " + str(score) + "    Best: " + str(highScore)
    if score > highScore:
        open("HighScore.txt", "w+").write(str(score))
    window.fill(BGColor)
    pygame.font.init()
    font = pygame.font.SysFont('comicsansms', 32)
    text = font.render(menu, True, BGColor, FoodColor)
    textRect = text.get_rect()
    textRect.center = (600 // 2, 600 // 2)
    window.blit(text, textRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


snake = Snake()
while True:
    time.sleep(0.05)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_w:
                if not snake.moving["Down"]:
                    snake.moveUp()
                    snake.move("Up")
            elif event.key == pygame.K_s:
                if not snake.moving["Up"]:
                    snake.moveDown()
                    snake.move("Down")
            elif event.key == pygame.K_a:
                if not snake.moving["Right"]:
                    snake.moveLeft()
                    snake.move("Left")
            elif event.key == pygame.K_d:
                if not snake.moving["Left"]:
                    snake.moveRight()
                    snake.move("Right")
    time.sleep(0.05)
    if snake.checkDeath():
        time.sleep(1.5)
        ShowText()
    if snake.moving["Right"]:
        snake.moveRight()
    if snake.moving["Left"]:
        snake.moveLeft()
    if snake.moving["Up"]:
        snake.moveUp()
    if snake.moving["Down"]:
        snake.moveDown()
