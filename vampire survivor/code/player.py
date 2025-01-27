from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos, collisionSprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-50, 0)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collisionSprites = collisionSprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox.center
       

    def collision(self, direction):
        for sprite in self.collisionSprites:
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom
                     

    def update(self, dt):
        self.input()
        self.move(dt)
