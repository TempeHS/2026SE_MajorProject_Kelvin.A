import random

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

# defence chances
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
game_over = 0  # 0 = no winner, -1 = enemy win, 1 = player win

# load fonts
font = pygame.font.SysFont("Times New Roman", 40)
mode_font = pygame.font.SysFont("Times New Roman", 20)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
