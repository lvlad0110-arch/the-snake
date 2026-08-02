from random import randint

import pygame

import parts.constants as const
import parts.settings as sett
from parts.GameObject import GameObject


class Apple(GameObject):
    """Отвечает за генерирование яблок и их поедание"""

    def __init__(self, color, width=20, height=20):
        # выравниваем положения яблока по "сетке" поля, чтобы
        # координаты сходились
        super().__init__(color, width, height)
        self.x = randint(0, (const.SCREEN_WIDTH // 20 - 1)) * 20
        self.y = randint(0, (const.SCREEN_HEIGHT // 20 - 1)) * 20

    def random_position(self, snake):
        """Генерирует случайные координаты для змейки"""
        while True:
            self.x = randint(0, (const.SCREEN_WIDTH // 20 - 1)) * 20
            self.y = randint(0, (const.SCREEN_HEIGHT // 20 - 1)) * 20
            if (self.x, self.y) not in snake.body:
                break

    def apple_draw(self):
        """Отрисовывает яблоки"""
        pygame.draw.rect(sett.dis, const.COLOR_APPLE,
                         (self.x, self.y, self.width, self.height))

    def apple_consume(self, snake):
        """При съедении яблока увеличивает длину змейки"""
        if snake.body[0] == (self.x, self.y):
            snake.lenght += 1
            return True
