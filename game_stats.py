import pygame as pg
import pygame.font
from pygame.sprite import Sprite
from pygame.sprite import Group

from ship import Ship

class GameStats():
    """Track scoring and statistics for game"""
    def __init__(self, game_settings):
        self.game_active = False
        self.settings = game_settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.game_level = 1


class Scoreboard():
    def __init__(self, game_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = game_settings
        self.stats = stats
        self.text_color = (0, 255, 0)
        self.font = pygame.font.SysFont("comicsansms", 32)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Render image of scoreboard"""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(
            "Score: " + score_str, True, self.text_color, self.settings.bg_colors
        )

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(
            "High Score: " + score_str, True, self.text_color, self.settings.bg_colors
        )

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx - 20
        self.high_score_rect.top = 20


    def prep_level(self):
        self.level_image = self.font.render(
            "Level: " + str(self.stats.game_level), True, self.text_color, self.settings.bg_colors
        )

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = 10
        self.level_rect.top = 20

    def prep_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            s = Ship(self.settings, self.screen)
            s.rect.x = self.level_rect.right + 10 + i * s.rect.width
            s.rect.top = 20
            self.ships.add(s)


    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


class Button():
    """A rectangular label for starting  the game."""
    def __init__(self, game_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 300, 75
        self.color = (0, 0, 255) # green
        self.text_color = (255, 255, 255) # white
        self.font = pygame.font.SysFont("comicsansms", 32)

        # build/center object
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)


    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
