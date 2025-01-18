import pygame
from os.path import join
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        #setup
        self.image = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 500

        # cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.cooldownTime = 400  # in ms

    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserShootTime >= self.cooldownTime:
                self.canShoot = True

    def update(self, dt):
        pressedKeys = pygame.key.get_pressed()
        justPressedKeys = pygame.key.get_just_pressed()

        # movement
        self.direction.x = int(pressedKeys[pygame.K_d]) - int(pressedKeys[pygame.K_a])
        self.direction.y = int(pressedKeys[pygame.K_s]) - int(pressedKeys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # fire laser
        if justPressedKeys[pygame.K_SPACE] and self.canShoot: 
            print("fire laser")
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()

        self.laserTimer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        #setup
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))


pygame.init()

# size of main window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# creates the main screen/window
displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# sets the title of main window/caption
pygame.display.set_caption("Space shooter")

# made to control frame rate
clock = pygame.time.Clock()

# in a groupo the sprites are sorted by the time has been added, so stars must be created before the player
spriteGroup = pygame.sprite.Group()
starSurface = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha() # the import is made here so its only made once, otherwise in the for loop it will import the image 20 times
for i in range(20):
    Star(spriteGroup, starSurface)

player = Player(spriteGroup)


# events
meteorEvent = pygame.event.custom_type()
pygame.time.set_timer(meteorEvent, 1000)


# var to control main loop
running = True
# main loop
while running:
    
    # sets the frame rate to the given value
    dt = clock.tick(120) / 1000 # divide by 1000 to convert from ms to s

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteorEvent:
            print("create meteor")

    spriteGroup.update(dt)

    # draw the game
    displaySurface.fill("black")

    spriteGroup.draw(displaySurface)

    pygame.display.update() 

# opposite to init(), nedeed to avoid bugs or bad behavior
pygame.quit()