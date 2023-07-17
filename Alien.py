import pygame
import Laser
from constants import ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_SPD, ALIEN_LASER_SPD, WHITE, laser_image_1, bonus_image


class Alien(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, alien_type, cost):
        pygame.sprite.Sprite.__init__(self)
        self.image = alien_type
        self.image = pygame.transform.scale(alien_type, (ALIEN_WIDTH, ALIEN_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
        self.speed = ALIEN_SPD
        self.cost = cost

    def update(self, speed_coefficient, direction_x, direction_y=0):
        self.rect.x += direction_x * self.speed * speed_coefficient
        self.rect.y += direction_y

    def shoot_alien_laser(self):
        return Laser.Laser(self.rect.centerx, self.rect.centery, pygame.image.load(laser_image_1).convert(), ALIEN_LASER_SPD, flip=True)


class Bonus(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(bonus_image).convert(), (3/2 * ALIEN_WIDTH, ALIEN_HEIGHT))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
        self.speed = ALIEN_SPD
        self.direction = direction

    def update(self):
        self.rect.x += self.direction * self.speed
