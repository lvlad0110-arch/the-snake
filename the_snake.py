import pygame

from random import randint

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial', 36)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

FPS = 20
clock = pygame.time.Clock()
dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

COLOR_SNAKE = (0, 255, 0)
COLOR_APPLE = (255, 0, 0)
TEXT_COL = (255, 255, 255)
BOARD_BG = (0, 0, 0)


class GameObject:
    '''Инициализируем родитлельский край'''

    def __init__(self, color, x, y, width=20, height=20):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        '''передаем пустой метод отрисовки для дочерних классов'''
        pass


class Snake(GameObject):
    '''Класс, отвечающий за логику змейки'''

    def __init__(self, color, x, y, width=20, height=20, direction=' '):
        super().__init__(color, x, y, width, height)
        self.direction = direction
        self.position = [(self.x, self.y)]
        self.lenght = 1

    def draw(self):
        '''Отрисовываем змейку'''
        for x, y in self.position:
            pygame.draw.rect(dis, self.color, (x, y, self.width, self.height))

    def move(self):
        '''Метод изменяет direction, который определяет движение змейки'''
        if self.direction == 'UP':
            self.y -= 20
        elif self.direction == 'DOWN':
            self.y += 20
        elif self.direction == 'LEFT':
            self.x -= 20
        elif self.direction == 'RIGHT':
            self.x += 20

    def update_body(self):
        '''
        Метод отвечает за увеличение змейки и останавливает
        ее бесконечный рост
        '''
        # добавляем голову в начало списка
        self.position.insert(0, (self.x, self.y))
        # Удаляем последний сегмент (хвост), чтобы длина оставалась постоянной
        if len(self.position) > self.lenght:
            self.position.pop()

    def border_transition(self):
        '''Метод переносит голову змеюки через границу экрана'''
        # из максимальной ширины вычитается 10px, тк змейка может
        # застрять ровно на 640
        if self.x > SCREEN_WIDTH - 10:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH
        # из максимальной высоты вычитается 10px, тк змейка может
        # застрять ровно на 480, и не перейдет
        elif self.y > SCREEN_HEIGHT - 10:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT

    def collision_check(self):
        '''Метод проверяет столкновения'''
        return (self.x, self.y) in self.position[1:]

    def snake_reset(self):
        '''Метод отвечает за сброс игры и дает возможность выключить игру'''
        text = font.render('Сыграть еще? (y - да | n - нет)', True, TEXT_COL)
        rect_t = text.get_rect(center=(SCREEN_WIDTH // 2,
                                       SCREEN_HEIGHT // 2))
        if self.collision_check():
            dis.fill((BOARD_BG))
            dis.blit(text, rect_t)
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
                            self.position = [(self.x, self.y)]
                            self.lenght = 1
                            self.direction = ' '
                            return
                        elif event.key == pygame.K_n:
                            pygame.quit()
                            raise SystemExit


class Apple(GameObject):
    '''Отвечает за генерирование яблок и их поедание'''

    def __init__(self, color, width=20, height=20):
        # выравниваем положения яблока по "сетке" поля, чтобы
        # координаты сходились
        super().__init__(color, width, height)
        self.x = randint(0, (SCREEN_WIDTH // 20 - 1)) * 20
        self.y = randint(0, (SCREEN_HEIGHT // 20 - 1)) * 20

    def random_position(self, snake):
        '''Генерирует случайные координаты для змейки'''
        while True:
            self.x = randint(0, (SCREEN_WIDTH // 20 - 1)) * 20
            self.y = randint(0, (SCREEN_HEIGHT // 20 - 1)) * 20

            if (self.x, self.y) not in snake.position:
                break

    def apple_draw(self):
        '''Отрисовывает яблоки'''
        pygame.draw.rect(dis, COLOR_APPLE,
                         (self.x, self.y, self.width, self.height))

    def apple_consume(self, snake):
        '''При съедении яблока увеличивает длину змейки'''
        if snake.position[0] == (self.x, self.y):
            snake.lenght += 1
            return True


def handle_keys(snake):
    '''Обрабатывает нажатия на клавиатуру для управления'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.direction = "RIGHT"


def main():
    '''Запускает основной цикл игры'''
    # Инициализация PyGame:
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()

    pygame.display.set_caption('Змейка')

    # Создаем эксемпляры яблока и змеи
    snake = Snake(COLOR_SNAKE, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2)
    apple = Apple(COLOR_APPLE)

    running = True
    while running:
        handle_keys(snake)
        snake.move()
        snake.border_transition()
        snake.update_body()
        dis.fill((0, 0, 0))
        if apple.apple_consume(snake):
            apple.random_position(snake)
        apple.apple_draw()
        snake.draw()
        pygame.display.update()
        if snake.collision_check():
            snake.snake_reset()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
