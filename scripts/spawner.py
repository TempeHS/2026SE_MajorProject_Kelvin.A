import pygame
from utilities import button


def create_fighters(Fighter):
    Player = Fighter(500, 600, "Samurai", 100, 14, 3)
    Gintoki = Fighter(1400, 600, "Gintoki", 85, 11, 2, flip=True)
    Sakata = Fighter(1650, 590, "Sakata", 60, 8, 1, flip=True)

    enemy_list = [Gintoki, Sakata]
    return Player, enemy_list, Sakata, Gintoki


def create_health(Player, Gintoki, Sakata, HealthBar, screen_height, bottom_panel):
    Player_health_bar = HealthBar(
        80, screen_height - bottom_panel + 80, Player.hp, Player.max_hp
    )
    Gintoki_health_bar = HealthBar(
        1580, screen_height - bottom_panel + 80, Gintoki.hp, Gintoki.max_hp
    )
    Sakata_health_bar = HealthBar(
        1580, screen_height - bottom_panel + 190, Sakata.hp, Sakata.max_hp
    )
    return Player_health_bar, Gintoki_health_bar, Sakata_health_bar


def create_buttons(
    screen_width,
    screen_height,
    bottom_panel,
    Gintoki_health_bar,
    Potion_img,
    Restart_img,
):

    # set button rect for mode change
    mode_button_rect = pygame.Rect(
        Gintoki_health_bar.x - 400, Gintoki_health_bar.y - 8, 140, 60
    )

    # create buttons
    # Health potion
    health_potion_button = button.Button(
        80, screen_height - bottom_panel + 150, Potion_img, 0.3
    )
    
    # Restart button below Game Over text
    restart_button = button.Button(
        screen_width // 2 - Restart_img.get_width() // 2,
        screen_height // 2 + 50,
        Restart_img,
        1,
    )
    return mode_button_rect, health_potion_button, restart_button
