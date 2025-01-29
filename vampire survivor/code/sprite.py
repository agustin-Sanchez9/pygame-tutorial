from settings import *

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
        self.distance = 80
        self.playerDir = pygame.Vector2(1,0)

        # setup
        super().__init__(groups)
        self.gunSurf = pygame.image.load(join('vampire survivor', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gunSurf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.playerDir * self.distance)


    def update(self, _):
        self.rect.center = self.player.rect.center + self.playerDir * self.distance


