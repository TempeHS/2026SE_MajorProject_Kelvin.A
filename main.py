# WAIT FOR postCreateCommand TO RUN FIRST
# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
# WAIT FOR PORT 6080 TO RUN
import os

# Set SDL to use a renderer that doesn't require hardware accel
os.environ["SDL_RENDER_DRIVER"] = "software"

import pygame

from scripts.collision import player_action, hovering_enemy
from scripts.spawner import create_fighters, create_health, create_buttons
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
from entities.enemy import enemy_turns
from entities.player import (
    Fighter,
    HealthBar,
    DamageText,
    configure_player_module,
    player_turn,
)
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


def run_game():

    # pygame setup
    pygame.init()

    # Define constants
    bottom_panel = Bottom_Panel
    screen_width = Screen_Width
    screen_height = Screen_Height
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    run = True
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
    Player, gintoki, sakata, Enemy_list = create_fighters(Fighter)

    # Create health bars
    Player_health_bar, gintoki_health_bar, sakata_health_bar = create_health(
        Player, gintoki, sakata, HealthBar, screen_height, bottom_panel
    )
    # Create buttons
    mode_button_rect, health_potion_button, restart_button = create_buttons(
        screen_width,
        screen_height,
        bottom_panel,
        gintoki_health_bar,
        Potion_img,
        Restart_img,
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
        gintoki_health_bar.draw(gintoki.hp)
        sakata_health_bar.draw(sakata.hp)

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
            screen,
            current_fighter,
            Player,
            Enemy_list,
            mode_font,
            cyan,
            red,
            Indicator_img,
        )

        # control player actions
        # reset action var
        potion = False
        pos = pygame.mouse.get_pos()
        attack, defend, target = player_action(player_mode, clicked, Enemy_list, pos)

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
            # player action turn
            current_fighter, action_cooldown = player_turn(
                Player,
                current_fighter,
                action_cooldown,
                action_wait_time,
                defend,
                attack,
                target,
                potion,
                player_potion_effect,
                damage_text_group,
                DamageText,
                green,
            )

            # check if player has died
            if Player.alive is False:
                game_over = -1

            # check if all enemies are dead
            if any(enemy.alive for enemy in Enemy_list) is False:
                game_over = 1

            # Save match result to database
            if game_over != 0 and result_saved is False:
                match_outcome = "WIN" if game_over == 1 else "LOSS"
                save_match_result(match_outcome, Player.hp, gintoki.hp, sakata.hp)
                result_saved = True

            # enemy turns
            current_fighter, action_cooldown = enemy_turns(
                Enemy_list,
                Player,
                current_fighter,
                action_cooldown,
                action_wait_time,
                enemy_potion_effect,
                enemy_defence_chance,
                damage_text_group,
                DamageText,
                green,
            )

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
            draw_restart_label(
                screen, font, red, Restart_img, screen_width, screen_height
            )

        # Draw cursor replacement as the final render step for minimum latency.
        live_pos = pygame.mouse.get_pos()
        is_hovering_enemy = hovering_enemy(Enemy_list, live_pos)

        if player_mode == 1:  # DEFEND mode
            want_visible = False
            shield_pos = (
                live_pos[0] - shield_hotspot[0],
                live_pos[1] - shield_hotspot[1],
            )
            screen.blit(Shield_img, shield_pos)
        elif is_hovering_enemy:
            want_visible = False
            katana_pos = (
                live_pos[0] - katana_hotspot[0],
                live_pos[1] - katana_hotspot[1],
            )
            screen.blit(Katana_img, katana_pos)
        else:
            want_visible = True

        # Only toggle OS cursor visibility when state changes
        if want_visible != cursor_visible:
            pygame.mouse.set_visible(want_visible)
            cursor_visible = want_visible

        pygame.display.flip()
        clock.tick(target_fps)

    pygame.quit()


if __name__ == "__main__":
    run_game()
