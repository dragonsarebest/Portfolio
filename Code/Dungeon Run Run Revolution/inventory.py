#Joshua Byron
import pygame

class Inventory(object):
    def __init__(self, x, y, numSlots, backgroundImageFileName):
        self.x = x
        self.y = y
        self.numSlots = numSlots
        self.selected = 0
        self.backgroundImageFileName = backgroundImageFileName

        self.back = pygame.image.load("./Sprites/"+ self.backgroundImageFileName + ".png")
        self.number = []
        self.backpack = []
        for i in range(0, self.numSlots):
            self.number.append(-1)
            self.backpack.append(-1)
        self.totalWeight = 0

    def throwSelected(self):
        pass

    def setSelected(self, increment):
        self.selected += increment
        if(self.selected >= self.numSlots):
            self.selected = 0
        if(self.selected < 0):
            self.selected = self.numSlots

    def addItem(self, item):
        if(item.stackable == False):
            pass

    def drawInventory(self, window):
        pass

class inventoryItem(object):
    def __init__(self, fileName, slotNumber, weight, number, stackable = False):
        self.fileName = fileName
        self.image = pygame.image.load("./Sprites/"+fileName+".png")
        self.slotNumber = slotNumber
        self.weight = weight
        self.number = number
        self.stackable = stackable

    def drawItem(self, x, y, window):
        window.blit(self.image, (x,y))





