# WAIT FOR postCreateCommand TO RUN FIRST
# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
# WAIT FOR PORT 6080 TO RUN
import os

os.environ["SDL_RENDER_DRIVER"] = "software"

import pygame
from utilities import button

from core.scene_manager import (
    draw_text,
    draw_bg,
    draw_panel,
    draw_mode_button,
    draw_black_box_turn_indicator,
    draw_turn_indicator,
    draw_game_over_overlay,
    draw_restart_label,
)
from entities.enemy import clear_enemy_defend_state, perform_enemy_action
from entities.player import Fighter, HealthBar, DamageText, configure_player_module
from core.game import init_db, save_match_result
from core.settings import (
    Bottom_Panel,
    Screen_Width,
    Screen_Height,
    Target_fps,
    Player_mode_default,
    Enemy_defence_chance,
    Partial_block_min,
    Partial_block_max,
    Full_block_chance,
    Counter_chance,
    Current_fighter_default,
    Total_fighters,
    Action_cooldown_default,
    Action_wait_time,
    Player_potion_effect,
    Enemy_potion_effect,
    Game_over_default,
    Red,
    Green,
    Yellow,
    White,
    Cyan,
)

from utilities.resource_loader import load_fonts, load_images, get_cursor_hotspots

# pygame setup
pygame.init()

# Define constants
bottom_panel = Bottom_Panel
screen_width = Screen_Width
screen_height = Screen_Height
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
run = True
dt = 0
target_fps = Target_fps

# define game variables
player_mode = Player_mode_default  # default to attack mode

enemy_defence_chance = Enemy_defence_chance  # 33% chance for enemy to defend

# defence chances
partial_block_min = Partial_block_min
partial_block_max = Partial_block_max
full_block_chance = Full_block_chance
counter_chance = Counter_chance

current_fighter = Current_fighter_default
total_fighters = Total_fighters
action_cooldown = Action_cooldown_default
action_wait_time = Action_wait_time
attack = False
potion = False
player_potion_effect = Player_potion_effect
enemy_potion_effect = Enemy_potion_effect
clicked = False
game_over = Game_over_default  # 0 = no winner, -1 = enemy win, 1 = player win

cursor_visible = True
pygame.mouse.set_visible(cursor_visible)

# load fonts
font, mode_font = load_fonts()

# define colours
red = Red
green = Green
yellow = Yellow
white = White
cyan = Cyan

(
    backround_img,
    panel_img,
    Potion_img,
    Katana_img,
    Shield_img,
    Indicator_img,
    Restart_img,
) = load_images(screen_width, screen_height, bottom_panel)

# Anchor mouse position to tip
katana_hotspot, shield_hotspot = get_cursor_hotspots(Shield_img)

result_saved = False

damage_text_group = pygame.sprite.Group()

configure_player_module(
    screen,
    font,
    red,
    green,
    yellow,
    white,
    partial_block_min,
    partial_block_max,
    full_block_chance,
    counter_chance,
    damage_text_group,
)

# Fighter Locations and stats
Player = Fighter(500, 600, "Samurai", 100, 14, 3)
Gintoki = Fighter(1400, 600, "Gintoki", 85, 11, 2, flip=True)
Sakata = Fighter(1650, 590, "Sakata", 60, 8, 1, flip=True)

Enemy_list = []
Enemy_list.append(Gintoki)
Enemy_list.append(Sakata)

Player_health_bar = HealthBar(
    80, screen_height - bottom_panel + 80, Player.hp, Player.max_hp
)
Gintoki_health_bar = HealthBar(
    1580, screen_height - bottom_panel + 80, Gintoki.hp, Gintoki.max_hp
)
Sakata_health_bar = HealthBar(
    1580, screen_height - bottom_panel + 190, Sakata.hp, Sakata.max_hp
)

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

# init database
init_db()

