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

UP = (1, 0)
DOWN = (-1, 0)
LEFT = (0, 1)
RIGHT = (0, -1)
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

    def __init__(self, DEF_COLOR, x=0, y=0, width=20, height=20):
        self.body_color = DEF_COLOR
        self.position = (x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """передаем пустой метод отрисовки для дочерних классов"""
        pass


class Snake(GameObject):
    """Класс, отвечающий за логику змейки"""

    def __init__(self, body_color=(0, 255, 0), x=0, y=0,
                 width=20, height=20, direction=' '):
        super().__init__(body_color, x, y, width, height)
        self.direction = direction
        self.positions = [(self.x, self.y)]
        self.length = 1

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки"""
        # Проверяем, чтобы змейка не могла повернуть на 180 градусов

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
        if self.direction == UP:
            self.y -= GRID_SIZE
        elif self.direction == DOWN:
            self.y += GRID_SIZE
        elif self.direction == LEFT:
            self.x -= GRID_SIZE
        elif self.direction == RIGHT:
            self.x += GRID_SIZE

    def update_body(self):
        """
        Метод отвечает за увеличение змейки и останавливает
        ее бесконечный рост
        """
        self.positions.insert(0, (self.x, self.y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def border_transition(self):
        """Метод переносит голову змейки через границу экрана"""
        if self.x >= SCREEN_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH - GRID_SIZE
        elif self.y >= SCREEN_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT - GRID_SIZE

    def collision_check(self):
        """Метод проверяет столкновения"""
        return (self.x, self.y) in self.positions[1:]

    def reset(self):
        """Метод отвечает за сброс игры и дает возможность выключить игру"""
        text = font.render('Сыграть еще? (y - да | n - нет)', True, TEXT_COL)
        rect_t = text.get_rect(center=(SCREEN_WIDTH // 2,
                                       SCREEN_HEIGHT // 2))
        if self.collision_check():
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
                            self.x = SCREEN_WIDTH // 2
                            self.y = SCREEN_HEIGHT // 2
                            self.positions = [(self.x, self.y)]
                            self.length = 1
                            self.direction = ' '
                            return
                        elif event.key == pygame.K_n:
                            pygame.quit()
                            raise SystemExit


class Apple(GameObject):
    """Отвечает за генерирование яблок и их поедание"""

    def __init__(self, body_color=(255, 0, 0), width=20, height=20):
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
        super().__init__(body_color, x, y, width, height)
        self.position = (self.x, self.y)

    def randomize_position(self, snake):
        """Генерирует случайные координаты для яблока"""
        while True:
            self.x = randint(0, (SCREEN_WIDTH // GRID_SIZE - 1)) * GRID_SIZE
            self.y = randint(0, (SCREEN_HEIGHT // GRID_SIZE - 1)) * GRID_SIZE
            self.position = (self.x, self.y)

            if (self.x, self.y) not in snake.positions:
                break

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


def main():
    """Запускает основной цикл игры"""
    # Создаем экземпляры яблока и змеи
    snake = Snake(COLOR_SNAKE, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2)
    apple = Apple(COLOR_APPLE)

    running = True
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.border_transition()
        snake.update_body()
        screen.fill(BOARD_BACKGROUND_COLOR)
        if apple.apple_consume(snake):
            apple.randomize_position(snake)
        apple.draw()
        snake.draw()
        pygame.display.update()
        if snake.collision_check():
            snake.reset()


if __name__ == '__main__':
    main()
