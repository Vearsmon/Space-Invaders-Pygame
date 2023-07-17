import pygame
from constants import LASER_WIDTH, LASER_HEIGHT, BLACK, HEIGHT


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, flip):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.image = pygame.transform.scale(image, (LASER_WIDTH, LASER_HEIGHT))
        if flip:
            self.image = pygame.transform.flip(self.image, False, True)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
