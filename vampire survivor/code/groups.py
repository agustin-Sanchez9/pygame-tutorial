from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, targetPos):
        self.offset.x = -(targetPos[0] - WINDOW_WIDTH/2)
        self.offset.y = -(targetPos[1] - WINDOW_HEIGHT/2)

        groundSprite = [sprite for sprite in self if hasattr(sprite, 'ground')]
        objectSprite = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [groundSprite, objectSprite]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.displaySurface.blit(sprite.image, sprite.rect.topleft + self.offset)