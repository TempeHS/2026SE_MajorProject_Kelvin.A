# USE THIS WHEN UPDATING/STARTING GAME TO LOAD IN VNC: bash start.sh
import os
import random
import pygame

# pygame setup
pygame.init()

bottom_panel = 360
screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
run = True
dt = 0

# define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90

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
panel_img = pygame.transform.scale(
    pygame.image.load(
        "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/panel.png"
    ).convert_alpha(),
    (screen_width, bottom_panel),
)


# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, False, text_col)
    screen.blit(img, (x, y))


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
            self.frame_index = 0

    def attack(self, target):
        # deal damage
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage

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
Samurai = Fighter(500, 600, "Samurai", 50, 10, 3)
Enemy1 = Fighter(1400, 600, "Enemy", 70, 8, 2, flip=True)
Enemy2 = Fighter(1650, 590, "Enemy", 60, 8, 2, flip=True)

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

    # player action
    if Samurai.alive == True:
        if current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time:
                # look for player action
                # Attack
                Samurai.attack(Enemy1)
                current_fighter += 1
                action_cooldown = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
