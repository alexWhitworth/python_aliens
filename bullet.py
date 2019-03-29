
import pygame as pg
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from ships in-game"""

    def __init__(self, game_settings, screen, ship):
        """Bullets begin at the ship that fired them"""
        super().__init__()
        self.screen = screen

        # Create bullet rect at (0, 0), then set correct position.
        self.rect = pg.Rect(
            0, 0, game_settings.bullet_width, game_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store a decimal value for the bullet's position.
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update_position(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw(self):
        """Draw the bullet to the screen."""
        pg.draw.rect(self.screen, self.color, self.rect)
