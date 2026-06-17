# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
import os
import random
import pygame
from pygame import draw
from utilities import button

# pygame setup
pygame.init()

# Define constants
bottom_panel = 360
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
run = True
dt = 0
target_fps = 144

# define game variables
player_mode = 0  # default to attack mode

enemy_defence_chance = 0.33  # 33% chance for enemy to defend

# d efence chances
partial_block_min = 0.45
partial_block_max = 0.65
full_block_chance = 0.20
counter_chance = 0.10

current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
player_potion_effect = 16 + random.randint(-2, 10)
enemy_potion_effect = 9 + random.randint(-2, 5)
clicked = False
game_over = 0  # 0 = no winner, -1 = enemy win

# load fonts
font = pygame.font.SysFont("Times New Roman", 40)
mode_font = pygame.font.SysFont("Times New Roman", 20)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

# load images
_bg_size = (screen_width, screen_height - bottom_panel)
backround_img = pygame.transform.scale(
    pygame.image.load(
        "/workspaces/2026SE_MajorProject_Kelvin.A/assets/backgrounds/Background.gif"
    ).convert(),
    _bg_size,
)

# Load Panel
panel_img = pygame.transform.scale(
    pygame.image.load(
        "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/panel.png"
    ).convert_alpha(),
    (screen_width, bottom_panel),
)

# Load Potion
Potion_img = pygame.image.load(
    "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/Potion.png"
).convert_alpha()

# Load Katana
Katana_img = pygame.image.load(
    "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/Katana.png"
).convert_alpha()
Katana_img = pygame.transform.scale(
    Katana_img,
    (max(1, Katana_img.get_width() // 2), max(1, Katana_img.get_height() // 2)),
)

# load shield
Shield_img = pygame.image.load(
    "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/shield.png"
).convert_alpha()
Shield_scale = 0.28
Shield_img = pygame.transform.scale(
    Shield_img,
    (
        max(1, int(Shield_img.get_width() * Shield_scale)),
        max(1, int(Shield_img.get_height() * Shield_scale)),
    ),
)


# load Restart button
Restart_img = pygame.image.load(
    "/workspaces/2026SE_MajorProject_Kelvin.A/assets/ui/restart_button.png"
).convert_alpha()

# Anchor mouse position to tip
katana_hotspot = (8, 8)
shield_hotspot = (Shield_img.get_width() // 2, Shield_img.get_height() // 2)


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
        f"{Samurai.name} HP: {Samurai.hp}",
        font,
        red,
        80,
        screen_height - bottom_panel + 30,
    )
    # Go through ememy list and show stats
    for count, i in enumerate(Enemy_list):
        # show enemy stats
        draw_text(
            f"{i.name} HP: {i.hp}",
            font,
            red,
            1580,
            (screen_height - bottom_panel + 30) + count * 110,
        )


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
Samurai = Fighter(500, 600, "Samurai", 100, 14, 3)
Enemy1 = Fighter(1400, 600, "Enemy", 45, 8, 1, flip=True)
Enemy2 = Fighter(1650, 590, "Enemy", 45, 10000, 1, flip=True)

Enemy_list = []
Enemy_list.append(Enemy1)
Enemy_list.append(Enemy2)

Samurai_health_bar = HealthBar(
    80, screen_height - bottom_panel + 80, Samurai.hp, Samurai.max_hp
)
Enemy1_health_bar = HealthBar(
    1580, screen_height - bottom_panel + 80, Enemy1.hp, Enemy1.max_hp
)
Enemy2_health_bar = HealthBar(
    1580, screen_height - bottom_panel + 190, Enemy2.hp, Enemy2.max_hp
)

# set button rect for mode change
mode_button_rect = pygame.Rect(
    Enemy1_health_bar.x - 400, Enemy1_health_bar.y - 8, 140, 60
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
    Samurai_health_bar.draw(Samurai.hp)
    Enemy1_health_bar.draw(Enemy1.hp)
    Enemy2_health_bar.draw(Enemy2.hp)

    # draw fighters
    Samurai.update()
    Samurai.draw()
    for enemy in Enemy_list:
        enemy.update()
        enemy.draw()

    # draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # draw mode button
    draw_mode_button()

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
    draw_text(str(Samurai.potions), font, red, 190, screen_height - bottom_panel + 150)

    if game_over == 0:
        # check if player has died
        if Samurai.alive == False:
            game_over = -1
        # player action
        if Samurai.alive == True and current_fighter == 1:
            if Samurai.is_defending and Samurai.action == 4:
                Samurai.is_defending = False
                Samurai.idle()
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action

                # Defend
                if defend == True:
                    Samurai.defend()
                    current_fighter += 1
                    action_cooldown = 0

                # Attack
                if attack == True and target is not None:
                    was_alive = target.alive
                    Samurai.attack(target)

                    if was_alive and not target.alive:
                        Samurai.potions += 1

                    current_fighter += 1
                    action_cooldown = 0

                # use Potion
                if potion == True and Samurai.potions > 0:
                    # heal the player
                    if Samurai.hp + player_potion_effect < Samurai.max_hp:
                        heal_amount = player_potion_effect
                    else:
                        heal_amount = Samurai.max_hp - Samurai.hp
                    Samurai.hp += heal_amount
                    Samurai.potions -= 1
                    damage_text = DamageText(
                        Samurai.rect.centerx, Samurai.rect.y, str(heal_amount), green
                    )
                    damage_text_group.add(damage_text)

                    current_fighter += 1
                    action_cooldown = 0

        # enemy action
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
                        enemy.attack(Samurai)

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
            text_surface = font.render("SAMURAI SLAIN", False, yellow)
            text_rect = text_surface.get_rect(
                center=(screen_width // 2, screen_height // 2)
            )
            screen.blit(text_surface, text_rect)

        # Draw button
        if restart_button.draw(screen):
            Samurai.reset()
            for enemy in Enemy_list:
                enemy.reset()
            current_fighter = 1
            action_cooldown = 0
            game_over = 0

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
