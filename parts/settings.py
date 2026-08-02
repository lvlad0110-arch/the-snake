import pygame

import parts.constants as const

pygame.init()
pygame.font.init()

# Скорость движения змейки и времени:
clock = pygame.time.Clock()

# Настройка игрового окна:
dis = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

# настройка текста
font = pygame.font.SysFont('Arial', 36)
