#import the things you need here
import math
import random
import pygame

from .libraries.VectorMatrixLibrary import *
from .libraries.MiscFunctions import *

#40 unit diameter = tank
#10 unit diameter = bullet

#runs @ 60fps
#15 sec reload time b/w shots

#1000 x 1000
# 0 = right, 90 = up, 180 = left, 270 = down

global TANK_LIST 
TANK_LIST = {}
#key = tank name + house name, value = tank obj
global BULLET_LIST 
BULLET_LIST = []
#value = bullet obj

unit = 1
#1 unit = 1 pixel!

global TANK_SPEED
TANK_SPEED = 1*unit
#1 unit
global BULLET_SPEED
BULLET_SPEED = 8*unit
#8 * that of a tank

global BARRIERS
BARRIERS = []

global BULLET_RADIUS
BULLET_RADIUS = 5

global TANK_RADIUS
TANK_RADIUS = 20

global MAP_SIZE
MAP_SIZE = 1000

global MAP_CORNERS
MAP_CORNERS = [Vector2(0,0), Vector2(1000,0), Vector2(0, 1000), Vector2(1000,1000)]

global DENSITY
DENSITY = []

global NUM_ALIVE
NUM_ALIVE = 0

def getClosestTankName(yourPos, tankName = None):
	global TANK_LIST 
	closestT = math.inf
	closestTank = None
	for key in TANK_LIST:
		tank = TANK_LIST[key]
		if (tankName != None and tank.tankName == TANK_LIST[tankName].tankName):
			continue
		if(tank.alive == False):
			continue
		distance_squared = (yourPos - tank.pos).magnitudeSq
		if (distance_squared < closestT):
			closestT = distance_squared
			closestTank = key
	return closestTank

def canWeHit(tank1, tank2, foresight = False, closestBar = None):
	#tank2 = always a tank, tank1 = tank OR bullet, checking if they have vision on eachother/can hit eachother
	global BARRIERS, BULLET_SPEED, TANK_SPEED, VISION
	
	if(type(tank1) == Bullet):
		speed = BULLET_SPEED
	else:
		speed = TANK_SPEED
	
	if(tank2.health < 1):
		return [False, tank2.pos]
	
	newTargetPos = tank2.pos
	if(foresight):
		#target_position, target_velocity, projectile_speed
		canWeHitInTime = direct_solution(tank2.pos, tank2.direction, speed)
		if(canWeHitInTime == None):
			return [False, newTargetPos]
		else:
			newTargetPos = canWeHitInTime
	
	dir = (newTargetPos-tank1.pos).normalized
	distToTankDirectly = (newTargetPos-tank1.pos).magnitudeSq
	
	if(areTheseOpposingSides(tank1, tank2)):
		return [False, newTargetPos]
	return [True, newTargetPos]

def areTheseOpposingSides(tank1, tank2):
	#returns true if they're on opposite sides
	global BARRIERS
	barNum = getClosestBarrier(tank1)
	tempBar = BARRIERS[barNum]
	
	#if the two entities are on opposing sides of a barrier they CANNOT see eachother
	result1 = tempBar.getSide(tank1.pos)[1:]
	result2 = tempBar.getSide(tank2.pos)[1:]
	foundOpposite = False
	#LEFT RIGHT TOP BOTTOM
	for item in result1:
		for item2 in result2:
			if(item == "LEFT" and item2 == "RIGHT"):
				foundOpposite = True
				break
			if(item == "RIGHT" and item2 == "LEFT"):
				foundOpposite = True
				break
			if(item == "TOP" and item2 == "BOTTOM"):
				foundOpposite = True
				break
			if(item == "BOTTOM" and item2 == "TOP"):
				foundOpposite = True
				break
		if(foundOpposite):
			break
	return foundOpposite

