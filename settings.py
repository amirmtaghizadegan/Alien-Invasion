class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # Ship settings
        self.ship_limit = 3


        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 4

        # Bar settings
        self.bar_width = 260
        self.bar_height = 20
        self.bar_color = [230, 230, 230]

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 2.21
        self.bullet_speed = 1.1
        self.alien_speed = 0.51

        # fleet_direction of 1 represents right and -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50
        self.score_scale = 1.5


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
