#Joshua Byron
import pygame
from myvector import *
from ASTAR import *

class Enemy(object):
    def __init__(self, x, y, animations, health = 100, movementSpeed = 5):
        self.position = MyVector(x,y)
        #position is the tile row & col
        self.animations = animations
        self.health = health
        self.movementSpeed = movementSpeed
        self.destination = self.position
        #desitination is the tile row & col
        self.path = []
        self.increment = 0
        self.direction = MyVector(0,0)
        self.end = self.position
        self.goal = self.end
        
    def update(self, deltaTime, playerPos):
        self.animations.update(deltaTime)
        self.position += self.direction*self.movementSpeed*deltaTime
        #self.position = self.end

    def draw(self, window, offsetX, offsetY):
        window.blit(self.animations.getSurf(), self.position-MyVector(offsetX, offsetY))

    def findPath(self, start, goal, tileMap):
        self.goal = goal
        #path finding
        #tileMap 0 = good to move, 1 = wall. MUST be a nmap.array
        #start are the center of the tile they are in
        return astar(tileMap, start, goal)
        #returns a list of tuples (x, y) positions on the passed in nmap.array
