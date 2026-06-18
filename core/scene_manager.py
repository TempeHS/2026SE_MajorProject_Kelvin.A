import math
import pygame


# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, False, text_col)
    screen.blit(img, (x, y))


# function to draw a background
def draw_bg():
    screen.blit(backround_img, (0, 0))


# funtion to draw panel
def draw_panel():
    # draw panel
    pygame.draw.rect(
        screen,
        (74, 45, 35),
        (0, screen_height - bottom_panel, screen_width, bottom_panel),
    )
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    # show player stats
    draw_text(
        f"{Player.name} HP: {Player.hp}",
        font,
        cyan,
        80,
        screen_height - bottom_panel + 30,
    )
    # Go through enemy list and show stats
    for count, i in enumerate(Enemy_list):
        # show enemy stats
        draw_text(
            f"{i.name} HP: {i.hp}",
            font,
            red,
            1580,
            (screen_height - bottom_panel + 30) + count * 110,
        )


# change mode button
def draw_mode_button():
    if player_mode == 0:
        fill = (170, 50, 50)
        mode_text = "ATTACKING"
    else:
        fill = (50, 120, 170)
        mode_text = "DEFENDING"

    pygame.draw.rect(screen, fill, mode_button_rect, border_radius=12)
    pygame.draw.rect(screen, white, mode_button_rect, 3, border_radius=12)

    label_img = mode_font.render(mode_text, True, white)
    label_rect = label_img.get_rect(center=mode_button_rect.center)
    screen.blit(label_img, label_rect)


def draw_black_box_turn_indicator():
    # Draw a black box behind the turn indicator
    box_width = 175
    box_height = 50
    box_x = 10
    box_y = 10
    pygame.draw.rect(
        screen, (0, 0, 0), (box_x, box_y, box_width, box_height), border_radius=8
    )


# indicates whos turn it is
def draw_turn_indicator():
    if current_fighter == 1:
        text = "Player's Turn"
    else:
        # display name of enemy Sakata/Gintoki
        text = f"{Enemy_list[current_fighter - 2].name}'s Turn"

    # skip indication if the enemy is dead.
    if current_fighter > 1 and not Enemy_list[current_fighter - 2].alive:
        text = f"{Enemy_list[current_fighter - 2].name} is dead"

    # red enemy text, cyan player text
    if current_fighter == 1:
        label_img = mode_font.render(text, True, cyan)
    else:
        label_img = mode_font.render(text, True, red)

    # should be on the top left of the screen
    label_rect = label_img.get_rect(topleft=(20, 20))
    screen.blit(label_img, label_rect)

    # draw indicator arrow next to the left of the current_fighter
    if current_fighter > 1:
        enemy_rect = Enemy_list[current_fighter - 2].rect
        arrow_x = enemy_rect.left - Indicator_img.get_width() + 5
        arrow_y = enemy_rect.centery - Indicator_img.get_height() // 2

    else:
        # point to player
        player_rect = Player.rect
        arrow_x = player_rect.left - Indicator_img.get_width() + 5
        arrow_y = player_rect.centery - Indicator_img.get_height() // 2

    # animate indicator bob left and right slightly
    bob_amount = 5
    bob_speed = 0.005
    bob_offset = bob_amount * math.sin(pygame.time.get_ticks() * bob_speed)
    screen.blit(Indicator_img, (arrow_x + bob_offset, arrow_y))


def draw_game_over_overlay(
    screen, game_over, screen_width, screen_height, font, yellow, cyan
):
    if game_over == -1:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
        text_surface = font.render("PLAYER SLAIN", False, yellow)
        text_rect = text_surface.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        screen.blit(text_surface, text_rect)

    if game_over == 1:
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
        text_surface = font.render("ENEMIES SLAIN", False, cyan)
        text_rect = text_surface.get_rect(
            center=(screen_width // 2, screen_height // 2)
        )
        screen.blit(text_surface, text_rect)


def draw_restart_label(screen, font, red, restart_img, screen_width, screen_height):
    button_x = screen_width // 2 - restart_img.get_width() // 2
    button_y = screen_height // 2 + 50
    label = font.render("RESTART", True, red)
    label = pygame.transform.scale(
        label, (label.get_width() // 1.5, label.get_height() // 1.5)
    )
    label_rect = label.get_rect(
        center=(
            button_x + restart_img.get_width() // 2,
            button_y + restart_img.get_height() // 2,
        )
    )
    screen.blit(label, label_rect)
