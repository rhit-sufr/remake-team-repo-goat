import math
import random
import sys

import pygame

import load_image
import player
import enemy

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game -- GOAT Studio")

PLAYER_COLOR = (70, 130, 180)
HEALTH_BAR = (50, 205, 50)
TEXT_COLOR = (220, 220, 220)
BACKGROUND = (40, 44, 52)
ENEMY_COLOR = (220, 20, 60)
BULLET_COLOR = (255, 215, 0)
WALL_COLOR = (100, 100, 100)
AMMO_BAR = (255, 140, 0)
WEAPON_HIGHLIGHT = (0, 191, 255)
MELEE_COLOR = (30, 144, 255)

class WeaponDrop:
    def __init__(self, x, y, weapon_type):
        self.x = x
        self.y = y
        self.weapon_type = weapon_type
        self.radius = 15
        self.color = (50, 205, 50) if weapon_type != "Knife" else (30, 144, 255)
        self.icon = None

        if weapon_type == "Shotgun":
            self.icon = load_image.load_image("shotgun_icon", (20, 20))
        elif weapon_type == "Rifle":
            self.icon = load_image.load_image("rifle_icon", (25, 15))
        elif weapon_type == "Rocket Launcher":
            self.icon = load_image.load_image("rocket_icon", (20, 20))
        elif weapon_type == "Knife":
            self.icon = load_image.load_image("knife_icon", (20, 20))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

        if self.icon:
            screen.blit(self.icon, (self.x - self.icon.get_width() // 2,
                                    self.y - self.icon.get_height() // 2))
        else:
            font = pygame.font.SysFont(None, 24)
            text = font.render(self.weapon_type[0], True, (255, 255, 255))
            screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def check_collision(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (self.radius + player.radius)


class Wall:
    def __init__(self, x, y, width, height, wall_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.wall_type = wall_type
        self.color = WALL_COLOR

        if wall_type == "breakable":
            self.color = (139, 69, 19)
        elif wall_type == "metal":
            self.color = (169, 169, 169)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (70, 70, 70), self.rect, 2)


class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.walls = []
        self.enemies = []
        self.initial_player_pos = (WIDTH // 2, HEIGHT // 2)
        self.weapon_drops = []

        if level_num == 1:
            self._create_level_1()
        elif level_num == 2:
            self._create_level_2()
        elif level_num == 3:
            self._create_level_3()
        elif level_num == 4:
            self._create_level_4()
        else:
            self._create_final_level()

    def _create_level_1(self):

        self.walls = [
            Wall(200, 150, 100, 30, "normal"),
            Wall(400, 300, 30, 200, "normal"),
            Wall(600, 100, 200, 30, "normal"),
            Wall(700, 400, 100, 30, "normal"),
            Wall(150, 500, 300, 30, "normal"),
            Wall(800, 200, 30, 150, "normal"),
        ]

        self.enemies = [
            enemy.Enemy(300, 300, "normal"),
            enemy.Enemy(700, 300, "normal"),
            enemy.Enemy(500, 500, "normal")
        ]

        self.weapon_drops = [
            WeaponDrop(200, 200, "Shotgun")
        ]

    def _create_level_2(self):

        self.walls = [
            Wall(100, 100, 50, 300, "normal"),
            Wall(100, 100, 300, 50, "normal"),
            Wall(350, 100, 50, 200, "normal"),
            Wall(200, 250, 200, 50, "normal"),
            Wall(500, 150, 50, 300, "breakable"),
            Wall(650, 150, 200, 50, "normal"),
            Wall(650, 300, 200, 50, "normal"),
            Wall(800, 150, 50, 200, "normal"),
            Wall(200, 450, 400, 50, "normal"),
            Wall(700, 450, 200, 50, "normal"),
        ]

        self.enemies = [
            enemy.Enemy(300, 200, "normal"),
            enemy.Enemy(400, 400, "fast"),
            enemy.Enemy(600, 200, "normal"),
            enemy.Enemy(750, 400, "normal"),
            enemy.Enemy(500, 350, "sniper")
        ]

        self.weapon_drops = [
            WeaponDrop(600, 400, "Rifle"),
            WeaponDrop(400, 200, "Knife")
        ]

    def _create_level_3(self):

        self.walls = [
            Wall(100, 100, 800, 50, "normal"),  # 顶部
            Wall(100, 550, 800, 50, "normal"),  # 底部
            Wall(100, 100, 50, 500, "normal"),  # 左侧
            Wall(850, 100, 50, 500, "normal"),  # 右侧

            Wall(250, 200, 50, 300, "metal"),
            Wall(700, 200, 50, 300, "metal"),
            Wall(350, 150, 300, 50, "normal"),
            Wall(350, 500, 300, 50, "normal"),
            Wall(450, 250, 100, 200, "breakable"),
        ]

        self.enemies = [
            enemy.Enemy(200, 200, "fast"),
            enemy.Enemy(200, 500, "fast"),
            enemy.Enemy(800, 200, "fast"),
            enemy.Enemy(800, 500, "fast"),
            enemy.Enemy(500, 300, "tank"),
            enemy.Enemy(400, 400, "sniper"),
            enemy.Enemy(600, 400, "sniper")
        ]

        self.weapon_drops = [
            WeaponDrop(500, 200, "Rocket Launcher"),
            WeaponDrop(500, 500, "Knife")
        ]

    def _create_level_4(self):

        self.walls = [

            Wall(50, 50, 900, 30, "metal"),
            Wall(50, 50, 30, 600, "metal"),
            Wall(50, 620, 900, 30, "metal"),
            Wall(920, 50, 30, 600, "metal"),

            Wall(150, 150, 200, 30, "normal"),
            Wall(150, 150, 30, 200, "normal"),
            Wall(650, 150, 200, 30, "normal"),
            Wall(820, 150, 30, 200, "normal"),
            Wall(150, 500, 200, 30, "normal"),
            Wall(150, 330, 30, 200, "normal"),
            Wall(650, 500, 200, 30, "normal"),
            Wall(820, 330, 30, 200, "normal"),

            Wall(400, 250, 200, 30, "breakable"),
            Wall(400, 450, 200, 30, "breakable"),
            Wall(350, 300, 30, 150, "breakable"),
            Wall(620, 300, 30, 150, "breakable"),

            Wall(450, 350, 100, 100, "metal")
        ]

        self.enemies = [
            enemy.Enemy(200, 200, "tank"),
            enemy.Enemy(800, 200, "tank"),
            enemy.Enemy(200, 550, "tank"),
            enemy.Enemy(800, 550, "tank"),
            enemy.Enemy(300, 300, "sniper"),
            enemy.Enemy(700, 300, "sniper"),
            enemy.Enemy(300, 500, "sniper"),
            enemy.Enemy(700, 500, "sniper"),
            enemy.Enemy(500, 400, "boss")
        ]

        self.weapon_drops = [
            WeaponDrop(200, 400, "Rocket Launcher"),
            WeaponDrop(800, 400, "Rocket Launcher"),
            WeaponDrop(500, 200, "Rifle")
        ]

    def _create_final_level(self):

        self.walls = [

            Wall(100, 100, 800, 30, "metal"),
            Wall(100, 100, 30, 500, "metal"),
            Wall(100, 570, 800, 30, "metal"),
            Wall(870, 100, 30, 500, "metal"),

            Wall(200, 200, 100, 300, "breakable"),
            Wall(700, 200, 100, 300, "breakable"),
            Wall(350, 150, 300, 50, "normal"),
            Wall(350, 500, 300, 50, "normal"),

            Wall(400, 250, 50, 200, "metal"),
            Wall(550, 250, 50, 200, "metal"),

            Wall(475, 350, 50, 50, "metal")
        ]

        enemy_types = ["normal", "fast", "tank", "sniper"]
        for i in range(12):
            x = random.randint(150, 850)
            y = random.randint(150, 550)

            valid_pos = True
            enemy_rect = pygame.Rect(x - 25, y - 25, 50, 50)
            for wall in self.walls:
                if enemy_rect.colliderect(wall.rect):
                    valid_pos = False
                    break

            if valid_pos:
                enemy_type = random.choice(enemy_types)
                self.enemies.append(enemy.Enemy(x, y, enemy_type))

        self.enemies.append(enemy.Enemy(500, 350, "boss"))

        self.weapon_drops = [
            WeaponDrop(150, 150, "Rocket Launcher"),
            WeaponDrop(850, 150, "Rocket Launcher"),
            WeaponDrop(150, 550, "Rocket Launcher"),
            WeaponDrop(850, 550, "Rocket Launcher"),
            WeaponDrop(500, 300, "Knife")
        ]


def main():
    clock = pygame.time.Clock()

    player_instance = player.Player(WIDTH // 2, HEIGHT // 2)

    current_level = 1
    level = Level(current_level)
    walls = level.walls
    enemies = level.enemies
    weapon_drops = level.weapon_drops
    player_instance.x, player_instance.y = level.initial_player_pos

    bullets = []

    game_over = False
    level_complete = False
    score = 0
    level_transition_timer = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_instance.moving["up"] = True
                if event.key == pygame.K_s:
                    player_instance.moving["down"] = True
                if event.key == pygame.K_a:
                    player_instance.moving["left"] = True
                if event.key == pygame.K_d:
                    player_instance.moving["right"] = True

                if event.key == pygame.K_r and not game_over:
                    player_instance.reload()
                if event.key == pygame.K_j and not game_over:
                    player_instance.shoot(bullets, enemies, walls)
                if event.key == pygame.K_q:
                    player_instance.switch_weapon(-1)
                if event.key == pygame.K_e:
                    player_instance.switch_weapon(1)
                if event.key == pygame.K_SPACE and (game_over or level_complete):
                    if game_over:
                        return main()
                    elif level_complete:
                        level_complete = False
                        current_level += 1
                        if current_level > 5:
                            current_level = 1
                        level = Level(current_level)
                        walls = level.walls
                        enemies = level.enemies
                        weapon_drops = level.weapon_drops
                        player_instance.x, player_instance.y = level.initial_player_pos
                        player_instance.health = min(player_instance.max_health, player_instance.health + 30)
                        bullets = []

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player_instance.moving["up"] = False
                if event.key == pygame.K_s:
                    player_instance.moving["down"] = False
                if event.key == pygame.K_a:
                    player_instance.moving["left"] = False
                if event.key == pygame.K_d:
                    player_instance.moving["right"] = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    player_instance.shoot(bullets, enemies, walls)

        if game_over:
            screen.fill(BACKGROUND)

            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            game_over_text = font_large.render("GAME OVER", True, (220, 20, 60))
            score_text = font_medium.render(f"Final Score: {score}", True, TEXT_COLOR)
            level_text = font_medium.render(f"Reached Level: {current_level}", True, TEXT_COLOR)
            restart_text = font_small.render("Press SPACE to Restart", True, TEXT_COLOR)

            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue

        if level_complete:
            screen.fill(BACKGROUND)

            font_large = pygame.font.SysFont(None, 72)
            font_medium = pygame.font.SysFont(None, 48)
            font_small = pygame.font.SysFont(None, 36)

            level_text = font_large.render(f"LEVEL {current_level} COMPLETE!", True, (50, 205, 50))
            score_text = font_medium.render(f"Score: {score}", True, TEXT_COLOR)
            next_text = font_small.render("Press SPACE to Continue to Next Level", True, TEXT_COLOR)

            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 100))

            pygame.display.flip()
            clock.tick(60)
            continue

        mouse_pos = pygame.mouse.get_pos()
        player_instance.rotate(mouse_pos)

        player_instance.update_movement(walls)

        player_instance.update()

        for enemy in enemies[:]:
            enemy.move_towards_player(player_instance.x, player_instance.y, walls)
            enemy.update()

            dx = enemy.x - player_instance.x
            dy = enemy.y - player_instance.y
            distance = math.sqrt(dx * dx + dy * dy)

            if distance < enemy.radius + player_instance.radius:
                if enemy.can_attack(player_instance.x, player_instance.y):
                    player_instance.health -= enemy.damage
                    if player_instance.health <= 0:
                        game_over = True
            elif enemy.enemy_type == "sniper" and enemy.attack_cooldown > 0:

                enemy.target_x = player_instance.x
                enemy.target_y = player_instance.y

        for bullet in bullets[:]:
            bullet.move()

            for enemy in enemies[:]:
                dx = bullet.x - enemy.x
                dy = bullet.y - enemy.y
                distance = math.sqrt(dx * dx + dy * dy)

                if distance < bullet.radius + enemy.radius:
                    if bullet.is_explosive:

                        for e in enemies[:]:
                            edx = bullet.x - e.x
                            edy = bullet.y - e.y
                            edist = math.sqrt(edx * edx + edy * edy)
                            if edist < bullet.explosion_radius:
                                if e.take_damage(bullet.damage):
                                    player_instance.kills += 1
                                    score += e.score_value

                                    if random.random() < 0.3 and len(player_instance.weapons) < 5:
                                        weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                        for wt in weapon_types:
                                            if wt not in player_instance.weapons:
                                                weapon_drops.append(WeaponDrop(e.x, e.y, wt))
                                                break
                                    enemies.remove(e)
                        bullets.remove(bullet)
                        break
                    else:
                        if enemy.take_damage(bullet.damage):
                            player_instance.kills += 1
                            score += enemy.score_value

                            if random.random() < 0.3 and len(player_instance.weapons) < 5:
                                weapon_types = ["Shotgun", "Rifle", "Rocket Launcher", "Knife"]
                                for wt in weapon_types:
                                    if wt not in player_instance.weapons:
                                        weapon_drops.append(WeaponDrop(enemy.x, enemy.y, wt))
                                        break
                            enemies.remove(enemy)
                        bullets.remove(bullet)
                        break

            if bullet.is_out_of_bounds():
                bullets.remove(bullet)

        for drop in weapon_drops[:]:
            if drop.check_collision(player_instance):
                player_instance.add_weapon(drop.weapon_type)
                weapon_drops.remove(drop)

        if len(enemies) == 0 and not level_complete:
            level_complete = True

        screen.fill(BACKGROUND)

        for wall in walls:
            wall.draw(screen)

        for drop in weapon_drops:
            drop.draw(screen)

        for bullet in bullets:
            bullet.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        player_instance.draw(screen)

        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        level_text = font.render(f"Level: {current_level}", True, TEXT_COLOR)
        health_text = font.render(f"Health: {player_instance.health}", True, TEXT_COLOR)
        kills_text = font.render(f"Kills: {player_instance.kills}", True, TEXT_COLOR)

        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 60))
        screen.blit(health_text, (20, 100))
        screen.blit(kills_text, (20, 140))

        controls_font = pygame.font.SysFont(None, 24)
        controls = [
            "Controls: WASD - Move, Mouse - Aim, LMB/J - Shoot",
            "R - Reload, Q/E - Switch Weapon, SPACE - Next Level"
        ]

        for i, text in enumerate(controls):
            ctrl_text = controls_font.render(text, True, TEXT_COLOR)
            screen.blit(ctrl_text, (WIDTH - ctrl_text.get_width() - 20, 20 + i * 30))

        weapon_y = HEIGHT - 50
        for i, weapon in enumerate(player_instance.weapons):
            color = WEAPON_HIGHLIGHT if i == player_instance.current_weapon else (100, 100, 100)
            pygame.draw.rect(screen, color, (20 + i * 150, weapon_y, 140, 40))
            pygame.draw.rect(screen, (50, 50, 50), (20 + i * 150, weapon_y, 140, 40), 2)

            weapon_text = controls_font.render(weapon, True, (255, 255, 255))

            if weapon in player_instance.weapon_icons:
                icon = player_instance.weapon_icons[weapon]
                screen.blit(icon, (20 + i * 150 + 70 - icon.get_width() // 2,
                                   weapon_y + 20 - icon.get_height() // 2))
            else:
                screen.blit(weapon_text, (20 + i * 150 + 70 - weapon_text.get_width() // 2, weapon_y + 15))

            if weapon != "Knife":
                ammo_text = controls_font.render(f"{player_instance.ammo[weapon]}/{player_instance.max_ammo[weapon]}",
                                                 True,
                                                 (255, 255, 255))
                screen.blit(ammo_text, (20 + i * 150 + 70 - ammo_text.get_width() // 2, weapon_y + 25))

        if player_instance.health <= 0:
            game_over = True

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
