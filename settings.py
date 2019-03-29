from typing import List, Dict, Tuple

class Settings():
    """A class to store components of the Alien Invasion game."""
    def __init__(self, screen_width: int, screen_height: int, bg_colors: Tuple[int, int, int],
                 gm_caption: str):
        # screen settings
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bg_colors = bg_colors
        self.gm_caption = gm_caption

        # game settings
        self.ship_limit = 3
        self.level_speedup = 1.25

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = 180, 10, 10
        self.max_bullets = 25
        self.reset_settings()


    def reset_settings(self):
        self.bullet_speed_factor = 3
        # alien settings
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.hit_points = 50

    def increase_gamespeed(self):
        self.bullet_speed_factor *= self.level_speedup
        self.fleet_drop_speed    *= self.level_speedup
        self.hit_points = int(self.hit_points * self.level_speedup ** 2)
