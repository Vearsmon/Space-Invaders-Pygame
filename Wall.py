import pygame
from constants import WALL_WIDTH, WALL_HEIGHT, WHITE, wall_image


class Wall(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(wall_image).convert(), (WALL_WIDTH, WALL_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
