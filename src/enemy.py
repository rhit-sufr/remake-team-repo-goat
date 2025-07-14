import math

import pygame

import main


class Enemy:
    def __init__(self, x, y, enemy_type="normal"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type

        if enemy_type == "normal":
            self.radius = 18
            self.speed = 2
            self.health = 30
            self.damage = 10
            self.color = (220, 20, 60)
            self.score_value = 50
        elif enemy_type == "fast":
            self.radius = 15
            self.speed = 3.5
            self.health = 20
            self.damage = 5
            self.color = (255, 105, 180)
            self.score_value = 75
        elif enemy_type == "tank":
            self.radius = 25
            self.speed = 1.2
            self.health = 80
            self.damage = 20
            self.color = (139, 0, 0)
            self.score_value = 150
        elif enemy_type == "sniper":
            self.radius = 16
            self.speed = 1.8
            self.health = 25
            self.damage = 35
            self.color = (0, 191, 255)
            self.score_value = 100
        elif enemy_type == "boss":
            self.radius = 40
            self.speed = 1.5
            self.health = 200
            self.damage = 30
            self.color = (128, 0, 128)
            self.score_value = 500

        self.max_health = self.health
        self.attack_cooldown = 0
        self.direction = 0
        self.attack_range = 250 if enemy_type == "sniper" else 150

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        dx = math.cos(math.radians(self.direction))
        dy = -math.sin(math.radians(self.direction))
        eye_x = self.x + dx * self.radius * 0.6
        eye_y = self.y + dy * self.radius * 0.6
        pygame.draw.circle(screen, (30, 30, 30), (int(eye_x), int(eye_y)), self.radius // 3)

        pygame.draw.rect(screen, (100, 100, 100), (self.x - self.radius, self.y - self.radius - 10, self.radius * 2, 5))
        pygame.draw.rect(screen, main.HEALTH_BAR, (self.x - self.radius, self.y - self.radius - 10,
                                                   self.radius * 2 * (self.health / self.max_health), 5))

        if self.enemy_type == "sniper" and self.attack_cooldown > 30:
            player_pos = (self.target_x, self.target_y)
            pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), player_pos, 2)

    def move_towards_player(self, player_x, player_y, walls):
        dx = player_x - self.x
        dy = player_y - self.y
        distance = max(1, math.sqrt(dx * dx + dy * dy))

        self.direction = math.degrees(math.atan2(-dy, dx))

        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed

        new_x = self.x + move_x
        new_y = self.y + move_y

        enemy_rect = pygame.Rect(new_x - self.radius, new_y - self.radius,
                                 self.radius * 2, self.radius * 2)

        can_move = True
        for wall in walls:
            if enemy_rect.colliderect(wall.rect):
                can_move = False
                break

        if can_move and distance > self.radius + 20:
            self.x = new_x
            self.y = new_y
        elif distance < self.radius + 20:
            self.x -= move_x * 0.5
            self.y -= move_y * 0.5

    def can_attack(self, player_x, player_y):
        if self.enemy_type == "sniper":

            if self.attack_cooldown == 0:
                self.target_x = player_x
                self.target_y = player_y
                self.attack_cooldown = 90
                return False
            elif self.attack_cooldown == 1:
                return True

        if self.attack_cooldown <= 0:

            dx = player_x - self.x
            dy = player_y - self.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < self.attack_range:
                self.attack_cooldown = 60
                return True
        return False

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
