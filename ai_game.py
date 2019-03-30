import sys
import pygame as pg
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from ship import AlienShip
from game_stats import GameStats
from game_stats import Scoreboard
from game_stats import Button
from pygame.sprite import Group

# primary game functions
# ---------------------------------------------------------
def fire_bullet(game_settings, screen, ship, bullets):
    """Fire Bullets on user action"""
    if len(bullets) < game_settings.max_bullets:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(game_settings, stats, screen, sb, ship, bullets, aliens):
    bullets.update()
    for b in bullets.sprites():
        b.update_position()
    for b in bullets.copy(): # use copy() so that we don't delete w/in for-loop
        if b.rect.bottom <= 0:
            bullets.remove(b) # no delete

    check_bullet_hit(game_settings, stats, screen, sb, ship, bullets, aliens)


def check_bullet_hit(game_settings, stats, screen, sb, ship, bullets, aliens):
    hit = pg.sprite.groupcollide(bullets, aliens, True, True)

    if hit:
        for aliens in hit.values():
            stats.score += game_settings.hit_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)

    # When zero aliens remain, prep the next level
    if len(aliens) == 0:
        bullets.empty()
        game_settings.increase_gamespeed()
        for a in aliens:
            a.increase_gamespeed()
        stats.game_level += 1
        sb.prep_level()
        create_fleet(game_settings, screen, aliens)


def create_fleet(game_settings, screen, aliens):
    """Create a fleet of aliens"""
    # determine fleet size
    alien = AlienShip(game_settings, screen)
    alien_x = alien.rect.width
    alien_y = alien.rect.height

    space_x = int(game_settings.screen_width - alien_x)
    space_y = int(game_settings.screen_height * 0.5)
    ncols = int(space_x / (2 * alien_x)) + 1  # number of aliens in a row
    nrows = int(space_y / (alien_y * 1.5)) # number of rows of aliens

    # create fleet
    for r in range(nrows):
        for c in range(ncols):
            new_alien = AlienShip(game_settings, screen)
            new_alien.x = alien_x + (2 * alien_x * c)
            new_alien.y = alien_y + (2 * alien_y * r)
            new_alien.rect.x = new_alien.x
            new_alien.rect.y = new_alien.y
            aliens.add(new_alien) # add to group


def check_fleet_edges(game_settings, aliens):
    """return True if any alien at screen edge"""
    for a in aliens.sprites():
        if a.check_screen_edge():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    for a in aliens.sprites():
        a.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def update_aliens(game_settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(game_settings, aliens)
    for a in aliens:
        a.update_position()

    if pg.sprite.spritecollideany(ship, aliens):
        print("Hull breach!!! Get to your escape pods... We're all gonna die!")
        ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(game_settings, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()

        create_fleet(game_settings, screen, aliens)
        ship.center_ship()

        # pause
        sleep(1.0)
    else:
        stats.game_active = False


def check_event_keyup(event, ship):
    "modify ship position based on key releases"
    if event.key == pg.K_RIGHT:
        ship.moving_right = False
    elif event.key == pg.K_LEFT:
        ship.moving_left = False


def check_event_keydown(event, game_settings, stats, screen, ship, bullets):
    "modify ship position based on key presses"
    if event.key == pg.K_RIGHT:
        ship.moving_right = True
    elif event.key == pg.K_LEFT:
        ship.moving_left = True
    elif event.key == pg.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pg.K_q:
        stats.write_high_score()
        sys.exit()

def check_play_button(game_settings, stats, screen, sb, ship, bullets, aliens, play_button,
                      mouse_x, mouse_y):
    """Respond to play button activity"""
    playing = play_button.rect.collidepoint(mouse_x, mouse_y)
    if playing and not stats.game_active:
        # reset game stats
        game_settings.reset_settings()
        stats.reset_stats()
        stats.game_active = True

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        # reset objects
        aliens.empty()
        bullets.empty()
        create_fleet(game_settings, screen, aliens)
        ship.center_ship()


def check_events(game_settings, stats, screen, sb, ship, bullets, aliens, play_button):
    """Wrapper for event functionality"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            stats.write_high_score()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            check_event_keydown(event, game_settings, stats, screen, ship, bullets)
        elif event.type == pg.KEYUP:
            check_event_keyup(event, ship)
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(game_settings, stats, screen, sb, ship, bullets, aliens, play_button,
                                  mouse_x, mouse_y)


def update_screen(game_settings, stats, screen, sb, ship, bullets, aliens, play_button):
    screen.fill(game_settings.bg_colors)

    for b in bullets.sprites():
        b.draw()
    for a in aliens.sprites():
        a.draw()
    ship.draw()
    sb.draw()

    if not stats.game_active:
        play_button.draw()
    pg.display.flip()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



# run the game
# --------------------------------------------------------
def run_game():
    """The main function for running the game Alien Invasion."""

    # 01. Settings and initialization
    pg.init()
    game_settings = Settings(1000, 800, (50,50,50), 'Alien Invasion')
    stats = GameStats(game_settings)

    screen = pg.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height)
    )
    pg.display.set_caption(game_settings.gm_caption)

    play_button = Button(game_settings, screen, "Defeat the Aliens!!")
    sb = Scoreboard(game_settings, screen, stats)
    ship = Ship(game_settings, screen)
    bullets = Group()
    aliens = Group()
    create_fleet(game_settings, screen, aliens)

    # 02. Primary game-play conditions
    while True:
        check_events(game_settings, stats, screen, sb, ship, bullets, aliens, play_button)
        update_screen(game_settings, stats, screen, sb, ship, bullets, aliens, play_button)

        if stats.game_active:
            update_bullets(game_settings, stats, screen, sb, ship, bullets, aliens)
            ship.update_position()
            update_aliens(game_settings, stats, screen, sb, ship, aliens, bullets)


# execute
run_game()
