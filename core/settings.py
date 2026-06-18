import random

# Define constants
Bottom_Panel = 360
Screen_Width = 1920
Screen_Height = 1080
Target_fps = 60

# define game variables
Player_mode_default = 0  # default to attack mode

Enemy_defence_chance = 0.33  # 33% chance for enemy to defend

# defence chances
Partial_block_min = 0.45
Partial_block_max = 0.65
Full_block_chance = 0.20
Counter_chance = 0.10

Current_fighter_default = 1
Total_fighters = 3
Action_cooldown_default = 0
Action_wait_time = 90
Game_over_default = 0  # 0 = no winner, -1 = enemy win, 1 = player win

Player_potion_effect = 16 + random.randint(-2, 10)
Enemy_potion_effect = 9 + random.randint(-2, 5)

# define colours
Red = (255, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)
White = (255, 255, 255)
Cyan = (0, 255, 255)
