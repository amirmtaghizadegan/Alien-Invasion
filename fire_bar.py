import pygame as pg


class Bar:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.height = ai_game.settings.bar_height
        self.width = (self.screen_rect.width - ai_game.settings.bar_width) / 2
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.midtop = self.screen_rect.midtop
        self.settings = ai_game.settings
        self.color = self.settings.bar_color
        self.init_color = self.settings.bar_color[:]


    def update(self, bullet_count):
        # print(bullet_count / self.settings.bullets_allowed)
        self.color[0] = self.init_color[0] + bullet_count * (255 - self.init_color[0]) / self.settings.bullets_allowed
        self.color[1] = self.init_color[1] - bullet_count * self.init_color[1] / self.settings.bullets_allowed
        self.color[2] = self.init_color[2] - bullet_count * self.init_color[2] / self.settings.bullets_allowed

    def draw(self):
        """Draw the bullet to the screen. """
        pg.draw.rect(self.screen, self.color, self.rect)
