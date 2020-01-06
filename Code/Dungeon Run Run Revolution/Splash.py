import pygame

def splash(screen, clock):

    # Updates
    dt = clock.tick(60) / 1000.0
    if (dt > 1 / 20.0):
        dt = 0.0

    screen.fill((0,0,0))

    image = pygame.image.load("Splash.jpg")
    screen.blit(image, (0, 0))

    pygame.display.flip()
    pygame.time.wait(5000)

def gameOver(screen, clock):
    image = pygame.image.load("Cat.png")

    dt = clock.tick(60) / 1000.0
    if (dt > 1 / 20.0):
        dt = 0.0

    screen.fill((0,0,0))

    screen.blit(image, (242, 84))

    pygame.display.flip()
    pygame.time.wait(5000)
