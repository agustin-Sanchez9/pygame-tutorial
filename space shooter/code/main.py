import pygame
from os.path import join
from random import randint

pygame.init()

# size of main window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# creates the main screen/window
displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# sets the title of main window/caption
pygame.display.set_caption("Space shooter")

# var to control main loop
running = 1

# made to control frame rate
clock = pygame.time.Clock()

# player
playerSurf = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
# player rectangle
playerRect = playerSurf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
playerDirection = pygame.math.Vector2()
playerSpeed = 300


# meteor
meteorSurf = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
meteorRect = meteorSurf.get_frect(center = (WINDOW_WIDTH/3, WINDOW_HEIGHT/3))

# laser
laserSurf = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
laserRect = laserSurf.get_frect(bottomleft = (20,WINDOW_HEIGHT-20))

# star
starSurf = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha()
starPositions = [(randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)) for i in range(50)]

# main loop
while running:
    
    # sets the frame rate to the given value
    # delta time
    dt = clock.tick(120) / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0


    #input
    keys = pygame.key.get_pressed()

    playerDirection.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    playerDirection.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])


    # draw the game
    displaySurface.fill("black")

    for pos in starPositions:
        displaySurface.blit(starSurf, pos)

    #displaySurface.blit(laserSurf, laserRect)
    #displaySurface.blit(meteorSurf, meteorRect)

    # player
    playerRect.center += playerDirection * playerSpeed * dt
    displaySurface.blit(playerSurf, playerRect)


    pygame.display.update() 

# opposite to init(), nedeed to avoid bugs or bad behavior
pygame.quit()