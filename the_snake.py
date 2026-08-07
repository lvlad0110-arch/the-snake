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

START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
DEFAULT_POSITION = (0, 0)

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
DEFAULT_COLOR = (0, 0, 0)


class GameObject:
    """Инициализируем родительский класс"""

    def __init__(self, body_color=DEFAULT_COLOR):
        self.body_color = body_color
        self.position = DEFAULT_POSITION

    def draw(self):
        """Передаем метод для дочерних классов"""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён.'
        )


class Snake(GameObject):
    """Класс, отвечающий за логику змейки"""

    def __init__(self, body_color=DEFAULT_COLOR, direction=None):
        super().__init__(body_color)
        self.reset()
        self.direction = direction
        self.positions = [self.position]
        self.length = 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки"""
        # Если новое направление не противоположно текущему, обновляем
        if new_direction != OPPOSITE_DIRECTION.get(self.direction):
            self.direction = new_direction

    def draw(self):
        """Отрисовываем змейку"""
        for axis_x, axis_y in self.positions:
            pygame.draw.rect(screen, self.body_color,
                             (axis_x, axis_y, GRID_SIZE, GRID_SIZE))

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.position

    def move(self):
        """Двигает змейку"""
        if self.direction is not None:
            direction_x, direction_y = self.direction
            location_x, location_y = self.position
            location_x = (location_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
            location_y = (location_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
            self.position = (location_x, location_y)

        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает состояние змейки"""
        self.position = START_POSITION
        self.length = 1
        self.positions = [self.position]
        self.direction = None


class Apple(GameObject):
    """Отвечает за генерирование яблок и их поедание"""

    def __init__(self, body_color=DEFAULT_COLOR):
        super().__init__(body_color)
        self.position = START_POSITION

    def randomize_position(self, snake):
        """Генерирует случайную позицию яблока."""
        while self.position in snake.positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self):
        """Отрисовывает яблоки"""
        pygame.draw.rect(screen, self.body_color,
                         (*self.position, GRID_SIZE, GRID_SIZE))


def handle_keys(snake):
    """Обрабатывает нажатия на клавиатуру для управления"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def terminate():
    """Функция вызывает выход из игры"""
    pygame.quit()
    raise SystemExit


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
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    snake.reset()
                    return
                elif event.key == pygame.K_n:
                    terminate()


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
        screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)
        elif snake.get_head_position() in snake.positions[1:]:
            game_over(snake)
            apple.randomize_position(snake)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
