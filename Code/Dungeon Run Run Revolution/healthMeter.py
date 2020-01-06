#Joshua Byron Running Meter
import pygame
from Animation import *

class HealthMet(object):
    def __init__(self, startX, startY, health, filenameBack=None, filenameFront=None, anime = False):
        """can take in either an image or a rectangle"""
        self.x = startX
        self.y = startY
        self.Anime = anime
        self.health = health
        self.dam = 0.0
                
        if(self.Anime == False):
            self.background = pygame.image.load(filenameBack + ".png")
            self.foreground = pygame.image.load(filenameFront + ".png")
            self.background.convert_alpha()
            self.foreground.convert_alpha()
            self.widthBack = self.background.get_width()
            self.heightBack = self.background.get_height()
            self.widthFront = self.foreground.get_width()
            self.heightFront = self.foreground.get_height()
        else:
            backSpriteSheet = pygame.image.load(filenameBack + ".png")
            frontSpriteSheet = pygame.image.load(filenameFront + ".png")
            self.background = Animation(5, backSpriteSheet, 0.1)
            self.foreground = Animation(2, frontSpriteSheet, 1)
            self.widthBack = backSpriteSheet.get_width()/5
            self.heightBack = backSpriteSheet.get_height()
            self.widthFront = frontSpriteSheet.get_width()/2
            self.heightFront = frontSpriteSheet.get_height()

        self.diffX = self.widthBack - self.widthFront
        self.diffY = self.heightBack - self.heightFront
        self.percentageFull = 1
        
    def update(self, deltaTime):
        if(self.Anime == True):
            self.foreground.update(deltaTime)
            self.background.update(deltaTime)

    def damage(self, ammount):
        self.dam+=ammount
        #self.dam = min(self.health, self.dam)
        self.percentageFull = (self.health-self.dam) / self.health

    def drawHealthMet(self, window):
        if(self.Anime == True):
            window.blit(self.foreground.getSurf(), (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.percentageFull), self.heightFront))
            window.blit(self.background.getSurf(), (self.x, self.y))
        else:
            window.blit(self.foreground, (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.percentageFull), self.heightFront))
            window.blit(self.background, (self.x, self.y))





        
            
