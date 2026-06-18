def player_action(player_mode, clicked, Enemy_list, mouse_pos):
    attack = False
    defend = False
    target = None

    if player_mode == 1 and clicked:
        defend = True

    if player_mode == 0:
        for count, enemy in enumerate(Enemy_list):
            hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
            if enemy.alive and hover_rect.collidepoint(mouse_pos):
                if clicked == True:
                    attack = True
                    target = Enemy_list[count]
                break
    return attack, defend, target


def hovering_enemy(Enemy_list, mouse_pos):
    for enemy in Enemy_list:
        hover_rect = enemy.image.get_rect(midbottom=enemy.rect.midbottom)
        if enemy.alive and hover_rect.collidepoint(mouse_pos):
            return True
    return False
