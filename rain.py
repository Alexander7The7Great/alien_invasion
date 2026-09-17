import sys

import pygame
from pygame.sprite import Sprite

from settings import Settings

from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
import sys

SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440

class Rain(pygame.sprite.Sprite):
    """A class to represent a rain in the background."""

    def __init__(self, ai_game):
        """Initialize the rain and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.rain_color

        #rain rect
        self.rect = pygame.Rect(0, 0, self.settings.rain_width, 
                                self.settings.rain_height)
        self.rect.midtop = (SCREEN_WIDTH // 2,0)

        self.y = float(self.rect.y)

    def check_rain_bottom(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.top > self.screen.get_rect().height)
        
    def update(self):
        """draw rain to screen"""
        self.y += self.settings.rain_speed 
        self.rect.y = self.y

    def draw_rain(self):
        pygame.draw.rect(self.screen, self.color, self.rect)