class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        # Screen Settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.star_count = 50

        #ship settings
        self.ship_speed = 1.5


        self.dev_mode = False

        if self.dev_mode == True:
            self.bullet_width == 3000

        #Bullet settings
        self.bullet_speed = 2.0
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

    