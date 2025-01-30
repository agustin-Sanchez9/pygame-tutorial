from settings import *
from math import atan2, degrees

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True


class Gun(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        # player connection
        self.player = player
        self.distance = 120
        self.playerDir = pygame.Vector2(1,0)

        # setup
        super().__init__(groups)
        self.gunSurf = pygame.image.load(join('vampire survivor', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gunSurf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.playerDir * self.distance)

    def getDirection(self):
        mousePos = pygame.Vector2(pygame.mouse.get_pos())
        playerPos = pygame.Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) # because player is allways in the center due to the camera following him
        self.playerDir = (mousePos - playerPos).normalize()

    def rotateGun(self):
        angle = degrees(atan2(self.playerDir.x, self.playerDir.y)) -90
        if self.playerDir.x > 0:
            self.image = pygame.transform.rotozoom(self.gunSurf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gunSurf, abs(angle), 1) # abs() is used to avoid bad behavior by angle being negative
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.getDirection()
        self.rotateGun()
        self.rect.center = self.player.rect.center + self.playerDir * self.distance


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, dir):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.spawnTime = pygame.time.get_ticks()
        self.lifeTime = 1500

        self.direction = dir
        self.speed = 2000

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

        if pygame.time.get_ticks() - self.spawnTime >= self.lifeTime:
            self.kill()
