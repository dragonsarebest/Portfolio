#Joshua Byron Running Meter
import pygame
from Animation import *

class RunMet(object):
    def __init__(self, startX, startY, widthBack, heightBack, widthFront, heightFront, colorBack, colorFront, fontFilename, fontColor, resetTime = 5.0, increment = 0.3, image = False,
                 filenameBack=None, filenameFront=None, anime = False):
        """can take in either an image or a rectangle"""
        self.x = startX
        self.y = startY
        self.isImage = image
        self.fontFilename = fontFilename
        self.fontColor = fontColor
        self.Anime = anime
                
        if(self.isImage == False):
            self.widthBack = widthBack
            self.heightBack = heightBack
            self.widthFront = widthFront
            self.heightFront = heightFront
            self.colorBack = colorBack
            self.colorFront = colorFront
            self.background = pygame.Surface((self.widthBack, self.heightBack))
            self.foreground = pygame.Surface((self.widthFront, self.heightFront))
            self.background.fill(self.colorBack)
            self.foreground.fill(self.colorFront)
        elif(self.isImage == True and self.Anime == False):
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
        
        #1 font point = 16pixels
        self.fontSize = self.heightBack
        self.font = pygame.font.SysFont(self.fontFilename, self.fontSize)
        
        self.percentageFull = 0.001
        self.runStreak = 0

        self.timeSinceLastMoving = 0.0
        self.timeMoving = 0.0
        self.resetTime = resetTime
        #how long the player can stand still before losing his meter
        self.increment = increment
        #base of how much the player's run-meter increases each time
        self.decrease = 0.0
        #show the meter running out instead of just cutting back to 0 percent
        self.isStopped = False
        
    def update(self, deltaTime, moving):
        if(self.Anime == True):
            self.foreground.update(deltaTime)
            self.background.update(deltaTime)
        if(moving == False):
            self.timeMoving = 0.0
            self.timeSinceLastMoving += deltaTime
            #only add to this if the player isnt moving
            if(self.timeSinceLastMoving >= self.resetTime and self.isStopped == False):
                print("player stoped for " + str(self.timeSinceLastMoving) + " seconds!")
                self.decrease = self.percentageFull
                self.percentageFull = 0.001
                self.isStopped = True
                #if the player is still too long set this to 0.001
        else:
            self.isStopped = False
            self.timeMoving += deltaTime
            self.timeSinceLastMoving = 0.0
            self.decrease = 0.0
            #set back to 0 if the player is moving
            self.percentageFull += self.increment/(self.runStreak+1)
            if(self.percentageFull >= 1.0):
                self.runStreak+=1
                self.increment/=1.4
                self.percentageFull = 0.001
                self.decrease = 1.0
        

    def drawRunMet(self, window):
        if(self.Anime == False):
            if(self.isImage == False and self.Anime == False):
                window.blit(self.background, (self.x, self.y))
                #using two rectangles instead of images
            if(self.decrease <= 0.0):
                #print("not decreasing")
                window.blit(self.foreground, (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.percentageFull), self.heightFront))
            else:
                window.blit(self.foreground, (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.decrease), self.heightFront))
                self.decrease -= self.increment
                self.decrease = max(0.0, self.decrease)
            if(self.isImage == True):
                window.blit(self.background, (self.x, self.y))
                #assumes background image contains transparencey
        else:
            if(self.decrease <= 0.0):
                window.blit(self.foreground.getSurf(), (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.percentageFull), self.heightFront))
            else:
                window.blit(self.foreground.getSurf(), (self.x+(self.diffX*0.5), self.y+(self.diffY*0.5)), (0,0, self.widthFront*(self.decrease), self.heightFront))
                self.decrease -= self.increment
                self.decrease = max(0.0, self.decrease)
            if(self.isImage == True):
                window.blit(self.background.getSurf(), (self.x, self.y))
        
        temp = self.font.render(str(self.runStreak), True, self.fontColor)
        window.blit(temp, (self.x + self.widthBack + self.diffX, self.y))