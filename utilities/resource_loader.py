import pygame


def load_fonts():
    font = pygame.font.SysFont("Times New Roman", 40)
    mode_font = pygame.font.SysFont("Times New Roman", 20)
    return font, mode_font


def load_images(screen_width, screen_height, bottom_panel):
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
    # load indicator arrow
    Indicator_img = pygame.image.load(
        "/workspaces/2026SE_MajorProject_Kelvin.A/assets/icons/arrow_indicator.png"
    ).convert_alpha()
    Indicator_scale = 0.30
    Indicator_img = pygame.transform.scale(
        Indicator_img,
        (
            max(1, int(Indicator_img.get_width() * Indicator_scale)),
            max(1, int(Indicator_img.get_height() * Indicator_scale)),
        ),
    )

    # load Restart button
    Restart_img = pygame.image.load(
        "/workspaces/2026SE_MajorProject_Kelvin.A/assets/ui/restart_button.png"
    ).convert_alpha()

    return (
        backround_img,
        panel_img,
        Potion_img,
        Katana_img,
        Shield_img,
        Indicator_img,
        Restart_img,
    )


def get_cursor_hotspots(shield_img):
    katana_hotspot = (8, 8)
    shield_hotspot = (shield_img.get_width() // 2, shield_img.get_height() // 2)
    return katana_hotspot, shield_hotspot
