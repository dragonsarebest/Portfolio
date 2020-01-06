#Joshua Byron
import pygame

class Animations:
    """this is the animation class"""
    def __init__(self, numFrames, spriteSheets, followThrough, speed = 0.1):
        """creates the aniamtion with a position and sprtesheets"""
        self.animations = []
        self.numFrames = []
        self.followThrough = followThrough
        self.attack = False
        
        for frame in numFrames:
            self.numFrames.append(frame)

        print("This is the num frame of animation:::",self.numFrames)
        for i in range(0, len(spriteSheets)):
            item = []
            width = spriteSheets[i].get_width()/self.numFrames[i]
            height = spriteSheets[i].get_height()
            print("This is the width of animation:::",width)
            #assumes the spritesheets are one straight line
            for j in range(0, numFrames[i]):
                temp = pygame.Surface((width, height),pygame.SRCALPHA,32)
                temp.blit(spriteSheets[i], (0,0), (j*width, 0*height, width, height))
                item.append(temp)
                #breaks up a spritesheet into individual sprites and palces them into item
            self.animations.append(item)
            #adds the list of sprites to the list of animations

        #animation info
        self.metaAnime = 0
        self.frameNumber = 0
        #metaAnime is the index for numFrames and spriteSheets
        self.animationTime = 0.0
        self.currentFrame = self.animations[self.metaAnime][self.frameNumber]
        self.animationSpeed = speed
        self.animate = True


    def update(self, deltaTime):
        """advances the animationFrame"""
        self.animationTime += deltaTime
        if (self.animationTime >= self.animationSpeed):
            if(self.attack == True and (self.frameNumber + 1) % self.numFrames[self.metaAnime] == 0):
                self.attack = False
            if(self.followThrough[self.metaAnime] == -1):
                self.frameNumber = (self.frameNumber + 1) % self.numFrames[self.metaAnime]
                self.animationTime = 0.0
            else:
                self.frameNumber+=1
                if(self.frameNumber > self.numFrames[self.metaAnime]-1):
                    self.changeMeta(self.followThrough[self.metaAnime])
                else:
                    self.animationTime = 0.0
            #resets the frame back to begining if the aniamtion length >= spritesheet length
            self.currentFrame = self.animations[self.metaAnime][self.frameNumber]

    def getSurf(self):
        """returns the current frame"""
        return self.currentFrame

    def changeMeta(self, meta):
        self.metaAnime = meta
        self.frameNumber = 0
        
