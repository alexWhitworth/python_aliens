import pygame as pg
import os
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, settings, screen):
        # basic attributes
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pg.image.load(os.path.join('Images','ship.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.speed_factor = 1.0

        # initial position
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # movements
        self.moving_right = False
        self.moving_left = False

    def draw(self):
        """draw the ship"""
        self.screen.blit(self.image, self.rect)

    def update_position(self):
        """Update position based on movement flags"""
        right_max = self.screen_rect.right
        left_min  = 0

        if self.moving_right and self.rect.right < (right_max - int(5.0 * self.speed_factor)):
            self.rect.centerx += int(5.0 * self.speed_factor)
        if self.moving_left and self.rect.left > (left_min + int(5.0 * self.speed_factor)):
            self.rect.centerx -= int(5.0 * self.speed_factor)

    def center_ship(self):
        self.center = self.screen_rect.centerx


class AlienShip(Sprite):
    """A class to represent a single alien ship."""
    def __init__(self, game_settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = game_settings

        self.image = pg.image.load(os.path.join('Images','alien.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.speed_factor = 2.0

        # starting position -- top of left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # save as float
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def draw(self):
        self.screen.blit(self.image, self.rect)


    def update_position(self):
        fleet_direction = self.settings.fleet_direction
        self.x += self.speed_factor * fleet_direction
        self.rect.x = self.x


    def check_screen_edge(self):
        """Return True if at screen edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def increase_gamespeed(self):
        self.speed_factor *= self.settings.level_speedup
