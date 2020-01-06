#Joshua Byron
import pygame
from myvector import *
from enemy import *
from projectile import *

from Objects2D import *

class meele(Enemy):
    def __init__(self, x, y, animations, rechargeTime, damage, attackRange, drops, health = 100, movementSpeed = 5):
        Enemy.__init__(self, x, y, animations, health, movementSpeed)
        self.drops = drops
        
        self.timeSinceLastAttack = rechargeTime+10
        self.rechargeTime = rechargeTime
        self.maxHealth = health
        self.damage = damage
        self.attackRange = attackRange

        #self.timer = 20.0
        #self.ASTAR = 1
        self.inRange = False
        self.hasHit = False
        
        c = self.animations.getSurf()
        self.cube = Cuboid(MyVector(0,0,0), self.position, MyVector(c.get_width()*2, c.get_height()*2))
        
    def update(self, deltaTime, enemyCuboid, damage, enemyAttack):
        c = self.animations.getSurf()
        self.cube.mPos = self.position
        self.cube.changeDim(MyVector(c.get_width(), c.get_height()))
        
        if(self.health <= 0):
            return self.position
        else:
            if(self.hasHit == False):
                if(enemyAttack == True):
                    c = self.animations.getSurf()
                    self.cube = Cuboid(MyVector(0,0,0), self.position, MyVector(c.get_width(), c.get_height()))
                    if(collides(enemyCuboid, self.cube)):
                        self.health-=damage
                        print(self.health, "meelee!")
                    
            enemyPos = enemyCuboid.mPos
            
            self.timeSinceLastAttack+=deltaTime

            dist = (enemyPos - self.position).magnitude
            self.direction = (enemyPos - self.position).normalized
            
            if(enemyPos.x < self.position.x):
                if(self.animations.metaAnime != 0 and self.inRange == False):
                    self.animations.metaAnime = 0
                if(self.animations.metaAnime != 2 and self.inRange == True and self.timeSinceLastAttack >= self.rechargeTime and self.animations.attack == False and self.hasHit == False):
                    self.animations.metaAnime = 2
                    self.animations.attack = True

            if(enemyPos.x >= self.position.x):
                if(self.animations.metaAnime != 1 and self.inRange == False):
                    self.animations.metaAnime = 1
                if(self.animations.metaAnime != 2 and self.inRange == True and self.timeSinceLastAttack >= self.rechargeTime and self.animations.attack == False and self.hasHit == False):
                    self.animations.metaAnime = 2
                    self.animations.attack = True
                
            if(dist <= self.attackRange):
                self.inRange = True

            if(dist > self.attackRange):
                self.inRange = False

            Enemy.update(self, deltaTime, enemyPos)
            return None
    
    def draw(self, window, offsetX, offsetY):
        Enemy.draw(self, window, offsetX, offsetY)
        #self.cube.drawPygame(window, offsetX, offsetY)
        if(self.health >0):
            pygame.draw.rect(window, (255,0,0),(self.position.x-offsetX,self.position.y-15-offsetY, self.animations.getSurf().get_width() * (self.health/self.maxHealth), 10))
