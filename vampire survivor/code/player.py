from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos, collisionSprites):
        super().__init__(groups)
        self.loadImages()
        self.state = 'down'
        self.frameIndex = 0
        self.image = pygame.image.load(join('vampire survivor', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox = self.rect.inflate(-60, -100)
        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collisionSprites = collisionSprites

    def loadImages(self):
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}

        for state in self.frames.keys():
            for folderPath, subFolders, fileNames in walk(join('vampire survivor', 'images', 'player', state)):
                if fileNames:
                    for file in sorted(fileNames, key = lambda name: int(name.split('.')[0])):
                        fullPath = join(folderPath, file)
                        surf = pygame.image.load(fullPath).convert_alpha()
                        self.frames[state].append(surf)

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
                     
    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # animate
        self.frameIndex = self.frameIndex + 8 * dt if self.direction else 0
        self.image = self.frames[self.state][int(self.frameIndex)%len(self.frames[self.state])]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
