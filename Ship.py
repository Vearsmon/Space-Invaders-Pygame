import pygame
import Laser
from constants import PLAYER_WIDTH, PLAYER_HEIGHT, WHITE, WIDTH, PLAYER_SPD, PLAYER_LASER_SPD
from constants import ship_image_1, laser_image_1

class Ship(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(ship_image_1).convert(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
        self.speed = 0
        self.live_count = 3

    def update(self):
        self.speed = 0
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.speed -= PLAYER_SPD
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.speed += PLAYER_SPD
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH

    def shoot_ship_laser(self):
        return Laser.Laser(self.rect.centerx, self.rect.top, pygame.image.load(laser_image_1).convert(), PLAYER_LASER_SPD, flip=False)
