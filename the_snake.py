import pygame

import parts.settings as sett
from parts import constants as const
from parts.apple import Apple
from parts.movement import handle_keys as movement
from parts.snake import Snake


def main():
    """Запускает основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    pygame.font.init()

    clock = pygame.time.Clock()

    pygame.display.set_caption('Змейка')

    # Создаем эксемпляры яблока и змеи
    snake = Snake(const.COLOR_SNAKE, const.SCREEN_WIDTH // 2,
                  const.SCREEN_HEIGHT // 2)
    apple = Apple(const.COLOR_APPLE)

    running = True
    while running:
        movement(snake)
        snake.move()
        snake.border_transition()
        snake.update_body()
        sett.dis.fill((const.BOARD_BG))
        if apple.apple_consume(snake):
            apple.random_position(snake)
        apple.apple_draw()
        snake.draw()
        pygame.display.update()
        if snake.collision_check():
            snake.snake_reset()
        clock.tick(const.FPS)


if __name__ == '__main__':
    main()
