import pygame
import os


pygame.init()

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D射击闯关游戏")


BACKGROUND = (40, 44, 52)
PLAYER_COLOR = (70, 130, 180)
ENEMY_COLOR = (220, 20, 60)
BULLET_COLOR = (255, 215, 0)
WALL_COLOR = (100, 100, 100)
TEXT_COLOR = (220, 220, 220)
HEALTH_BAR = (50, 205, 50)
AMMO_BAR = (255, 140, 0)
WEAPON_HIGHLIGHT = (0, 191, 255)
MELEE_COLOR = (30, 144, 255)


def load_image(name, size=None):
    try:
        image = pygame.image.load(f"{name}.png")
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except:

        surf = pygame.Surface((size or (50, 50)))
        surf.fill((100, 100, 100))
        pygame.draw.rect(surf, (150, 150, 150), surf.get_rect(), 2)
        font = pygame.font.SysFont(None, 20)
        text = font.render(name, True, (255, 255, 255))
        surf.blit(text, (surf.get_width()//2 - text.get_width()//2,
                         surf.get_height()//2 - text.get_height()//2))
        return surf