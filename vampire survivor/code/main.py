from settings import *
from player import Player
from sprite import *
from groups import *
from pytmx.util_pygame import load_pygame
from random import randint

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.allSprites = AllSprites()
        self.collisionSprites = pygame.sprite.Group()

        self.setup()
        

    def setup(self):
        map = load_pygame(join('vampire survivor', 'data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite(self.allSprites, (x * TILE_SIZE, y * TILE_SIZE), image)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((self.allSprites, self.collisionSprites), (obj.x, obj.y), obj.image)
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite(self.collisionSprites, (obj.x, obj.y), pygame.Surface((obj.width, obj.height)))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(self.allSprites, (obj.x,obj.y), self.collisionSprites)
                self.gun = Gun(self.allSprites, self.player)
               

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(120) / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.allSprites.update(dt)

            # draw
            self.displaySurface.fill('black')
            self.allSprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()