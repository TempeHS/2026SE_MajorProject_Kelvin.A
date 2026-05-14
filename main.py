#USE THIS WHEN UPDATING/STARTING GAME TO UPDATE IN VNC: bash start.sh
import os
import pygame
import gif_pygame

# pygame setup
pygame.init()

bottom_panel = 360  
screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
run = True
dt = 0

_bg_raw = gif_pygame.load("/workspaces/2026SE_MajorProject_Kelvin.A/assets/backgrounds/Background.gif")
_bg_size = (screen_width, screen_height - bottom_panel)
backround_img = gif_pygame.GIFPygame(
    [(pygame.transform.scale(surf, _bg_size), dur) for surf, dur in _bg_raw.get_frame_data()]
)
panel_img = pygame.transform.scale(pygame.image.load("/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/panel.png").convert_alpha(), (screen_width, bottom_panel))


def draw_bg():
    backround_img.render(screen, (0, 0))

def draw_panel():
    pygame.draw.rect(screen, (74, 45, 35), (0, screen_height - bottom_panel, screen_width, bottom_panel))
    screen.blit(panel_img, (0, screen_height - bottom_panel))

class Fighter():
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
        self.action = 0 #0: idle, 1: attack, 2: hurt, 3: death
        self.update_time = pygame.time.get_ticks()
        idle_path = f"/workspaces/2026SE_MajorProject_Kelvin.A/assets/sprites/{self.name}/Idle"
        frame_count = len([f for f in os.listdir(idle_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{idle_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if flip:
                img = pygame.transform.flip(img, True, False)
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        animation_cooldown = 100
        #Handle animation
        #update image
        self.image = self.animation_list[self.frame_index]
        #Check the time before updating animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Reset to start if animation has reached the end
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
    
    def draw(self):
        screen.blit(self.image, self.rect)
        
Samurai = Fighter(500,500, "Samurai", 30, 10, 3)
Enemy1 = Fighter(1400,500, "Enemy1", 40, 8, 2, flip=True)
Enemy2 = Fighter(1700,500, "Enemy1", 40, 8, 2, flip=True)
    
Enemy_list = []
Enemy_list.append(Enemy1)
Enemy_list.append(Enemy2)
    
while run:
    
    screen.fill((0, 0, 0))

    #draw background
    draw_bg()
    
    #draw panel
    draw_panel()
    
    #draw fighters
    Samurai.update()
    Samurai.draw()
    for enemy in Enemy_list:
        enemy.update()
        enemy.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()