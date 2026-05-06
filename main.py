#USE THIS WHEN UPDATING GAME TO UPDATE IN VNC: bash start.sh
import pygame
import gif_pygame

# pygame setup
pygame.init()

bottom_panel = 360  # 1/3 of 1080, matches panel image natural aspect ratio at 1920px wide
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

while run:
    
    screen.fill((0, 0, 0))

    #draw background
    draw_bg()
    
    #draw panel
    draw_panel()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # flip() the display
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()