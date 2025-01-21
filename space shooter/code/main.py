import pygame
from os.path import join
from random import randint, uniform


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        #setup
        self.image = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 200))
        self.direction = pygame.Vector2()
        self.speed = 700

        # cooldown
        self.canShoot = True
        self.laserShootTime = 0
        self.cooldownTime = 300  # in ms

    def laserTimer(self):
        if not self.canShoot:
            currentTime = pygame.time.get_ticks()
            if currentTime - self.laserShootTime >= self.cooldownTime:
                self.canShoot = True

    def update(self, dt):
        pressedKeys = pygame.key.get_pressed()
        # movement
        self.direction.x = int(pressedKeys[pygame.K_d]) - int(pressedKeys[pygame.K_a])
        self.direction.y = int(pressedKeys[pygame.K_s]) - int(pressedKeys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        # fire laser
        if self.canShoot: 
            Laser((allGroup, laserGroup), laserSurf, self.rect.midtop)
            self.canShoot = False
            self.laserShootTime = pygame.time.get_ticks()
            laserSound.play()

        self.laserTimer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        #setup
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 1850 * dt 
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.orignal = surf
        self.image = self.orignal
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2((uniform(-0.5, 0.5), 1))
        self.speed = randint(100,500)
        self.rotationSpeed = randint(50,100)
        self.rotationAngle = 0


    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        self.rotationAngle += self.rotationSpeed * dt
        self.image = pygame.transform.rotozoom(self.orignal, self.rotationAngle, 1)
        self.rect = self.image.get_frect(center = self.rect.center) # needed to avoid strange movement patterns in the meteors while the image changes
    

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups)
        self.frames = frames
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frameIndex += 40 * dt
        if self.frameIndex < len(self.frames):
            self.image = self.frames[int(self.frameIndex)]
        else:
            self.kill()


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def collisions():
    global running
    playercollisions = pygame.sprite.spritecollide(player, meteorGroup, True, pygame.sprite.collide_mask)

    if playercollisions:
        running = False

    for laser in laserGroup:
        collisions = pygame.sprite.spritecollide(laser, meteorGroup, True)
        if collisions:
            laser.kill()
            AnimatedExplosion(allGroup, explosionFrames, laser.rect.midtop)
            explosionSound.play()


def score():
    currntTime = pygame.time.get_ticks() // 1000
    textSurf = font.render(str(currntTime), True, 'white')
    textRect = textSurf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-30))
    displaySurface.blit(textSurf, textRect)
    pygame.draw.rect(displaySurface, 'white', textRect.inflate(20, 15).move(0,-6), 3, 10)


pygame.init()

# size of main window
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 960

# creates the main screen/window
displaySurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# sets the title of main window/caption
pygame.display.set_caption("Space shooter")

# made to control frame rate
clock = pygame.time.Clock()

# imports
starSurface = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha() # the import is made here so its only made once, otherwise in the for loop it will import the image 20 times
laserSurf = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
meteorSurf = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
font = pygame.font.Font(join('space shooter', 'images', 'Oxanium-Bold.ttf'), 40)
explosionFrames = [pygame.image.load(join('space shooter', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]
# sound imports
laserSound = pygame.mixer.Sound(join('space shooter', 'audio', 'laser.wav'))
explosionSound = pygame.mixer.Sound(join('space shooter', 'audio', 'explosion.wav'))
gameMusic = pygame.mixer.Sound(join('space shooter', 'audio', 'game_music.wav'))
laserSound.set_volume(0.05)
explosionSound.set_volume(0.1)
gameMusic.set_volume(0.1)
gameMusic.play(loops = -1)

# in a groupo the sprites are sorted by the time has been added, so stars must be created before the player
allGroup = pygame.sprite.Group()
meteorGroup = pygame.sprite.Group()
laserGroup = pygame.sprite.Group()

for i in range(20):
    Star(allGroup, starSurface)

player = Player(allGroup)


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
            x = randint(0,WINDOW_WIDTH)
            y = randint(-200,-100)
            Meteor((allGroup, meteorGroup), meteorSurf, (x,y))

    allGroup.update(dt)

    collisions()

    # draw the game
    displaySurface.fill("black")
    allGroup.draw(displaySurface)

    score()


    pygame.display.update()

# opposite to init(), nedeed to avoid bugs or bad behavior
pygame.quit()