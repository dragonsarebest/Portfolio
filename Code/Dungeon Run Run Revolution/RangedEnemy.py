#Joshua Byron
import pygame
from myvector import *
from enemy import *
from projectile import *

from Animation import *
from Objects2D import *

class ranger(Enemy):
    def __init__(self, x, y, animations, projectileAnmations, reloadSpeed, projectileSpeed, damage, attackRange, drops, movementSpeed = 5, health = 100):
        Enemy.__init__(self, x, y, animations, health, movementSpeed)
        self.drops = drops
        self.timeSinceLastShot = reloadSpeed+10
        self.reloadSpeed = reloadSpeed
        self.projectileSpeed = projectileSpeed
        self.damage = damage
        self.attackRange = attackRange
        self.projectileAnmations = projectileAnmations

        self.arrows = []
        self.inRange = False
        self.hasHit = False
        self.maxHealth = health

        c = self.animations.getSurf()
        self.cube = Cuboid(MyVector(0,0,0), self.position, MyVector(c.get_width(), c.get_height()))
            
    def attack(self, goal):
        print("PEW!")
        dire = goal.x-self.position.x
        direct = goal - self.position
        #assumes theyre skelliton
        if(dire > 0):
            #animations, numFrames, speed = 0.1
            anime = Animation.createThrough(self.projectileAnmations.animations[1], 6)
        else:
            anime = Animation.createThrough(self.projectileAnmations.animations[0], 6)
        self.arrows.append(projectile(self.position.x, self.position.y, direct, self.projectileSpeed, self.damage, anime))
        
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
                        print(self.health)

            enemyPos = enemyCuboid.mPos
            self.timeSinceLastShot+=deltaTime
            dist = (enemyPos - self.position).magnitude
            self.direction = (enemyPos - self.position).normalized

            if(enemyPos.x < self.position.x):
                if(self.animations.metaAnime != 0 and self.inRange == False):
                    self.animations.metaAnime = 0
                #if(self.animations.metaAnime != 2 and self.inRange == True):
                #    self.animations.metaAnime = 2
                #never made this animation
            if(enemyPos.x >= self.position.x):
                if(self.animations.metaAnime != 1 and self.inRange == False):
                    self.animations.metaAnime = 1
                #if(self.animations.metaAnime != 2 and self.inRange == True):
                #    self.animations.metaAnime = 2
            
            if(self.timeSinceLastShot >= self.reloadSpeed and dist <= self.attackRange):
                self.attack(enemyPos)
                self.inRange = True
                self.timeSinceLastShot = 0.0
                
            if(dist > self.attackRange):
                self.inRange = False
            
            for item in self.arrows:
                item.update(deltaTime)
                dist = (item.position - self.position).magnitude
                if(dist >= self.attackRange*2.5):
                    self.arrows.remove(item)
                
            Enemy.update(self, deltaTime, enemyPos)
            return None
    def draw(self, window, offsetX, offsetY):
        #self.cube.drawPygame(window, offsetX, offsetY)
        if(self.health > 0):
            for item in self.arrows:
                item.draw(window, offsetX, offsetY)
            pygame.draw.rect(window, (255,0,0),(self.position.x-offsetX,self.position.y-15-offsetY, self.animations.getSurf().get_width() * (self.health/self.maxHealth), 10))
        Enemy.draw(self, window, offsetX, offsetY)
        
