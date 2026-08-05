from random import randint

import pygame

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 36)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE_DIRECTION = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}


SPEED = 10
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

COLOR_SNAKE = (0, 255, 0)
COLOR_APPLE = (255, 0, 0)
TEXT_COL = (255, 255, 255)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
DEF_COLOR = (0, 0, 0)


class GameObject:
    """Инициализируем родительский класс"""

    def __init__(self, body_color=DEF_COLOR):
        self.body_color = body_color
        self.width = GRID_SIZE
        self.height = GRID_SIZE
        self.position = (0, 0)

    def draw(self):
        """Передаем метод для дочерних классов"""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён.'
        )


class Snake(GameObject):
    """Класс, отвечающий за логику змейки"""

    def __init__(self, body_color=DEF_COLOR, direction=' '):
        super().__init__(body_color)
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.direction = direction
        self.positions = [(self.x, self.y)]
        self.length = 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки"""
        # Если новое направление не противоположно текущему, обновляем
        if new_direction != OPPOSITE_DIRECTION.get(self.direction):
            self.direction = new_direction

    def draw(self):
        """Отрисовываем змейку"""
        for axisX, axisY in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             (axisX, axisY, self.width, self.height))

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0] if self.positions else (self.x, self.y)

    def move(self):
        """Метод изменяет direction, который определяет движение змейки"""
        if self.direction != ' ':
            dx, dy = self.direction
            self.x += dx * GRID_SIZE
            self.y += dy * GRID_SIZE
            # Переносит голову змейки через границу экрана
            self.x %= SCREEN_WIDTH
            self.y %= SCREEN_HEIGHT

        # Отвечает за увеличение змейки и останавливает ее бесконечный рост
        self.positions.insert(0, (self.x, self.y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает состояние змейки"""
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.length = 1
        self.positions = [(self.x, self.y)]
        self.direction = ' '


class Apple(GameObject):
    """Отвечает за генерирование яблок и их поедание"""

    def __init__(self, body_color=DEF_COLOR):
        super().__init__(body_color)
        self.x = 0
        self.y = 0
        self.position = (self.x, self.y)

    def randomize_position(self, snake):
        """Генерирует случайные координаты для яблока"""
        self.x, self.y = snake.positions[0]

        while (self.x, self.y) in snake.positions:
            self.x = randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE
            self.y = randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE

        self.position = (self.x, self.y)

    def draw(self):
        """Отрисовывает яблоки"""
        pygame.draw.rect(screen, self.body_color,
                         (self.x, self.y, self.width, self.height))

    def apple_consume(self, snake):
        """При съедении яблока увеличивает длину змейки"""
        if snake.positions[0] == (self.x, self.y):
            snake.length += 1
            return True
        return False


def handle_keys(snake):
    """Обрабатывает нажатия на клавиатуру для управления"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def game_over(snake):
    """Функция отвечает за сброс игры и дает возможность выключить игру"""
    text = font.render('Сыграть еще? (y - да | n - нет)', True, TEXT_COL)
    rect_t = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(BOARD_BACKGROUND_COLOR)
    screen.blit(text, rect_t)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    snake.reset()
                    return
                elif event.key == pygame.K_n:
                    pygame.quit()
                    raise SystemExit


def main():
    """Запускает основной цикл игры"""
    # Создаем экземпляры яблока и змеи
    snake = Snake(COLOR_SNAKE)
    apple = Apple(COLOR_APPLE)
    apple.randomize_position(snake)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        # При съедении яблока увеличивает длину змейки
        # В замечании строки 168 в в.1 проекта указано перенести в мув
        # но у яблока мув нет. Если не плодить функции, то лучше так навреное
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
        elif snake.get_head_position() in snake.positions[1:]:
            game_over(snake)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
