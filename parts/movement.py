import pygame

pygame.init()


def handle_keys(snake):
    '''Обрабатывает нажатия на клавиатуру для управления'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.direction = 'RIGHT'
