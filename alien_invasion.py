import sys
from time import sleep

import pygame as pg

from settings import Settings
from ship import Ship
from bullet import Bullet
from fire_bar import Bar
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pg.init()
        self.settings = Settings()

        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pg.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()
        self.bar = Bar(self)

        self.play_button = Button(self, "play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.bar.update(len(self.bullets))
            # Redraw the screen during each pass through the loop
            self._update_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.bar.draw()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.scoreboard.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # showing the configured screen
        pg.display.flip()


    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == pg.K_RIGHT:
            # Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_SPACE:
            self._fire_bullet()
        elif event.key == pg.K_ESCAPE:
            sys.exit()


    def _check_keyup_events(self, event):
        """Responds to key releases"""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        # Update bullet position.
        self.bullets.update()
        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        # check for any bullets that have hit aliens.
        #  If so, get rid of the bullet and the alien.
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()


    def _create_fleet(self):
        """create the fleet of aliens"""
        # make an alien.
        alien = Alien(self)
        self.aliens.add(alien)

        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of alien that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) -
                             ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)


    def _update_aliens(self):
        """update the position of all aliens in teh fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)

        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)





    def _check_aliens_bottom(self):
        """Checks if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the got hit.
                self._ship_hit()
                break


    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            pg.mouse.set_visible(False)


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