while run:

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode_button_rect.collidepoint(event.pos):
                if player_mode == 0:
                    player_mode = 1
                elif player_mode == 1:
                    player_mode = 0
            else:
                clicked = True

    screen.fill((0, 0, 0))

    # draw background
    draw_bg(screen, backround_img)

    # draw panel
    draw_panel(
        screen,
        panel_img,
        Player,
        Enemy_list,
        font,
        cyan,
        red,
        screen_width,
        screen_height,
        bottom_panel,
    )
    Player_health_bar.draw(Player.hp)
    Gintoki_health_bar.draw(Gintoki.hp)
    Sakata_health_bar.draw(Sakata.hp)

    # draw fighters
    Player.update()
    Player.draw()
    for enemy in Enemy_list:
        enemy.update()
        enemy.draw()

    # draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # draw mode button
    draw_mode_button(screen, player_mode, mode_button_rect, mode_font, white)
    # draw black box behind turn indicator
    draw_black_box_turn_indicator(screen)
    # draw turn indicator
    draw_turn_indicator(
        screen, current_fighter, Player, Enemy_list, mode_font, cyan, red, Indicator_img
    )

    # control player actions
    # reset action var
    attack = False
    potion = False
    target = None
    defend = False

    pos = pygame.mouse.get_pos()

    if player_mode == 1 and clicked:
        defend = True

    if player_mode == 0:
        for count, enemy in enumerate(Enemy_list):
            hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
            if enemy.alive and hover_rect.collidepoint(pos):
                if clicked == True:
                    attack = True
                    target = Enemy_list[count]
                break

    if health_potion_button.draw(screen):
        potion = True
    # no. of potions shown in panel
    draw_text(
        screen,
        str(Player.potions),
        font,
        cyan,
        80,
        screen_height - bottom_panel + 120,
    )

    if game_over == 0:
        # check if player has died
        if Player.alive == False:
            game_over = -1
        # player action
        if Player.alive == True and current_fighter == 1:
            if Player.is_defending and Player.action == 4:
                Player.is_defending = False
                Player.idle()
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action

                # Defend
                if defend == True:
                    Player.defend()
                    current_fighter += 1
                    action_cooldown = 0

                # Attack
                if attack == True and target is not None:
                    was_alive = target.alive
                    Player.attack(target)

                    if was_alive and not target.alive:
                        Player.potions += 1

                    current_fighter += 1
                    action_cooldown = 0

                # use Potion
                if potion == True and Player.potions > 0:
                    # heal the player
                    if Player.hp + player_potion_effect < Player.max_hp:
                        heal_amount = player_potion_effect
                    else:
                        heal_amount = Player.max_hp - Player.hp
                    Player.hp += heal_amount
                    Player.potions -= 1
                    damage_text = DamageText(
                        Player.rect.centerx, Player.rect.y, str(heal_amount), green
                    )
                    damage_text_group.add(damage_text)

                    current_fighter += 1
                    action_cooldown = 0

        # enemy action
        # check if all enemys are dead
        # enemy action
        if any(enemy.alive for enemy in Enemy_list) == False:
            game_over = 1

        # Save match result to database
        if game_over != 0 and result_saved == False:
            match_outcome = "WIN" if game_over == 1 else "LOSS"
            save_match_result(match_outcome, Player.hp, Gintoki.hp, Sakata.hp)
            result_saved = True

        for count, enemy in enumerate(Enemy_list):
            if current_fighter == 2 + count:
                if enemy.alive == False:
                    current_fighter += 1
                    action_cooldown = 0
                    continue

                action_cooldown += 1
                if action_cooldown < action_wait_time:
                    continue

                # clear defend state if enemy was defending last turn
                clear_enemy_defend_state(enemy)

                perform_enemy_action(
                    enemy,
                    Player,
                    enemy_potion_effect,
                    enemy_defence_chance,
                    damage_text_group,
                    DamageText,
                    green,
                )

                current_fighter += 1
                action_cooldown = 0
                break  # only one enemy acts per turn

        # reset turns if all have gone
        if current_fighter > total_fighters:
            current_fighter = 1

    # check for game over and reset
    else:
        draw_game_over_overlay(
            screen, game_over, screen_width, screen_height, font, yellow, cyan
        )

        # Draw button
        if restart_button.draw(screen):
            Player.reset()
            for enemy in Enemy_list:
                enemy.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0
            result_saved = False

            # clear states
            damage_text_group.empty()
            player_mode = Player_mode_default  # reset to default mode
            attack = False
            potion = False
            clicked = False

        # draws restart text
        draw_restart_label(screen, font, red, Restart_img, screen_width, screen_height)

    # Draw cursor replacement as the final render step for minimum latency.
    live_pos = pygame.mouse.get_pos()
    hovering_enemy = False
    for enemy in Enemy_list:
        hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
        if enemy.alive and hover_rect.collidepoint(live_pos):
            hovering_enemy = True
            break

    if player_mode == 1:  # DEFEND mode
        want_visible = False
        shield_pos = (live_pos[0] - shield_hotspot[0], live_pos[1] - shield_hotspot[1])
        screen.blit(Shield_img, shield_pos)
    elif hovering_enemy:
        want_visible = False
        katana_pos = (live_pos[0] - katana_hotspot[0], live_pos[1] - katana_hotspot[1])
        screen.blit(Katana_img, katana_pos)
    else:
        want_visible = True

    # Only toggle OS cursor visibility when state changes
    if want_visible != cursor_visible:
        pygame.mouse.set_visible(want_visible)
        cursor_visible = want_visible

    pygame.display.flip()
    dt = clock.tick(target_fps) / 1000

pygame.quit()
