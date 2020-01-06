import pygame
import myvector
from RunningMet import *
from healthMeter import *
from Animation import *
from Animations import *
import randommap
from MeeleEnemy import *
from RangedEnemy import *
import random
import math
import Splash

from Objects2D import *
#from MeeleEnemy import *
#from RangedEnemy import *
#from enemy import *

from test import *

from vectors import Point, Vector

def randomPosition(center, squareRadius):
    r = random.uniform(0, squareRadius)
    theta = 2*math.pi*random.random()
    x = r**0.5 * math.cos(theta)
    y = r**0.5 * math.sin(theta)

    return MyVector(x, y)

def Explode(clouds, animation, window, offset):
    for item in clouds:
        window.blit(animation.getSurf(), item)

        
random.seed()

win_width = 1024
win_height = 768
pygame.display.init()
pygame.font.init()
pygame.mixer.init()
pygame.joystick.init()
screen = pygame.display.set_mode((win_width, win_height))
done = False

rando = randommap.RandomMap()
player_xy = rando.mPlayerStartVector.copy()
player_prev_xy = player_xy.copy()


#M.test_tiles("DungeonTemplate1.png")

clock = pygame.time.Clock()

rando.mCamX = 0
rando.mCamY = 0
move_speed = 30
player_rect = [player_xy.x, player_xy.y, 82, 64]
wall_codes = [33, 17, 37]
hit_detection_exception_codes = []
exit_codes = []
player_accel = myvector.MyVector2(0, 0)
player_vel = myvector.MyVector2(0, 0)
friction_coefficient = 0.06
movingX = False
movingY = False
TouchingTop = False
TouchingBottom = False
TouchingLeft = False
TouchingRight = False

###########################################
#player animations

spriteSheets = []
numFrames = []
followThrough = []
#followThrough for each animation = the next animation number if a diferent animation follows it, by deafualt the animation will simply repeat (followThrough = -1)

#walkingLeft
spriteSheets.append(pygame.image.load("./Sprites/playerWalkLeft.png"))#0
numFrames.append(9)
followThrough.append(-1)

#walkingRight
spriteSheets.append(pygame.image.load("./Sprites/playerWalkRight.png"))#1
numFrames.append(9)
followThrough.append(-1)

#runningLeft
spriteSheets.append(pygame.image.load("./Sprites/playerRunLeft.png"))#2
numFrames.append(9)
followThrough.append(-1)

#runningRight
spriteSheets.append(pygame.image.load("./Sprites/playerRunRight.png"))#3
numFrames.append(9)
followThrough.append(-1)

#idleLeft
spriteSheets.append(pygame.image.load("./Sprites/playerIdleLeft.png"))#4
numFrames.append(2)
followThrough.append(-1)

#idleRight
spriteSheets.append(pygame.image.load("./Sprites/playerIdleRight.png"))#5
numFrames.append(2)
followThrough.append(-1)

#kickLeft
spriteSheets.append(pygame.image.load("./Sprites/playerAttackLeft.png"))#6
numFrames.append(8)
followThrough.append(-1)

#kickRight
spriteSheets.append(pygame.image.load("./Sprites/playerAttackRight.png"))#7
numFrames.append(8)
followThrough.append(-1)

#CompleteSwordAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerSwordLeft.png"))#8
numFrames.append(9)
followThrough.append(-1)

#CompleteSwordAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerSwordRight.png"))#9
numFrames.append(9)
followThrough.append(-1)

#CompleteHammerAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerHammerLeft.png"))#10
numFrames.append(9)
followThrough.append(-1)

#CompleteHammerAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerHammerRight.png"))#11
numFrames.append(9)
followThrough.append(-1)

#CompleteStickAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerBranchLeft.png"))#12
numFrames.append(9)
followThrough.append(-1)

#CompleteStickAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerBranchRight.png"))#13
numFrames.append(9)
followThrough.append(-1)

#CompleteStaffAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Staff_right.png"))#14
numFrames.append(3)
followThrough.append(15)

#TwitchStaffAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Staff_right.png"))#15
numFrames.append(3)
followThrough.append(-1)

#CompleteStaffAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Staff_left.png"))#16
numFrames.append(3)
followThrough.append(17)

#TwitchStaffAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Staff_left.png"))#17
numFrames.append(3)
followThrough.append(-1)

#CompleteCrossbowAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Crossbow_right.png"))#18
numFrames.append(3)
followThrough.append(19)

#TwitchCrossbowAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Crossbow_right.png"))#19
numFrames.append(3)
followThrough.append(-1)

#CompleteCrossbowAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Crossbow_left.png"))#20
numFrames.append(3)
followThrough.append(21)

#TwitchCrossbowAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Crossbow_left.png"))#21
numFrames.append(3)
followThrough.append(-1)

#CompleteBowAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Bow_right.png"))#22
numFrames.append(3)
followThrough.append(13)

#TwitchBowAnimationLeft
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Bow_right.png"))#23
numFrames.append(3)
followThrough.append(-1)

#CompleteBowAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/playerRangeAttack_Bow_left.png"))#24
numFrames.append(3)
followThrough.append(25)

#TwitchBowAnimationRight
spriteSheets.append(pygame.image.load("./Sprites/PlayerAimTwitch_Bow_left.png"))#25
numFrames.append(3)
followThrough.append(-1)


playerAnimations = Animations(numFrames, spriteSheets, followThrough)
##########################################

###########################################
#goblin animations

spriteSheets = []
numFrames = []
followThrough = []

#walkingLeft
spriteSheets.append(pygame.image.load("./Sprites/GoblinWalkLeft.png"))#0
numFrames.append(8)
followThrough.append(-1)

#walkingRight
spriteSheets.append(pygame.image.load("./Sprites/GoblinWalkLeft.png"))#1
numFrames.append(8)
followThrough.append(-1)

#AttackLeft
spriteSheets.append(pygame.image.load("./Sprites/GoblinAttackLeft.png"))#2
numFrames.append(8)
followThrough.append(4)

#AttackRight
spriteSheets.append(pygame.image.load("./Sprites/GoblinAttackRight.png"))#3
numFrames.append(8)
followThrough.append(5)

#SpinLeft
spriteSheets.append(pygame.image.load("./Sprites/GoblinSpinLeft.png"))#4
numFrames.append(5)
followThrough.append(-1)

#SpinRight
spriteSheets.append(pygame.image.load("./Sprites/GoblinSpinRight.png"))#5
numFrames.append(5)
followThrough.append(-1)

goblinAnimations = Animations(numFrames, spriteSheets, followThrough)
##########################################

# rando.mEnemyList.append(meele(player_xy.x//64, player_xy.y//64,goblinAnimations,5.0, 10,screen.get_width(),None,100, 8))

###########################################
#skelliton animations

spriteSheets = []
numFrames = []
followThrough = []

#walkingLeft
spriteSheets.append(pygame.image.load("./Sprites/skellitonWalkLeft.png"))#0
numFrames.append(2)
followThrough.append(-1)

#walkingRight
spriteSheets.append(pygame.image.load("./Sprites/skellitonWalkRight.png"))#1
numFrames.append(2)
followThrough.append(-1)

skullAnimations = Animations(numFrames, spriteSheets, followThrough)
##########################################


##########################################
#projectile animations

spriteSheets = []
numFrames = []
followThrough = []

#arrowLeft
spriteSheets.append(pygame.image.load("./Sprites/arrowAnimationLeft.png"))#0
numFrames.append(6)
followThrough.append(-1)
#arrowRight
spriteSheets.append(pygame.image.load("./Sprites/arrowAnimationRight.png"))#1
numFrames.append(6)
followThrough.append(-1)

#boltLeft
spriteSheets.append(pygame.image.load("./Sprites/boltAnimationLeft.png"))#2
numFrames.append(6)
followThrough.append(-1)
#boltRight
spriteSheets.append(pygame.image.load("./Sprites/boltAnimationRight.png"))#3
numFrames.append(6)
followThrough.append(-1)

#fireballLeft
spriteSheets.append(pygame.image.load("./Sprites/fireBallLeft.png"))#4
numFrames.append(4)
followThrough.append(-1)
#fireballRight
spriteSheets.append(pygame.image.load("./Sprites/fireBallRight.png"))#5
numFrames.append(4)
followThrough.append(-1)

projectileAnmations = Animations(numFrames, spriteSheets, followThrough)
#######################################

#DEATH
spriteSheets = (pygame.image.load("./Sprites/explosion.png"))#3
CloudNine = Animation(10, spriteSheets)

joystick_count = pygame.joystick.get_count()

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

#runMeter = RunMet(10, 10, 400, 30, 380, 25, (255, 0, 0), (0, 255, 0), "Times New Roman", (255, 255, 255), 1.5)
#^ rectangle based
runMeter = RunMet(10, 10, 0, 0, 0, 0, 0, 0, "Times New Roman", (255, 255, 255), 1.5, 0.1, True, "./Sprites/BackAnimation", "./Sprites/FrontAnimation", True)
healthMeter = HealthMet(10, 50, 100, "./Sprites/HealthBackAnimation", "./Sprites/HeathFrontAnimation", True)
faceLeft = True
faceRight = False

