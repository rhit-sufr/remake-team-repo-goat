import math

import pygame

import bullet
import load_image
import main


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.direction = 0
        self.weapons = ["Pistol", "Knife"]
        self.current_weapon = 0
        self.ammo = {
            "Pistol": 12,
            "Shotgun": 6,
            "Rifle": 30,
            "Rocket Launcher": 2,
            "Knife": float('inf')
        }
        self.max_ammo = {
            "Pistol": 12,
            "Shotgun": 6,
            "Rifle": 30,
            "Rocket Launcher": 2,
            "Knife": float('inf')
        }
        self.reloading = False
        self.reload_time = 0
        self.reload_duration = 60
        self.score = 0
        self.melee_attacking = False
        self.melee_time = 0
        self.melee_duration = 20
        self.melee_range = 50
        self.melee_damage = 25
        self.kills = 0
        self.weapon_icons = {
            "Pistol": load_image.load_image("pistol", (40, 30)),
            "Shotgun": load_image.load_image("shotgun", (50, 30)),
            "Rifle": load_image.load_image("rifle", (50, 20)),
            "Rocket Launcher": load_image.load_image("rocket", (50, 30)),
            "Knife": load_image.load_image("knife", (40, 40))
        }

        self.moving = {"up": False, "down": False, "left": False, "right": False}

    def draw(self, screen):

        pygame.draw.circle(screen, main.PLAYER_COLOR, (self.x, self.y), self.radius)

        end_x = self.x + (self.radius + 10) * math.cos(math.radians(self.direction))
        end_y = self.y - (self.radius + 10) * math.sin(math.radians(self.direction))
        pygame.draw.line(screen, (30, 30, 30), (self.x, self.y), (end_x, end_y), 4)

        font = pygame.font.SysFont(None, 24)
        weapon = self.weapons[self.current_weapon]

        if weapon != "Knife":
            ammo_text = font.render(f"Ammo: {self.ammo[weapon]}/{self.max_ammo[weapon]}", True, main.TEXT_COLOR)
            screen.blit(ammo_text, (self.x - 30, self.y - 70))

        pygame.draw.rect(screen, (100, 100, 100), (self.x - 30, self.y - 90, 60, 10))
        pygame.draw.rect(screen, main.HEALTH_BAR, (self.x - 30, self.y - 90, 60 * (self.health / self.max_health), 10))

        if self.reloading:
            reload_width = 40 * (1 - self.reload_time / self.reload_duration)
            pygame.draw.rect(screen, (100, 100, 100), (self.x - 20, self.y + 30, 40, 5))
            pygame.draw.rect(screen, main.AMMO_BAR, (self.x - 20, self.y + 30, reload_width, 5))

        if self.melee_attacking:
            angle_rad = math.radians(self.direction)
            start_x = self.x + self.radius * math.cos(angle_rad)
            start_y = self.y - self.radius * math.sin(angle_rad)
            end_x = start_x + self.melee_range * math.cos(angle_rad)
            end_y = start_y - self.melee_range * math.sin(angle_rad)

            alpha = int(200 * (1 - self.melee_time / self.melee_duration))
            color = (main.MELEE_COLOR[0], main.MELEE_COLOR[1], main.MELEE_COLOR[2], alpha)

            attack_surf = pygame.Surface((main.WIDTH, main.HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(attack_surf, color, (start_x, start_y), (end_x, end_y), 8)
            screen.blit(attack_surf, (0, 0))

    def update_movement(self, walls):

        dx, dy = 0, 0

        if self.moving["up"]:
            dy -= 1
        if self.moving["down"]:
            dy += 1
        if self.moving["left"]:
            dx -= 1
        if self.moving["right"]:
            dx += 1

        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        player_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                  self.radius * 2, self.radius * 2)

        collision_x, collision_y = False, False

        for wall in walls:
            if player_rect.colliderect(wall.rect):

                test_rect_x = pygame.Rect(new_x - self.radius, self.y - self.radius,
                                          self.radius * 2, self.radius * 2)
                if not test_rect_x.colliderect(wall.rect):
                    new_y = self.y
                else:

                    test_rect_y = pygame.Rect(self.x - self.radius, new_y - self.radius,
                                              self.radius * 2, self.radius * 2)
                    if not test_rect_y.colliderect(wall.rect):
                        new_x = self.x
                    else:

                        new_x, new_y = self.x, self.y

        if 30 <= new_x <= main.WIDTH - 30:
            self.x = new_x
        if 30 <= new_y <= main.HEIGHT - 30:
            self.y = new_y

    def rotate(self, mouse_pos):
        dx = mouse_pos[0] - self.x
        dy = self.y - mouse_pos[1]
        self.direction = math.degrees(math.atan2(dy, dx))

    def shoot(self, bullets, enemies, walls):
        if self.reloading:
            return False

        weapon = self.weapons[self.current_weapon]

        if weapon == "Knife":
            if not self.melee_attacking:
                self.melee_attacking = True
                self.melee_time = 0

                angle_rad = math.radians(self.direction)
                start_x = self.x + self.radius * math.cos(angle_rad)
                start_y = self.y - self.radius * math.sin(angle_rad)
                end_x = start_x + self.melee_range * math.cos(angle_rad)
                end_y = start_y - self.melee_range * math.sin(angle_rad)

                attack_line = pygame.Rect(min(start_x, end_x) - 10, min(start_y, end_y) - 10,
                                          abs(end_x - start_x) + 20, abs(end_y - start_y) + 20)

                for enemy in enemies[:]:
                    enemy_rect = pygame.Rect(enemy.x - enemy.radius, enemy.y - enemy.radius,
                                             enemy.radius * 2, enemy.radius * 2)

                    dx = enemy.x - self.x
                    dy = enemy.y - self.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < self.radius + enemy.radius + self.melee_range:

                        angle_to_enemy = math.degrees(math.atan2(-dy, dx))
                        angle_diff = abs((self.direction - angle_to_enemy + 180) % 360 - 180)

                        if angle_diff < 45:
                            if enemy.take_damage(self.melee_damage):
                                self.kills += 1
                                enemies.remove(enemy)
                return True

        if self.ammo[weapon] > 0:
            self.ammo[weapon] -= 1

            if weapon == "Pistol":
                bullets.append(bullet.Bullet(self.x, self.y, self.direction, 10, 20, "Pistol", walls))
            elif weapon == "Shotgun":
                for angle_offset in [-10, 0, 10]:
                    bullets.append(
                        bullet.Bullet(self.x, self.y, self.direction + angle_offset, 8, 15, "Shotgun", walls))
            elif weapon == "Rifle":
                bullets.append(bullet.Bullet(self.x, self.y, self.direction, 15, 15, "Rifle", walls))
            elif weapon == "Rocket Launcher":
                bullets.append(
                    bullet.Bullet(self.x, self.y, self.direction, 5, 30, "Rocket Launcher", walls, is_explosive=True))

            return True
        return False

    def reload(self):
        weapon = self.weapons[self.current_weapon]
        if weapon == "Knife":
            return

        if not self.reloading and self.ammo[weapon] < self.max_ammo[weapon]:
            self.reloading = True
            self.reload_time = 0

    def update(self):

        if self.reloading:
            self.reload_time += 1
            if self.reload_time >= self.reload_duration:
                weapon = self.weapons[self.current_weapon]
                self.ammo[weapon] = self.max_ammo[weapon]
                self.reloading = False

        if self.melee_attacking:
            self.melee_time += 1
            if self.melee_time >= self.melee_duration:
                self.melee_attacking = False

    def switch_weapon(self, direction):
        new_index = (self.current_weapon + direction) % len(self.weapons)
        self.current_weapon = new_index

    def add_weapon(self, weapon_name):
        if weapon_name not in self.weapons:
            self.weapons.append(weapon_name)
            self.ammo[weapon_name] = self.max_ammo[weapon_name]
            self.current_weapon = len(self.weapons) - 1