class Tank(object):
	def __init__(self, name, house, x, y, health, score):
		global TANK_RADIUS		
		self.name = name
		self.house = house
		self.health = health
		self.oldHealth = health
		self.score = score
		self.pos = Vector2(x, y)
		self.previousPos = Vector2(x, y)

		self.direction = Vector2(0,0)
		self.alive = True
		self.shieldActive = False
		self.moving = False
		self.alternate = False
		self.dodgeAngle = 0
		self.ammountLeftToMove = 0
		self.startedDodging = False
		self.touching = False
		self.wasHit = False
		self.oldNumDangerBullets = 0
		self.clockWise = 1
		self.dodging = False
		self.currentClosestBarrier = 0
			
	@property
	def tankName(self):
		return self.name+self.house

	def draw(self, surf, isMySelf = False):
		if(self.alive == False):
			return 
		if(isMySelf):
			col = (255,255,255)
		else:
			col = (0,255,0)
		pygame.draw.circle(surf, col, self.pos.i, TANK_RADIUS)

	def update(self, x, y, health, score):
		global TANK_SPEED
		self.oldHealth = self.health
		self.health = health
		
		self.wasHit = False
		
		if((self.oldHealth - self.health) > 2):
			self.wasHit = True

		if(self.health <= 0):
			self.alive = False
			return
			
		self.alternate = not self.alternate
		
		self.score = score
		self.previousPos = self.pos
		self.pos = Vector2(x, y)
		
		self.direction = (self.pos - self.previousPos)
		self.ammountLeftToMove-=(self.direction.magnitude)
		self.direction = self.direction.normalized
		
		if(self.ammountLeftToMove <= 0):
			self.dodging = False
			
	def canSeeTank(self, tank2, foresight = False):
		#can these 2 tanks see eachother?
		return canWeHit(self, tank2, foresight)
		
	def canIShoot(self, tank2, foresight = True):
		#self.alternate
		if(foresight == True):
			foresight = self.alternate
		results = self.canSeeTank(tank2, foresight)
		#results = [tank2.health > 0, tank2.pos]
		return results
		
class Bullet(object):
	def __init__(self, x, y, closestTank = None):
		global TANK_LIST, BULLET_RADIUS
		self.pos = Vector2(x, y) #for some reason making a vector 2 here is what is causing the error!
		if(closestTank == None):
			self.mastersName = getClosestTankName(self.pos)
		else:
			self.mastersName = closestTank
		self.direction = (self.pos - TANK_LIST[self.mastersName].pos).normalized
		self.init = True
		self.expected = self.pos
	
	def draw(self, surf, name, isDanger = False):
		global BULLET_RADIUS
		if(self.mastersName == name):
			return
		color = (0,255,0)
		if(isDanger):
			color = (255, 0, 0)
		pygame.draw.circle(surf, color, self.pos.i, BULLET_RADIUS*2)
		drawArrow(surf, self.pos, self.pos+self.direction * 40)
	
	def update(self):
		self.pos = self.pos + self.direction * BULLET_SPEED
	
	def newPos(self, newPos):
		self.pos = newPos
	
	def expectedLocation(self, ticks = 1):
		global BULLET_SPEED, MAP_SIZE, BARRIERS
		pos = self.pos + self.direction * BULLET_SPEED * ticks
		
		if(pos.x <= 0 or pos.x >= MAP_SIZE):
			return [False, pos, -1]
			
		if(pos.y <= 0 or pos.y >= MAP_SIZE):
			return [False, pos, -1]
			
		didHit = False
		
		distToBoxyBoi = math.inf
		orthogonal = self.direction.perpendicular
		for hitBox in BARRIERS:
			"""results = hitBox.getDistanceToRay(pos, -1*self.direction)
			if((results[0] - pos).magnitudeSq <= BULLET_RADIUS or hitBox.pointInsideBox(pos)):
				didHit = True
				ourDist = (results[0] - self.pos).magnitudeSq
				if(ourDist < distToBoxyBoi):
					distToBoxyBoi = ourDist
			"""
			
			#looks if the ray hits dead on, or to the left & right by the bullet radius (since that estimates a circle
			didHit = (hitBox.rayBoxIntersection(self.pos, self.direction) or hitBox.rayBoxIntersection(self.pos+orthogonal*BULLET_RADIUS, self.direction) or hitBox.rayBoxIntersection(self.pos-orthogonal*BULLET_RADIUS, self.direction))
			if(didHit):
				break
		if(didHit):
			return [False, pos]
		return [True, pos]

