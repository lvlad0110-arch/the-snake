import pygame
import parts.constants as const
import parts.settings as sett
from parts.GameObject import GameObject


class Snake(GameObject):
    """Класс, отвечающий за логику змейки"""

    def __init__(self, color, x, y, width=20, height=20, direction=' '):
        super().__init__(color, x, y, width, height)
        self.direction = direction
        self.body = [(self.x, self.y)]
        self.lenght = 1

    def draw(self):
        """Отрисовываем змейку"""
        for x, y in self.body:
            pygame.draw.rect(sett.dis, self.color,
                             (x, y, self.width, self.height))

    def move(self):
        """
        Метод изменяет direction, который определяет
        движение змейки
        """
        if self.direction == 'UP':
            self.y -= 20
        elif self.direction == 'DOWN':
            self.y += 20
        elif self.direction == 'LEFT':
            self.x -= 20
        elif self.direction == 'RIGHT':
            self.x += 20

    def update_body(self):
        """Метод отвечает за увеличение змейки и останавливает
        ее бесконечный рост
        """
        self.body.insert(0, (self.x, self.y))
        # Удаляем последний сегмент (хвост), чтобы длина
        # оставалась постоянной
        if len(self.body) > self.lenght:
            self.body.pop()

    def border_transition(self):
        """Метод переносит голову змеюки через границу экрана"""
        # из максимальной ширины вычитается 10px, тк змейка может
        # застрять ровно на 640
        if self.x > const.SCREEN_WIDTH - 10:
            self.x = 0
        elif self.x < 0:
            self.x = const.SCREEN_WIDTH
        # из максимальной высоты вычитается 10px, тк змейка может
        # застрять ровно на 480, и не перейдет
        elif self.y > const.SCREEN_HEIGHT - 10:
            self.y = 0
        elif self.y < 0:
            self.y = const.SCREEN_HEIGHT

    def collision_check(self):
        """Метод проверяет столкновения"""
        if (self.x, self.y) in self.body[1:]:
            return True
        return False

    def snake_reset(self):
        """Метод отвечает за сброс игры и дает возможность выключить игру"""
        text = sett.font.render("Сыграть еще? (y - да | n - нет)",
                                True, const.TEXT_COL)
        rect_t = text.get_rect(center=(const.SCREEN_WIDTH // 2,
                                       const.SCREEN_HEIGHT // 2))
        if self.collision_check():
            sett.dis.fill((const.BOARD_BG))
            sett.dis.blit(text, rect_t)
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                    elif event.key == pygame.K_y:
                        self.x = const.SCREEN_WIDTH // 2
                        self.y = const.SCREEN_HEIGHT // 2
                        self.body = [(self.x, self.y)]
                        self.lenght = 1
                        self.direction = ' '
                        return
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        raise SystemExit
