from settings import *
from player import Player
from sprite import *  

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
        self.allSprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.allSprites, (400,300), self.collisionSprites)
        for i in range(6):
            x = randint(0, WINDOW_WIDTH)
            y = randint(0, WINDOW_HEIGHT)
            w = randint(60, 100)
            h = randint(60, 100)
            CollisionSprite((self.allSprites, self.collisionSprites), (x,y), (w, h))

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
            self.allSprites.draw(self.displaySurface)
            pygame.display.update()
        
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()