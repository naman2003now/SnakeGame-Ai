from typing import Type

import pygame
from pygame.locals import *
import numpy as np
import time
import random
import sys
import queue

# Colours
SnakeColor = (250, 250, 255)
BGColor = (50, 50, 50)
FoodColor = (255, 60, 60)

# pyGame Init
windowHeight, windowWidth = 600, 600
window = pygame.display.set_mode((windowHeight, windowWidth))
pygame.display.set_caption("SnakeGame")


def drawRect(Colour, Coord):  # Draw Function
    xCoord = Coord[0] * 20
    yCoord = Coord[1] * 20
    pygame.draw.rect(window, Colour, (yCoord, xCoord, 20, 20))


class Path:
    def __init__(self):
        self.currentPath = ""
        self.map = snake.getArray()
        self.pathQueue = queue.Queue()
        self.end = snake.food
        self.start = snake.head
        self.notations = {
            "R": "Right",
            "L": "Left",
            "U": "Up",
            "D": "Down"
        }

    def findPath(self):
        self.checkNeighbours("")
        while True:
            self.currentPath = self.pathQueue.get()
            self.checkNeighbours(self.currentPath)
            if self.trackPath(self.currentPath, self.start) == self.end:
                return self.notations[self.currentPath[0]]
            if self.pathQueue.empty():
                self.map = snake.getArray()
                self.checkNeighbours("")
                return self.notations[self.pathQueue.get()]

    def checkNeighbours(self, path):
        for direction, _ in self.notations.items():
            tempPath = path
            tempPath += direction
            currentPoint = self.trackPath(tempPath, self.start)
            if 0 <= currentPoint[0] < 30 and 0 <= currentPoint[1] < 30:
                if self.map[currentPoint] == 0:
                    self.pathQueue.put(tempPath)
                    self.map[currentPoint] = 1


    def trackPath(self, path, point):
        for char in path:
            if char == "R":
                point = (point[0], point[1] + 1)
            if char == "L":
                point = (point[0], point[1] - 1)
            if char == "U":
                point = (point[0] - 1, point[1])
            if char == "D":
                point = (point[0] + 1, point[1])

        return point


class Snake:
    def __init__(self):
        self.array = np.zeros((30, 30))
        self.head = (14, 14)
        self.tail = [(14, 14), (14, 13), (14, 12), (14, 11)]
        self.getFood()
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

    def moveRight(self):
        self.head = (self.head[0], self.head[1] + 1)
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()

    def moveUp(self):
        self.head = (self.head[0] - 1, self.head[1])
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()

    def moveDown(self):
        self.head = (self.head[0] + 1, self.head[1])
        for i in range(1, len(self.tail)):
            self.tail[-i] = self.tail[-i - 1]
        self.tail[0] = self.head
        self.foodEaten()

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

    # Moving the snake
    def move(self, direction):
        self.moving["Left"] = False
        self.moving["Right"] = False
        self.moving["Up"] = False
        self.moving["Down"] = False
        self.moving[direction] = True


snake = Snake()
while True:
    start = time.time()
    path = Path()
    end = time.time()
    if not (end - start) > 0.1:
        time.sleep(0.1-(end-start))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if snake.checkDeath():
        snake = Snake()
    
    snake.move(path.findPath())
    if snake.moving["Right"]:
        snake.moveRight()
    if snake.moving["Left"]:
        snake.moveLeft()
    if snake.moving["Up"]:
        snake.moveUp()
    if snake.moving["Down"]:
        snake.moveDown()
    snake.showFrame()

