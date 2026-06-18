import random


def clear_enemy_defend_state(enemy):
    if enemy.is_defending and enemy.action == 4:
        enemy.is_defending = False
        enemy.idle()


def perform_enemy_action(
    enemy,
    player,
    enemy_potion_effect,
    enemy_defence_chance,
    damage_text_group,
    damage_text_class,
    green,
):
    # low HP -> potion
    if enemy.hp / enemy.max_hp < 0.5 and enemy.potions > 0:
        if enemy.hp + enemy_potion_effect < enemy.max_hp:
            heal_amount = enemy_potion_effect
        else:
            heal_amount = enemy.max_hp - enemy.hp

        enemy.hp += heal_amount
        enemy.potions -= 1
        damage_text = damage_text_class(
            enemy.rect.centerx,
            enemy.rect.y,
            str(heal_amount),
            green,
        )
        damage_text_group.add(damage_text)
        return

    # otherwise defend or attack
    if random.random() < enemy_defence_chance:
        enemy.defend()
    else:
        enemy.pick_attack()
        enemy.attack(player)


def enemy_turns(
    enemy_list,
    player,
    current_fighter,
    action_cooldown,
    action_wait_time,
    enemy_potion_effect,
    enemy_defence_chance,
    damage_text_group,
    damage_text_class,
    green,
):
    for count, enemy in enumerate(enemy_list):
        if current_fighter != 2 + count:
            continue

        if enemy.alive is False:
            return current_fighter + 1, 0

        action_cooldown += 1
        if action_cooldown < action_wait_time:
            return current_fighter, action_cooldown

        clear_enemy_defend_state(enemy)
        perform_enemy_action(
            enemy,
            player,
            enemy_potion_effect,
            enemy_defence_chance,
            damage_text_group,
            damage_text_class,
            green,
        )
        return current_fighter + 1, 0

    return current_fighter, action_cooldown
