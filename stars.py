import sys

import pygame

from settings import Settings

from ship import Ship
from bullet import Bullet
from alien import Alien
from random import randint
import sys

class Star(pygame.sprite.Sprite):
    """A class to represent a single star in the background."""

    def __init__(self, ai_game):
        """Initialize the star and set its random starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = randint(0, self.screen_rect.height - self.rect.height)

    def draw_star(self):
        """Draw the star at its current location."""
        self.screen.blit(self.image, self.rect)