def getClosestBarrier(myTank):
	closestBarrier = 0
	currentBar = 0
	closestBarrierDist = math.inf
	barrierDir = Vector2(1,0)
	touching = False
	for bar in BARRIERS:
		closest = bar.getSide(myTank.pos)[0]
		distToBarrier = (closest - myTank.pos)
		if(distToBarrier.isZero):
			closestBarrierDist = (myTank.pos - BARRIERS[closestBarrier].mPos).magnitudeSq
			closestBarrier = currentBar
			barrierDir = Vector2(0, 0)
			touching = True
			break
		dir = distToBarrier.normalized
		distToBarrier = distToBarrier.magnitudeSq
		if(distToBarrier < closestBarrierDist):
			closestBarrierDist = distToBarrier
			closestBarrier = currentBar
			barrierDir = dir
		currentBar += 1
	return closestBarrier

class Tank_AI(object):
	def __init__(self):
		global TANK_LIST, BULLET_LIST, BARRIERS
		self.name = "TankBattle-Inator"   #your bot name here
		self.house = "Witherell" #your house here: one of "Yost", "Witherell", "Lynn", "Skaggs"
		self.my_angle = 0
		self.fire_countdown = 0
		self.fire_countdown_total = 15
		self.hasFired = False
		
		TANK_LIST = {}
		BULLET_LIST = []
		BARRIERS = [Box(Vector2(200,300),Vector2(230,700)),Box(Vector2(800,300), Vector2(770,700)),Box(Vector2(400,200),Vector2(600,225)),Box(Vector2(400,775),Vector2(600,800))]
		
		self.initalize = True
		self.moveAngle = 0
		
		self.Fire = True
		self.Dodge = False
		self.Shield = False
		self.Move = False
		
		self.oldPos = None
		self.dupeNames = {}
		self.Shielding = False
		self.Shielding_countdown = 0
		self.Shielding_countdown_total = 2*60
		
		self.win = pygame.display.set_mode((1000, 1000))
		
	@property
	def tankName(self):
		return self.name+self.house
    
	def toDoBeforeReturn(self):
		for i in range(0, len(BULLET_LIST)):
			BULLET_LIST[i].update()
	
	def setup(self, tank_list_passed, bullet_list_passed):
		global TANK_LIST, BULLET_LIST, MAP_SIZE, DENSITY, NUM_ALIVE
		#tank_list_passed = [... tankName, tankHouse, x, y, health, score]
		#bullet_list_passed = [... x, y]
		DENSITY = [0,0,0,0]
		NUM_ALIVE = 0
		
		#update sheild & fire countdown
		if(self.hasFired):
			self.fire_countdown += 1
		if(self.fire_countdown >= self.fire_countdown_total):
			self.fire_countdown = 0
			self.hasFired = False
		
		if(self.Shielding):
			self.Shielding_countdown += 1
		if(self.Shielding_countdown >= self.Shielding_countdown_total):
			self.Shielding = False
			self.Shielding_countdown = 0
			TANK_LIST[self.tankName].shieldActive = False
		
		#update tank positions
		for i in range(0, len(tank_list_passed)):
			newTank = list(tank_list_passed[i])
			name = newTank[0]+newTank[1]
			name = self.duplicateName(name)
			if(self.initalize):
				#name, house, x, y, health, score
				TANK_LIST[name] = Tank(*newTank)
			else:
				TANK_LIST[name].update(*newTank[2:])
			
			if(TANK_LIST[name].alive == True):
				NUM_ALIVE += 1
			barNum = getClosestBarrier(TANK_LIST[name])
			TANK_LIST[name].currentClosestBarrier = barNum
			if(name != self.tankName):
				DENSITY[barNum] += 1
		
		myTank = TANK_LIST[self.tankName]
		matched_bullets = []
		
		for passedBull in bullet_list_passed:
			passedBullPos = Vector2(*passedBull)
			found = False
			indx = 0
			currentIndex = 0
			closestDist = math.inf
			closestBullet = None
			for currentBull in BULLET_LIST:
				tDist = (passedBullPos - currentBull.pos).magnitudeSq
				if(tDist < closestDist):
					if(tDist < (BULLET_RADIUS*2)**2):
						closestDist = tDist
						closestBullet = currentBull
						currentIndex = indx
						found = True
				indx += 1
			if(found):
				BULLET_LIST = BULLET_LIST[currentIndex+1:]
				#remove all bullets before this since this should maintain relative order, so these MUST be dead
				closestBullet.newPos(passedBullPos)
				matched_bullets.append(closestBullet)
			else:
				matched_bullets.append(Bullet(*passedBull))

		BULLET_LIST = []
		BULLET_LIST.extend(matched_bullets)
		

		if(self.initalize):
			self.initalize = False
	
	#50 * 8 = 400!! in the time a tank can move the 50 units 
	#200 ** 2 if we dodge propperly...
	def shouldIDodge(self, myTank, minDistance):
		global BULLET_LIST, BULLET_RADIUS, TANK_LIST
		#check if we are in danger now
		dangerBullets = []
		extra = False
		other = True
		
		tempBar = BARRIERS[myTank.currentClosestBarrier]
					
		for bullet in BULLET_LIST:
			#if we fired this bullet then continue
			if(TANK_LIST[bullet.mastersName].tankName == myTank.tankName):
				continue
			straightLine = (myTank.pos - bullet.pos)
			
			
			
			#if the bullet is either moving orthogonal to us or is moving away then continue
			if(dot(bullet.direction, straightLine.normalized) >= 0):
				distToCollision = straightLine.magnitudeSq
				
				#if the bullet is within the considered deadly range
				if(distToCollision <= minDistance):
					#if(bullet.expectedLocation(1.25)[1] == False):
					#	continue
					
					if(areTheseOpposingSides(myTank, bullet)):
						continue
					
					#if it collides with the barrier we're closest to
					if(tempBar.rayBoxIntersection(bullet.pos, bullet.direction)):
						
						#where would it hit?
						tempPos = tempBar.getClosestPoint(bullet.pos)
						tempVec = (tempPos-bullet.pos)
						if(dot(bullet.direction, tempVec.normalized) >= 0.8 and tempVec.magnitudeSq < distToCollision):
							continue
					dangerBullets.append(bullet)
		return dangerBullets
	
	def getClosestTank(self, myTank, foresight = False):
		closestTank = None
		closestDist = math.inf
		targetShot = None
		if(NUM_ALIVE > 2):
			for key in TANK_LIST:
				tank = TANK_LIST[key]
				
				if(tank.tankName == self.tankName):
					continue
				else:
					tempVec = myTank.pos - tank.pos
					dist = tempVec.magnitudeSq
					if(dist < closestDist):
						result = myTank.canIShoot(tank, foresight)										
						seeAnyways = True
						if(seeAnyways):
							if(result[0]):
								targetShot = result[1]
								closestDist = dist
								closestTank = tank
						else:
							targetShot = result[1]
							closestDist = dist
							closestTank = tank
		else:
			for key in TANK_LIST:
				tank = TANK_LIST[key]
				
				if(tank.tankName == self.tankName):
					continue
				closestTank = TANK_LIST[key]
				targetShot = closestTank.pos
				break
		return [closestTank, targetShot]

	def duplicateName(self, name):
		currentName = name
		if(name in self.dupeNames):
			self.dupeNames[name] += 1
			currentName += str(self.dupeNames[name])
		else:
			self.dupeNames[name] = 0
		return currentName
	
	def canMove(self, direction, myTank):
		global BARRIERS
		tempPos = myTank.pos + direction*TANK_RADIUS
		
		if(tempPos.x < TANK_RADIUS or tempPos.x > MAP_SIZE-TANK_RADIUS or tempPos.y < TANK_RADIUS or tempPos.y > MAP_SIZE-TANK_RADIUS):
			return False
		
		for bar in BARRIERS:
			closestPoint = bar.getClosestPoint(tempPos)
			if((closestPoint - tempPos).magnitudeSq <= (TANK_RADIUS * 1.02)**2):
				return False
		
		return True
		
	def fireOrMove(self, myTank, foresight):
		global BARRIERS, DENSITY, NUM_ALIVE
		barNum = myTank.currentClosestBarrier
		
		if(NUM_ALIVE <= 2):
			"""
			biggest = -math.inf
			index = 0
			for i in range(0, len(DENSITY)):
				if(DENSITY[i] > biggest):
					biggest = DENSITY[i]
					index = i
			barNum = index
			"""
			barNum = 0
			
			
		
		tempBar = BARRIERS[barNum]
		direction = Vector2(0, 0)
		closestPoint = tempBar.getClosestPoint(myTank.pos)
		
		results = self.getClosestTank(myTank, foresight)
		closestTank = results[0]
		targetShot = results[1]
		fire_angle = 0
		
		if(NUM_ALIVE <= 2):
			if(barNum != myTank.currentClosestBarrier):
				#we need to go around our current barrier
				if(myTank.currentClosestBarrier != closestTank.currentClosestBarrier):
					barNum = myTank.currentClosestBarrier
					tempBar = BARRIERS[barNum]
					direction = Vector2(0, 0)
					closestPoint = tempBar.getClosestPoint(myTank.pos)	
		
		if(closestTank == None or self.hasFired or self.Shielding == True):
			##print(BARRIERS[barNum].mPos)
			
			self.Fire = False
			self.Move = True
			
			dirDirect = (closestPoint - myTank.pos)
			
			distanceToBarrier = dirDirect.magnitudeSq
			dirDirect = dirDirect.normalized
			
			if(closestTank and cross(myTank.pos - tempBar.mPos, closestTank.pos - tempBar.mPos).z):
				myTank.clockWise = -1
			else:
				myTank.clockWise = 1
			
			if(distanceToBarrier < (TANK_RADIUS*1.25)**2):
				"""if(self.Shielding):
					#
					#if(closestTank):
					#	direction = (closestTank.pos - myTank.pos).normalized.perpendicular
					#else:
					#	direction += -1*dirDirect
					#
					direction += -1*dirDirect
				else:
					direction += dirDirect.perpendicular * myTank.clockWise
				"""
				direction += dirDirect.perpendicular * myTank.clockWise
			else:
				direction = (BARRIERS[barNum].mPos - myTank.pos).normalized
			
			fire_angle = direction.degrees_inv
		else:
			self.Fire = True
			self.Move = False
			angle = (targetShot - myTank.pos)
			fire_angle = angle.degrees_inv
			fire_angle += random.uniform(-0.1, 0.1)
			self.fire_countdown = 0
			self.hasFired = True
		return fire_angle
		
	def make_move(self, your_location, tank_list_passed, bullet_list_passed):
		global TANK_LIST, BULLET_LIST, TANK_SPEED, BULLET_SPEED, BARRIERS, BULLET_RADIUS, TANK_RADIUS
		
		self.win.fill((0,0,0))
		
		self.dupeNames = {}
		self.Shield = False
		self.Dodge = False
		self.Move = False
		self.Fire = False
		
		minDist = 200
		angle = 0
		fire_angle = 0
		
		foresight = False		
		self.toDoBeforeReturn()
		
		self.setup(tank_list_passed, bullet_list_passed)
		myTank = TANK_LIST[self.tankName]
		myTank.closest = getClosestBarrier(myTank)
		
		dangerBullets = []
		dangerBullets = self.shouldIDodge(myTank, minDist**2)
		minDist = 51
		
		myTank.oldNumDangerBullets = len(dangerBullets)
		
		"""
		for bull in BULLET_LIST:
			bull.draw(self.win, myTank.tankName, not areTheseOpposingSides(bull, myTank))
			drawArrow(self.win, bull.pos, myTank.pos)
		
		pygame.display.flip()	
		"""
		
		if(len(dangerBullets) != 0 and self.Shielding == False):
			#print("some dangerous bullets", len(dangerBullets))
			
			self.Fire = False
			self.Move = False
			
			getOuttaThere = Vector2(0,0)
			getOuttaThere = None
			smallest = math.inf
			closestBullet = None
			dodgeDiretion = Vector2(0,0)
			shieldThisNow = False
			
			#print(len(dangerBullets))
			closestBullet = dangerBullets[0]
			smallest = (myTank.pos - closestBullet.pos).magnitudeSq
			getOuttaThere = dangerBullets[0].direction
			dodgeDiretion = getOuttaThere.perpendicular
			dodgeDiretion = dodgeDiretion.normalized
			
			#if(len(dangerBullets) == 2 and abs(dot(dangerBullets[0].direction, dangerBullets[1].direction)) < 0.1):
			#	shieldThisNow = True
			#	#means they're either nearly parallel, or that they're nearly perpendicular

			if(smallest <= (TANK_RADIUS+BULLET_RADIUS)**2 and self.Shielding == False or shieldThisNow == True and self.Shielding == False):
				self.Shield = True
			else:
				self.Dodge = True
				reversedX = False
				reversedY = False
				
				myTank.dodging = True
				
				bar = BARRIERS[myTank.currentClosestBarrier]
				closest = bar.getDistanceToRay(myTank.pos, dodgeDiretion)[1:]
				
				#if(closest.count(True) > 0):
				#	#means we're colliding with a side
				#	#try reversing instead?
				#	#myTank.clockWise *= -1
					
				
				if(myTank.pos.x + dodgeDiretion.x <= TANK_RADIUS or myTank.pos.x + dodgeDiretion.x >= MAP_SIZE-TANK_RADIUS):
					dodgeDiretion.x = -dodgeDiretion.x
					reversedX = True
					self.Shield = True
				if(myTank.pos.y  + dodgeDiretion.y <= TANK_RADIUS or myTank.pos.y + dodgeDiretion.y >= MAP_SIZE-TANK_RADIUS):
					dodgeDiretion.y = -dodgeDiretion.y
					reversedY = True
					self.Shield = True
				
				if(doIntersect(myTank.pos, myTank.pos + dodgeDiretion*TANK_RADIUS**2, closestBullet.pos, closestBullet.pos + closestBullet.direction*TANK_RADIUS**2)):
					dodgeDiretion *= -1
					if(doIntersect(myTank.pos, myTank.pos + dodgeDiretion*TANK_RADIUS**2, closestBullet.pos, closestBullet.pos + closestBullet.direction*TANK_RADIUS**2)):
						#self.Shield = True
						myTank.clockWise *= -1
				
				angle = dodgeDiretion.degrees_inv
				myTank.dodgeAngle = angle
				myTank.ammountLeftToMove = TANK_RADIUS + BULLET_RADIUS
			
		else:
			fire_angle = self.fireOrMove(myTank, foresight)
			
			
		if(self.Shield):
			myTank.shieldActive = True
			self.Shielding = True
			command = ("shield", 69)
		
		elif(self.Fire):
			command = ("fire", fire_angle)			
			
		elif(self.Dodge):
			command = ("move", myTank.dodgeAngle)
		
		elif(self.Move):
			self.oldPos = myTank.pos
			command = ("move", fire_angle)
		
		
		return command
