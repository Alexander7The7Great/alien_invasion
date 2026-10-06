class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static default settings."""
        # Screen Settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.star_count = 50

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3


        self.dev_mode = False

        #Bullet settings
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #rain settings
        self.rain_speed = .5
        self.rain_width = 2
        self.rain_height = 30
        self.rain_color = (0, 0, 128)

        #Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        #how quickly the game speeds up
        self.speedup_scale = 1.05

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settins that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3
        self.alien_speed = 1.0

        #fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale