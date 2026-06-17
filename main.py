# WAIT FOR postCreateCommand TO RUN FIRST
# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
# WAIT FOR PORT 6080 TO RUN
import math
import os
import random
from pygame import draw
import pygame
from utilities import button
import sqlite3

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


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS match_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                outcome TEXT NOT NULL CHECK (outcome IN ('WIN', 'LOSS')),
                player_hp INTEGER NOT NULL CHECK (player_hp >= 0),
                gintoki_hp INTEGER NOT NULL CHECK (gintoki_hp >= 0),
                sakata_hp INTEGER NOT NULL CHECK (sakata_hp >= 0)
            );
            """)
        conn.commit()


def save_match_result(outcome, player_hp, gintoki_hp, sakata_hp):
    with sqlite3.connect(DB) as conn:
        conn.execute(
            """
            INSERT INTO match_results (outcome, player_hp, gintoki_hp, sakata_hp)
            VALUES (?, ?, ?, ?)
            """,
            (outcome, max(0, player_hp), max(0, gintoki_hp), max(0, sakata_hp)),
        )
        conn.commit()


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


# Class for all fighters in the game (player and enemies)
class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions, flip=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.is_defending = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Attack, 2: Hurt, 3: Death, 4: Defend
        # Load Idle images
        temp_list = []
        self.update_time = pygame.time.get_ticks()
        idle_path = (
            f"/workspaces/2026SE_MajorProject_Kelvin.A/assets/sprites/{self.name}/Idle"
        )
        frame_count = len([f for f in os.listdir(idle_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{idle_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load all Attack_* variant images
        base_path = (
            f"/workspaces/2026SE_MajorProject_Kelvin.A/assets/sprites/{self.name}"
        )
        self.attack_variants = []
        attack_folders = sorted(
            [d for d in os.listdir(base_path) if d.startswith("Attack_")]
        )
        for folder in attack_folders:
            temp_list = []
            attack_path = f"{base_path}/{folder}"
            frame_count = len(
                [f for f in os.listdir(attack_path) if f.endswith(".png")]
            )
            for i in range(1, frame_count + 1):
                img = pygame.image.load(f"{attack_path}/{i}.png").convert_alpha()
                img = pygame.transform.scale(
                    img, (img.get_width() * 3, img.get_height() * 3)
                )
                img = img.subsurface(img.get_bounding_rect()).copy()
                if flip:
                    img = pygame.transform.flip(img, True, False)
                temp_list.append(img)
            self.attack_variants.append(temp_list)
        # Set a random attack
        self.animation_list.append(random.choice(self.attack_variants))
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

        # Load hurt animation
        temp_list = []
        hurt_path = f"{base_path}/Hurt"
        frame_count = len([f for f in os.listdir(hurt_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{hurt_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load death animation
        temp_list = []
        death_path = f"{base_path}/Death"
        frame_count = len([f for f in os.listdir(death_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{death_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load defend animation
        temp_list = []
        defend_path = f"{base_path}/Defend"
        frame_count = len([f for f in os.listdir(defend_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{defend_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def pick_attack(self):
        # Randomly select an Attack_* variant for the next attack
        self.animation_list[1] = random.choice(self.attack_variants)
        self.frame_index = 0

    def update(self):
        animation_cooldown = 140
        # Handle animation
        # Dead fighters stay dead
        if not self.alive and self.action != 3:
            self.death()
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check the time before updating animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset to start if animation has reached the end
        # Reset to start if animation has reached the end
        if self.frame_index >= len(self.animation_list[self.action]):
            # Death stays on last frame forever
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1

            # Defend stays on last frame only while defending
            elif self.action == 4:
                if self.is_defending:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()

            # Attack/Hurt finish, then either return to defend-hold or idle
            elif self.action in (1, 2):
                if self.is_defending:
                    self.action = 4
                    self.frame_index = len(self.animation_list[4]) - 1
                    self.update_time = pygame.time.get_ticks()
                else:
                    self.idle()

            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):

        # Base damage
        rand = random.randint(-3, 3)
        base_damage = self.strength + rand

        # Global cri chance
        crit_chance = 0.15  # 15%
        is_critical = random.random() < crit_chance

        # Calculate damage x crit
        if is_critical:
            raw_damage = int(base_damage * 1.5)
        else:
            raw_damage = base_damage

        damage, defense_result, counter_damage = target.guard_damage(raw_damage, self)

        # Apply damage to target
        if damage > 0:
            target.hp -= damage
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            else:
                target.hurt()

        # Damage / defense floating text
        if defense_result == "Blocked":
            damage_text_group.add(
                DamageText(target.rect.centerx, target.rect.y, "BLOCK", white)
            )
        elif defense_result == "Countered":
            damage_text_group.add(
                DamageText(target.rect.centerx, target.rect.y, "COUNTER", yellow)
            )
            if counter_damage > 0:
                damage_text_group.add(
                    DamageText(
                        self.rect.centerx, self.rect.y, str(counter_damage), yellow
                    )
                )
        else:
            # show damage text / colour
            if is_critical:
                damage_colour = yellow
            else:
                damage_colour = red

            # Sylise crit marker
            if is_critical:
                damage_display = f"{damage}!"
            else:
                damage_display = str(damage)

            damage_text = DamageText(
                target.rect.centerx, target.rect.y, damage_display, damage_colour
            )
            damage_text_group.add(damage_text)

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set hurt method
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set death method
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Anchor to the bottom of the image
        draw_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        screen.blit(self.image, draw_rect)

    def reset(self):
        self.alive = True
        self.is_defending = False
        self.hp = self.max_hp
        self.potions = self.start_potions
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    # set defending state and return to idle animation
    def defend(self):
        self.is_defending = True
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def guard_damage(self, incoming_damage, attacker):
        # default no defense active
        if self.is_defending == False:
            return incoming_damage, "Hit", 0

        roll = random.random()

        # Counter attack chance
        if roll < counter_chance:
            # play attack
            self.pick_attack()
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            counter_damage = max(1, int(self.strength * 0.6) + random.randint(-2, 2))
            attacker.hp -= counter_damage
            if attacker.hp < 1:
                attacker.hp = 0
                attacker.alive = False
                attacker.death()
            else:
                attacker.hurt()
            return 0, "Countered", counter_damage

        if roll < counter_chance + full_block_chance:
            return 0, "Blocked", 0

        taken_ratio = random.uniform(partial_block_min, partial_block_max)
        reduced = max(1, int(incoming_damage * taken_ratio))
        return reduced, "Partial", 0


# Health bar class to show health of player and enemies
class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        ratio = hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 200 * ratio, 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # text hovers upwards
        self.rect.y -= 1
        # remove the text after it has moved a certain distance
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

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
                if enemy.is_defending and enemy.action == 4:
                    enemy.is_defending = False
                    enemy.idle()

                # low HP -> potion
                if enemy.hp / enemy.max_hp < 0.5 and enemy.potions > 0:
                    if enemy.hp + enemy_potion_effect < enemy.max_hp:
                        heal_amount = enemy_potion_effect
                    else:
                        heal_amount = enemy.max_hp - enemy.hp

                    enemy.hp += heal_amount
                    enemy.potions -= 1
                    damage_text = DamageText(
                        enemy.rect.centerx,
                        enemy.rect.y,
                        str(heal_amount),
                        green,
                    )
                    damage_text_group.add(damage_text)

                # otherwise defend or attack
                else:
                    if random.random() < enemy_defence_chance:
                        enemy.defend()
                    else:
                        enemy.pick_attack()
                        enemy.attack(Player)

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
