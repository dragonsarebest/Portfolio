import pygame
pygame.init()
class Item(object):
    def __init__(self, filename, slotNum, weight):
        self.name = filename
        self.image = pygame.image.load("./Sprites/" + filename + ".png")
        self.slotNum = slotNum
        self.weight = weight


class Sword(Item):
    def __init__(self):
        pass


class Inventory(object):
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = item

    def print_items(self):
        print('\t'.join(['Name', 'Atk', 'Arm', 'Lb', 'Hp']))
        for item in self.items.values():
            print('\t'.join([str(x) for x in [item.name, item.slotNum, item.weight]]))
    def draw_inventory(self,screen):
        pygame.draw.rect(screen, (255, 0, 0), (500, 0, 400, 50))
        for item in self.items.values():
            print('\t'.join([str(x) for x in [item.name, item.slotNum, item.weight]]))
            screen.blit(item.image, (500,5))

# inventory = Inventory()
# inventory.add_item(Item('Sword', 5, 1, 15, 0))
# inventory.add_item(Item('Armor', 0, 10, 25, 0))
# inventory.add_item(Item('Potion', 0, 0, 5, 5))
# inventory.draw_inventory(screen)
# inventory.print_items()