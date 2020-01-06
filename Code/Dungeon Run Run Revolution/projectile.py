#Joshua Byron
from myvector import *
import pygame

class projectile(object):
    def __init__(self, x, y, direction, speed, damage, animations):
        self.position = MyVector(x,y)
        self.direction = direction.normalized
        self.speed = speed
        self.animations = animations
        self.damage = damage

    def draw(self, window, offsetX, offsetY):
        window.blit(self.animations.getSurf(), (self.position- MyVector(offsetX, offsetY)))

    def update(self, deltaTime):
        self.position += self.direction * self.speed * deltaTime
        self.animations.update(deltaTime)
