import sys
from time import sleep

import pygame

from settings import Settings


from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Star
from random import randint
from rain import Rain
from game_stats import GameStats
from scoreboard import Scoreboard

from button import Button



class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #Start Alien Invasion in the inactive state
        self.game_active = False

        

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        
        self.rain = pygame.sprite.Group()
        self._create_rain()

        self._create_fleet()
        self.stars = pygame.sprite.Group()
        self._create_stars()

        #Play button
        self.play_button = Button(self, "Play")

        #Start Alien Invasion in an active state
        #self.game_active = True

        



    def _create_stars(self):
                """Create a field of randomly placed stars"""
                for _ in range(self.settings.star_count):
                    new_star = Star(self)
                    self.stars.add(new_star)

        
    def run_game(self):
        """Start the main loop for the game. """
        while True:
            # watch for keyboard and mouse events.
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_rain()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(120)
            # Redraw the screen during each pas through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self.settings.dev_mode = not self.settings.dev_mode
        

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of the old"""
        self.bullets.update()

        #get rid of bullets that have disapeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_play_button(self, mouse_pos):
        """Start new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            #Game Reset
            self.stats.reset_stats()
            self.game_active = True

            #Ridding the bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet while centering the ship
            self._create_fleet()
            self.ship.center_ship()

            #Mouse hidden
            pygame.mouse.set_visible(False)

        else:
            pygame.mouse.set_visible(True)
            
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens: 
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        

    def _create_drop(self, x_position, y_position):
        """Create rain and place in row"""
        new_rain = Rain(self)
        new_rain.y = y_position
        new_rain.rect.x = randint(0, self.settings.screen_width)
        new_rain.rect.y = y_position
        self.rain.add(new_rain)

    def _create_rain(self):
        """Create the down pour"""
                 
        rain = Rain(self)
        rain_width, rain_height = rain.rect.size
        
        current_x, current_y = rain_width, rain_height
        while current_y < (self.settings.screen_height - 2 * rain_height):
            while current_x < (self.settings.screen_width - 3 * rain_width):
                self._create_drop(current_x, current_y)
                current_x += 40 * rain_width
        
            #Finished a row; reset x value, and increment y value
            current_x = rain_width
            current_y += 2 * rain_height

    def _update_rain(self):
        self.rain.update()
        for rain in self.rain.copy():
            if rain.check_rain_bottom():
                rain.y = 0
                rain.rect.y = 0
                rain.rect.x = randint(0, self.settings.screen_width)
            
        

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            #Decrement ships_left
            self.stats.ships_left -= 1

            #Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(.5)
        else:
            self.game_active = False


    def _create_fleet(self):
         """Create the fleet of aliens."""
         #Create an alien and keep adding aliens until there is no more room left.
         #Spacing between aliens is no ealien width and one alien height
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size

         current_x, current_y = alien_width, alien_height
         while current_y < (self.settings.screen_height - 4 * alien_height):
             while current_x < (self.settings.screen_width - 3 * alien_width):
                 self._create_alien(current_x, current_y)
                 current_x += 2 * alien_width

            #Finished a row; reset x value, and increment y value
             current_x = alien_width
             current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the sccreen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break


    def _update_screen(self):
        """update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for star in self.stars.sprites():
            star.draw_star()
        for rain in self.rain.sprites():
            rain.draw_rain()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        #scoreboard
        self.sb.show_score()

        #Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
                    
        pygame.display.flip()
        

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()