# WAIT FOR postCreateCommand TO RUN FIRST
# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
# WAIT FOR PORT 6080 TO RUN
import math
from pygame import draw
import pygame
from utilities import button

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

# create database
DB = "/workspaces/2026SE_MajorProject_Kelvin.A/database/game.db"
result_saved = False


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
    draw_bg()

    # draw panel
    draw_panel()
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
    draw_mode_button()
    # draw black box behind turn indicator
    draw_black_box_turn_indicator()
    # draw turn indicator
    draw_turn_indicator()

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
    draw_text(str(Player.potions), font, white, 190, screen_height - bottom_panel + 150)

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
        if game_over == -1:
            draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
            text_surface = font.render("PLAYER SLAIN", False, yellow)
            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )
            screen.blit(text_surface, text_rect)
        if game_over == 1:
            draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
            text_surface = font.render("ENEMIES SLAIN", False, cyan)
            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )
            screen.blit(text_surface, text_rect)

        # Draw button
        if restart_button.draw(screen):
            Player.reset()
            for enemy in Enemy_list:
                enemy.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0
            result_saved = False

        # Draw restart text
        button_x = screen_width // 2 - Restart_img.get_width() // 2
        button_y = screen_height // 2 + 50
        label = font.render("RESTART", True, red)
        # half text size
        label = pygame.transform.scale(
            label, (label.get_width() // 1.5, label.get_height() // 1.5)
        )
        label_rect = label.get_rect(
            center=(
                button_x + Restart_img.get_width() // 2,
                button_y + Restart_img.get_height() // 2,
            )
        )
        screen.blit(label, label_rect)

    # Draw cursor replacement as the final render step for minimum latency.
    live_pos = pygame.mouse.get_pos()
    hovering_enemy = False
    for enemy in Enemy_list:
        hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
        if enemy.alive and hover_rect.collidepoint(live_pos):
            hovering_enemy = True
            break

    if player_mode == 1:  # DEFEND mode
        pygame.mouse.set_visible(False)
        shield_pos = (live_pos[0] - shield_hotspot[0], live_pos[1] - shield_hotspot[1])
        screen.blit(Shield_img, shield_pos)
    elif hovering_enemy:
        pygame.mouse.set_visible(False)
        katana_pos = (live_pos[0] - katana_hotspot[0], live_pos[1] - katana_hotspot[1])
        screen.blit(Katana_img, katana_pos)
    else:
        pygame.mouse.set_visible(True)

    pygame.display.flip()
    dt = clock.tick_busy_loop(target_fps) / 1000

pygame.quit()
