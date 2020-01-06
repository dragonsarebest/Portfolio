#Joshua Byron
import pygame

class Animation:
    """this is the animation class"""
    def __init__(self, numFrames, spriteSheet, speed = 0.1):
        """creates the aniamtion with a position and sprtesheets"""
        self.animation = []
        self.numFrames = numFrames
        self.frameNumber = 0
        if(spriteSheet!=None):
            width = spriteSheet.get_width()/self.numFrames
            height = spriteSheet.get_height()
            #assumes the spritesheets are one straight line
            for j in range(0, numFrames):
                temp = pygame.Surface((width, height),pygame.SRCALPHA,32)
                temp.blit(spriteSheet, (0,0), (j*width, 0*height, width, height))
                self.animation.append(temp)
                #breaks up a spritesheet into individual sprites and palces them into item
            #adds the list of sprites to the list of animations
            self.currentFrame = self.animation[self.frameNumber]
            #animation info
        #metaAnime is the index for numFrames and spriteSheets
        self.animationTime = 0.0
        self.animationSpeed = speed
        self.animate = True
        self.isDone = False

    def createThrough(animations, numFrames, speed = 0.1):
        anime = Animation(numFrames, None, speed)
        anime.animation = animations
        anime.numFrames = numFrames
        anime.currentFrame = anime.animation[anime.frameNumber]
        return anime

    def update(self, deltaTime):
        """advances the animationFrame"""
        self.animationTime += deltaTime
        if (self.animationTime >= self.animationSpeed):
            self.frameNumber = (self.frameNumber + 1) % self.numFrames
            #resets the frame back to begining if the aniamtion length >= spritesheet length
            self.animationTime = 0.0
            self.currentFrame = self.animation[self.frameNumber]

    def getSurf(self):
        """returns the current frame"""
        return self.currentFrame
        
