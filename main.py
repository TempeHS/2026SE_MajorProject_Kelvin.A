#USE THIS WHEN UPDATING GAME TO UPDATE IN VNC: pkill -f "python main.py"; DISPLAY=:99 python main.py &
import pygame

# pygame setup
pygame.init()

bottom_panel = 500
screen_width = 1280
screen_height = 720 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
run = True
dt = 0

backround_img = pygame.transform.scale(pygame.image.load("/workspaces/2026SE_MajorProject_Kelvin.A/assets/Backgrounds/background.jpg").convert_alpha(), (1280, 720))

def draw_bg():
    screen.blit(backround_img, (0, 0))

while run:
    
    #draw background
    draw_bg()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # flip() the display
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()