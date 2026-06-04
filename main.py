# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
import os
import random
import pygame

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
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False

# load fonts
font = pygame.font.SysFont("Times New Roman", 40)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)

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
# Load Katana
Katana_img = pygame.image.load(
    "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/Katana.png"
).convert_alpha()
Katana_img = pygame.transform.scale(
    Katana_img,
    (max(1, Katana_img.get_width() // 2), max(1, Katana_img.get_height() // 2)),
)
# Anchor mouse position to blade tip
katana_hotspot = (8, 8)


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
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Attack, 2: Defend 3: Run 4: Hurt, 5: Death
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

    def pick_attack(self):
        # Randomly select an Attack_* variant for the next attack
        self.animation_list[1] = random.choice(self.attack_variants)
        self.frame_index = 0

    def update(self):
        animation_cooldown = 140
        # Handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check the time before updating animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset to start if animation has reached the end
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage
        rand = random.randint(-3, 5)
        damage = self.strength + rand
        target.hp -= damage
        # if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Anchor to the bottom of the image
        draw_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        screen.blit(self.image, draw_rect)


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


# Fighter Locations and stats
Samurai = Fighter(500, 600, "Samurai", 100, 10, 3)
Enemy1 = Fighter(1400, 600, "Enemy", 40, 5, 2, flip=True)
Enemy2 = Fighter(1650, 590, "Enemy", 40, 5, 2, flip=True)

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

while run:

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
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

    # control player actions
    # reset action var
    attack = False
    potion = False
    target = None

    pos = pygame.mouse.get_pos()

    for count, enemy in enumerate(Enemy_list):
        hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
        if enemy.alive and hover_rect.collidepoint(pos):
            if clicked == True:
                attack = True
                target = Enemy_list[count]
            break

    # player action
    if Samurai.alive == True and current_fighter == 1:
        action_cooldown += 1
        if action_cooldown >= action_wait_time:
            # look for player action
            # Attack
            if attack == True and target is not None:
                Samurai.attack(target)
                current_fighter += 1
                action_cooldown = 0

    # enemy action
    for count, enemy in enumerate(Enemy_list):
        if current_fighter == 2 + count:
            if enemy.alive == True:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # Attack player
                    enemy.pick_attack()
                    enemy.attack(Samurai)
                    current_fighter += 1
                    action_cooldown = 0
            else:
                current_fighter += 1

    # reset turns if all have gone
    if current_fighter > total_fighters:
        current_fighter = 1

    # Draw cursor replacement as the final render step for minimum latency.
    live_pos = pygame.mouse.get_pos()
    hovering_enemy = False
    for enemy in Enemy_list:
        hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
        if enemy.alive and hover_rect.collidepoint(live_pos):
            hovering_enemy = True
            break

    if hovering_enemy:
        pygame.mouse.set_visible(False)
        katana_pos = (live_pos[0] - katana_hotspot[0], live_pos[1] - katana_hotspot[1])
        screen.blit(Katana_img, katana_pos)
    else:
        pygame.mouse.set_visible(True)

    pygame.display.flip()
    dt = clock.tick_busy_loop(target_fps) / 1000

pygame.quit()
