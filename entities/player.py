import os
import random
import pygame

screen = None
font = None
red = None
green = None
yellow = None
white = None
partial_block_min = 0.45
partial_block_max = 0.65
full_block_chance = 0.20
counter_chance = 0.10
damage_text_group = None


def configure_player_module(
    screen_ref,
    font_ref,
    red_ref,
    green_ref,
    yellow_ref,
    white_ref,
    partial_min,
    partial_max,
    full_block,
    counter,
    damage_group_ref,
):
    global screen, font, red, green, yellow, white
    global partial_block_min, partial_block_max, full_block_chance, counter_chance
    global damage_text_group

    screen = screen_ref
    font = font_ref
    red = red_ref
    green = green_ref
    yellow = yellow_ref
    white = white_ref
    partial_block_min = partial_min
    partial_block_max = partial_max
    full_block_chance = full_block
    counter_chance = counter
    damage_text_group = damage_group_ref


class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions, flip=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.is_defending = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Attack, 2: Hurt, 3: Death, 4: Defend
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

        # Load hurt animation
        temp_list = []
        hurt_path = f"{base_path}/Hurt"
        frame_count = len([f for f in os.listdir(hurt_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{hurt_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load death animation
        temp_list = []
        death_path = f"{base_path}/Death"
        frame_count = len([f for f in os.listdir(death_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{death_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # load defend animation
        temp_list = []
        defend_path = f"{base_path}/Defend"
        frame_count = len([f for f in os.listdir(defend_path) if f.endswith(".png")])
        for i in range(1, frame_count + 1):
            img = pygame.image.load(f"{defend_path}/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            img = img.subsurface(img.get_bounding_rect()).copy()
            if flip:
                img = pygame.transform.flip(img, True, False)
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def pick_attack(self):
        # Randomly select an Attack_* variant for the next attack
        self.animation_list[1] = random.choice(self.attack_variants)
        self.frame_index = 0

    def update(self):
        animation_cooldown = 140
        # Handle animation
        # Dead fighters stay dead
        if not self.alive and self.action != 3:
            self.death()
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check the time before updating animation
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Reset to start if animation has reached the end
        # Reset to start if animation has reached the end
        if self.frame_index >= len(self.animation_list[self.action]):
            # Death stays on last frame forever
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1

            # Defend stays on last frame only while defending
            elif self.action == 4:
                if self.is_defending:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()

            # Attack/Hurt finish, then either return to defend-hold or idle
            elif self.action in (1, 2):
                if self.is_defending:
                    self.action = 4
                    self.frame_index = len(self.animation_list[4]) - 1
                    self.update_time = pygame.time.get_ticks()
                else:
                    self.idle()

            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):

        # Base damage
        rand = random.randint(-3, 3)
        base_damage = self.strength + rand

        # Global cri chance
        crit_chance = 0.15  # 15%
        is_critical = random.random() < crit_chance

        # Calculate damage x crit
        if is_critical:
            raw_damage = int(base_damage * 1.5)
        else:
            raw_damage = base_damage

        damage, defense_result, counter_damage = target.guard_damage(raw_damage, self)

        # Apply damage to target
        if damage > 0:
            target.hp -= damage
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            else:
                target.hurt()

        # Damage / defense floating text
        if defense_result == "Blocked":
            damage_text_group.add(
                DamageText(target.rect.centerx, target.rect.y, "BLOCK", white)
            )
        elif defense_result == "Countered":
            damage_text_group.add(
                DamageText(target.rect.centerx, target.rect.y, "COUNTER", yellow)
            )
            if counter_damage > 0:
                damage_text_group.add(
                    DamageText(
                        self.rect.centerx, self.rect.y, str(counter_damage), yellow
                    )
                )
        else:
            # show damage text / colour
            if is_critical:
                damage_colour = yellow
            else:
                damage_colour = red

            # Sylise crit marker
            if is_critical:
                damage_display = f"{damage}!"
            else:
                damage_display = str(damage)

            damage_text = DamageText(
                target.rect.centerx, target.rect.y, damage_display, damage_colour
            )
            damage_text_group.add(damage_text)

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        # set hurt method
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        # set death method
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Anchor to the bottom of the image
        draw_rect = self.image.get_rect(midbottom=self.rect.midbottom)
        screen.blit(self.image, draw_rect)

    def reset(self):
        self.alive = True
        self.is_defending = False
        self.hp = self.max_hp
        self.potions = self.start_potions
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    # set defending state and return to idle animation
    def defend(self):
        self.is_defending = True
        self.action = 4
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def guard_damage(self, incoming_damage, attacker):
        # default no defense active
        if self.is_defending == False:
            return incoming_damage, "Hit", 0

        roll = random.random()

        # Counter attack chance
        if roll < counter_chance:
            # play attack
            self.pick_attack()
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            counter_damage = max(1, int(self.strength * 0.6) + random.randint(-2, 2))
            attacker.hp -= counter_damage
            if attacker.hp < 1:
                attacker.hp = 0
                attacker.alive = False
                attacker.death()
            else:
                attacker.hurt()
            return 0, "Countered", counter_damage

        if roll < counter_chance + full_block_chance:
            return 0, "Blocked", 0

        taken_ratio = random.uniform(partial_block_min, partial_block_max)
        reduced = max(1, int(incoming_damage * taken_ratio))
        return reduced, "Partial", 0


# Health bar class to show health of player and enemies
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


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # text hovers upwards
        self.rect.y -= 1
        # remove the text after it has moved a certain distance
        self.counter += 1
        if self.counter > 30:
            self.kill()


def player_turn(
    player,
    current_fighter,
    action_cooldown,
    action_wait_time,
    defend,
    attack,
    target,
    potion,
    player_potion_effect,
    damage_text_group,
    damage_text_class,
    green,
):
    if player.alive is False or current_fighter != 1:
        return current_fighter, action_cooldown

    if player.is_defending and player.action == 4:
        player.is_defending = False
        player.idle()

    action_cooldown += 1
    if action_cooldown < action_wait_time:
        return current_fighter, action_cooldown

    if defend:
        player.defend()
        return current_fighter + 1, 0

    if attack and target is not None:
        was_alive = target.alive
        player.attack(target)
        if was_alive and not target.alive:
            player.potions += 1
        return current_fighter + 1, 0

    if potion and player.potions > 0:
        if player.hp + player_potion_effect < player.max_hp:
            heal_amount = player_potion_effect
        else:
            heal_amount = player.max_hp - player.hp

        player.hp += heal_amount
        player.potions -= 1
        damage_text = damage_text_class(
            player.rect.centerx, player.rect.y, str(heal_amount), green
        )
        damage_text_group.add(damage_text)
        return current_fighter + 1, 0

    return current_fighter, action_cooldown