spawnRate = 10.0
spawnTimer = 5.0

tSurf = playerAnimations.getSurf()
PlayerSurfDim = Cuboid(MyVector(0,0,0), MyVector(player_xy.x,player_xy.y), MyVector(1, 1))

Splash.splash(screen, clock)


puffsOfCloudsLocations = []

while not done:
    # Updates
    dt = clock.tick(60) / 1000.0
    movingX = False
    movingY = False
    pygame.display.set_caption('Please Stop Running!')
    move_speed = 30 + (runMeter.runStreak * 2.2)

    spawnTimer+=dt
    if(spawnTimer >= spawnRate):
        #print("Skeleton!")
        newPos = player_xy + randomPosition(player_xy, 320**2)
        #print(newPos, player_xy)
        skelimon = random.randint(0,1)
        if(skelimon == 0):
            #self, x, y, animations, rechargeTime, damage, attackRange, drops, health = 100, movementSpeed = 5
            rando.mEnemyList.append(meele(newPos.x, newPos.y, goblinAnimations, 5.0, 10, screen.get_width()//4, None, 100, 150))
        else:
            #self, x, y, animations, projectileAnmations, reloadSpeed, projectileSpeed, damage, attackRange, drops, movementSpeed = 5, health = 100
            rando.mEnemyList.append(ranger(newPos.x, newPos.y, skullAnimations, projectileAnmations, 7.25, 400, 4.81, screen.get_width()//2, None, 100, 100))
        spawnTimer = 0.0

    tSurf = playerAnimations.getSurf()
    PlayerSurfDim = Cuboid(MyVector(0,0,0), player_xy, MyVector(tSurf.get_width(), tSurf.get_height()))
    
    for unit in rando.mEnemyList:
        PoPo = unit.update(dt, PlayerSurfDim, 5, playerAnimations.attack)
        if(PoPo == None):
            if(isinstance(unit, meele)):
                if(unit.hasHit == False):
                    if(collides(PlayerSurfDim, unit.cube) and unit.animations.attack == True):
                        print(healthMeter.health, "IS NOW:", healthMeter.health-unit.damage)
                        healthMeter.damage(unit.damage)
                        unit.hasHit = True
                        print("hit player!!")
        else:
            puffsOfCloudsLocations.append(PoPo)
            rando.mEnemyList.remove(unit)
        if unit.health <= 0:
            rando.mEnemyList.remove(unit)
            # EXPLOSION FUNCTION GOES HERE
    #Need to generate tileMap
    
    """update player position and other player stuff"""
    player_prev_xy = player_xy.copy()

    left_right_axis = 0

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            done = True
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                done = True
            if evt.key == pygame.K_F9:
                rando.mExitTriggered = True
            if evt.key == pygame.K_F4:
                healthMeter.dam = 100000
            if evt.key == pygame.K_SPACE:
                playerAnimations.attack = True

        if evt.type == pygame.JOYBUTTONDOWN:
            if evt.button == 0:
                pass
            else:
                print("button: ", str(evt.button))

    if joystick_count > 0:
        left_right_axis = joystick.get_axis(0)
        up_down_axis = joystick.get_axis(1)

        if left_right_axis < - 0.2:
            player_accel.x += move_speed * left_right_axis * dt
            faceLeft = True
            faceRight = False
        if left_right_axis > 0.2:
            player_accel.x += move_speed * left_right_axis * dt
            faceLeft = False
            faceRight = True

        if up_down_axis < - 0.2:
            player_accel.y += move_speed * up_down_axis * dt
        if up_down_axis > 0.2:
            player_accel.y += move_speed * up_down_axis * dt


    key_pressed = pygame.key.get_pressed()
    
    if key_pressed[pygame.K_a]:
        player_accel.x -= move_speed * dt
        faceLeft = True
        faceRight = False

    if key_pressed[pygame.K_d]:
        player_accel.x += move_speed * dt
        faceLeft = False
        faceRight = True

    if key_pressed[pygame.K_s]:
        player_accel.y += move_speed * dt

    if key_pressed[pygame.K_w]:
        player_accel.y -= move_speed * dt

    if player_accel.magnitude > (move_speed * dt):
        player_accel = player_accel.normalized * (move_speed * dt)

    if player_vel.magnitudeSq > 130:
        movingX = True
        movingY = True

    if player_vel.magnitudeSq < (90 + (runMeter.runStreak * 4)):
        player_vel += (player_accel * 2.0)
    else:
        player_vel += player_accel
    player_vel *= (1-friction_coefficient)
    if player_vel.magnitudeSq < 0.3:
        player_vel = myvector.MyVector2(0, 0)
    player_accel = myvector.MyVector2(0, 0)

    player_xy += player_vel

    player_rect[0] = player_xy.x
    player_rect[1] = player_xy.y

    # Check for collision on the new x & y and if it's colliding, roll the movement back step by step (via vector math
    # between the new and previous x&y) until the player is in a clear spot
    player_movement_vector = player_xy - player_prev_xy
    increment_back = player_movement_vector.normalized
    test_location = player_xy.copy()
    original_test_location = player_xy.copy()
    attempts = 0
    while ((rando.overlaps(player_rect)) and (attempts < 100)):
        test_location -= increment_back
        player_rect[0] = test_location.x
        player_rect[1] = test_location.y
        attempts += 1
    if attempts == 100:
        test_location = original_test_location
        player_rect[0] = test_location.x
        player_rect[1] = test_location.y

    LeftRect = [player_rect[0] - 2, player_rect[1]+4, 2, player_rect[3]-8]
    RightRect = [player_rect[0] + player_rect[2], player_rect[1]+4, 2, player_rect[3]-8]
    TopRect = [player_rect[0]+4, player_rect[1] - 2, player_rect[2]-8, 2]
    BottomRect = [player_rect[0]+4, player_rect[1] + player_rect[3], player_rect[2]-8, 2]
    TouchingLeft = rando.overlaps(LeftRect)
    TouchingRight = rando.overlaps(RightRect)
    TouchingBottom = rando.overlaps(BottomRect)
    TouchingTop = rando.overlaps(TopRect)

    if (TouchingTop):
        player_vel.y = max(player_vel.y, -player_vel.y)
        movingY = False

    if (TouchingBottom):
        player_vel.y = min(player_vel.y, -player_vel.y)
        movingY = False

    if (TouchingLeft):
        player_vel.x = max(player_vel.x, -player_vel.x)
        faceLeft = False
        faceRight = True
        movingX = False

    if (TouchingRight):
        player_vel.x = min(player_vel.x, -player_vel.x)
        faceRight = False
        faceLeft = True
        movingX = False

    if (not TouchingTop) and (not TouchingBottom):
        test_location.y = original_test_location.y

    if not (TouchingLeft or TouchingRight):
        test_location.x = original_test_location.x

    # Once we have a clear spot, we update the player x & y and calculate our collision rectangles
    # and whether or not they're colliding currently
    player_xy.x = test_location.x
    player_xy.y = test_location.y

    if player_xy.x < 0:
        player_xy.x = 0
        movingX = False

    if player_xy.x > rando.mMapWidth * (rando.mTileWidth) - player_rect[2]:
        player_xy.x = rando.mMapWidth * (rando.mTileWidth) - player_rect[2]
        movingX = False

    if player_xy.y < 0:
        player_y = 0
        movingY = False

    if player_xy.y > rando.mMapHeight * (rando.mTileHeight) - player_rect[3]:
        player_xy.y = rando.mMapHeight * (rando.mTileHeight) - player_rect[3]
        movingY = False

    rando.mCamX = min(max(0, int(player_xy.x) - (win_width // 2)), (rando.mTileWidth*rando.mMapWidth) - win_width)
    rando.mCamY = min(max(0, int(player_xy.y) - (win_height // 2)), (rando.mTileHeight*rando.mMapHeight) - win_height)

    #rando.mCamX = min(max(0, int(player_xy.x) - (win_width // 2)), (rando.mTileWidth*rando.mMapWidth) - win_width)
    #rando.mCamY = min(max(0, int(player_xy.y) - (win_height // 2)), (rando.mTileHeight*rando.mMapHeight) - win_height)

    player_rect[0] = int(player_xy.x)
    player_rect[1] = int(player_xy.y)

    if(player_vel.x < 0):
        if(playerAnimations.attack == False):
            playerAnimations.metaAnime = 0
            if(runMeter.timeMoving > 2.5):
                playerAnimations.metaAnime = 2
        else:
            if(faceLeft == True):
                playerAnimations.metaAnime = 6 + 2
            else:
                playerAnimations.metaAnime = 7 + 2
    elif(player_vel.x > 0):
        if(playerAnimations.attack == False):
            playerAnimations.metaAnime = 1
            if(runMeter.timeMoving > 2.5):
                playerAnimations.metaAnime = 3
        else:
            if(faceLeft == True):
                playerAnimations.metaAnime = 6 + 2
            else:
                playerAnimations.metaAnime = 7 + 2

    if(movingY == True or movingX == True):
        runMeter.update(dt, True)
    else:
        runMeter.update(dt, False)
        if(faceLeft == True and playerAnimations.attack == False):
            playerAnimations.metaAnime = 4
        if(faceRight == True and playerAnimations.attack == False):
            playerAnimations.metaAnime = 5
    healthMeter.update(dt)
    #playerAnimations.metaAnime = 10
    playerAnimations.update(dt)
    #goblinAnimations.update(dt)
    #skullAnimations.update(dt)
    CloudNine.update(dt)
    
    # Drawing
    screen.fill((0, 0, 0))

    #M.draw(screen, player_xy)

    #rando.draw(screen, player_xy)

    #M.draw(screen, player_xy)
    #rando.draw(screen, player_xy)

    #M.draw(screen, player_xy)
    level_change_test = rando.draw(screen, player_xy)

    if isinstance(level_change_test, myvector.MyVector2):
        # Do some kind of level change screen
        player_vel = myvector.MyVector2(0, 0)
        player_accel = myvector.MyVector2(0, 0)
        player_xy = level_change_test
        player_prev_xy = level_change_test

    # color = (0, 255, 0)
    #
    # pygame.draw.rect(screen, color, [player_rect[0]-rando.mCamX, player_rect[1]-rando.mCamY, player_rect[2], player_rect[3]], 1)
    # if TouchingTop:
    #     color = (255,0,0)
    # else:
    #     color = (0, 255, 0)
    # pygame.draw.rect(screen, color, [TopRect[0]-rando.mCamX, TopRect[1]-rando.mCamY, TopRect[2], TopRect[3]], 1)
    # if TouchingBottom:
    #     color = (255,0,0)
    # else:
    #     color = (0, 255, 0)
    # pygame.draw.rect(screen, color, [BottomRect[0]-rando.mCamX, BottomRect[1]-rando.mCamY, BottomRect[2], BottomRect[3]], 1)
    # if TouchingLeft:
    #     color = (255,0,0)
    # else:
    #     color = (0, 255, 0)
    # pygame.draw.rect(screen, color, [LeftRect[0]-rando.mCamX, LeftRect[1]-rando.mCamY, LeftRect[2], LeftRect[3]], 1)
    # if TouchingRight:
    #     color = (255,0,0)
    # else:
    #     color = (0, 255, 0)
    # pygame.draw.rect(screen, color, [RightRect[0]-rando.mCamX, RightRect[1]-rando.mCamY, RightRect[2], RightRect[3]], 1)

    runMeter.drawRunMet(screen)
    healthMeter.drawHealthMet(screen)

    #screen.blit(knight, (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))
    #screen.blit(playerAnimations.getSurf(), (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))
    #screen.blit(goblinAnimations.getSurf(), (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))

    #screen.blit(knight, (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))
    #screen.blit(playerAnimations.getSurf(), (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))
    #screen.blit(goblinAnimations.getSurf(), (int(player_rect[0])-M.mCamX, int(player_rect[1])-M.mCamY))

    #screen.blit(knight, (int(player_rect[0])-rando.mCamX, int(player_rect[1])-rando.mCamY))
    animationOffSet = MyVector(0,0)
    if(playerAnimations.attack == True):
        animationOffSet = MyVector((playerAnimations.getSurf().get_width() - player_rect[2] ), (playerAnimations.getSurf().get_height() - player_rect[3] ))
    screen.blit(playerAnimations.getSurf(), (int(player_rect[0])-rando.mCamX-animationOffSet.x, int(player_rect[1])-rando.mCamY-animationOffSet.y))
    #screen.blit(goblinAnimations.getSurf(), (int(player_rect[0])-rando.mCamX, int(player_rect[1])-rando.mCamY))
    for unit in rando.mEnemyList:
        unit.draw(screen, rando.mCamX, rando.mCamY)

    Explode(puffsOfCloudsLocations,CloudNine, screen, MyVector(rando.mCamX, rando.mCamY))
    
    inventory = Inventory()
    #inventory.add_item(Item('Sword', 0, 10))
    #inventory.add_item(Item('Armor', 1, 25))
    #inventory.add_item(Item('healthPotion', 2, 2))
    inventory.draw_inventory(screen)
    #inventory.print_items()
    if healthMeter.health - healthMeter.dam <= 0:
        Splash.gameOver(screen, clock)
        done = True
    pygame.display.flip()



pygame.display.quit()


    
