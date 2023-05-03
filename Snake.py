import random
from os import path
import pygame

pygame.init()

WIDTH = 900
HEIGHT = 650
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (35, 171, 250)
FPS = 45
snake_block = 20
snake_step = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

image_dir = path.join(path.dirname(__file__), 'img')
head = [
    pygame.image.load(path.join(image_dir, 'HeadL.png')),
    pygame.image.load(path.join(image_dir, 'HeadR.png')),
    pygame.image.load(path.join(image_dir, 'HeadB.png')),
    pygame.image.load(path.join(image_dir, 'HeadT.png'))
]


def draw_head(i, snake_list):
    png_i = head[i]
    png_i = pygame.transform.scale(png_i, (snake_block, snake_block))
    png_i_rect = png_i.get_rect(x=snake_list[-1][0], y=snake_list[-1][-1])
    screen.blit(png_i, png_i_rect)


def text(message, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    msg = font_style.render(message, True, color)
    screen.blit(msg, (x, y))


def eating_check(x_cor, y_cor, food_x, food_y):
    if food_x - snake_block <= x_cor <= food_x + snake_block:
        if food_y - snake_block <= y_cor <= food_y + snake_block:
            return True
    else:
        return False


def game_loop():
    snake_list = []
    x_cor = WIDTH / 2
    y_cor = HEIGHT / 2
    clock = pygame.time.Clock()
    length = 1
    x_change = 0
    y_change = 0
    score = 0
    food_x = random.randint(0, WIDTH - snake_block)
    food_y = random.randint(40, HEIGHT - snake_block)
    bg = pygame.image.load(path.join(image_dir, 'Fon_grass4.jpg'))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_rect = bg.get_rect()
    apple = [
        pygame.image.load(path.join(image_dir, 'f_1.png')),
        pygame.image.load(path.join(image_dir, 'f_2.png')),
        pygame.image.load(path.join(image_dir, 'f_3.png')),
        pygame.image.load(path.join(image_dir, 'f_4.png')),
        pygame.image.load(path.join(image_dir, 'f_5.png')),
        pygame.image.load(path.join(image_dir, 'f_6.png')),
        pygame.image.load(path.join(image_dir, 'f_7.png'))
    ]
    food = pygame.transform.scale(random.choice(apple), (snake_block, snake_block))
    food_rect = food.get_rect(x=food_x, y=food_y)
    i = 0
    run_game = True
    while run_game:
        clock.tick(FPS)
        screen.fill(BG)
        screen.blit(bg, bg_rect)
        text(f'Ваш счёт: {score}', WHITE, 10, 10, 'comicsans', 30)
        game_close = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    y_change = -snake_step
                    x_change = 0
                    i = 3
                elif event.key == pygame.K_s:
                    y_change = snake_step
                    x_change = 0
                    i = 2
                elif event.key == pygame.K_d:
                    x_change = snake_step
                    y_change = 0
                    i = 1
                elif event.key == pygame.K_a:
                    x_change = -snake_step
                    y_change = 0
                    i = 0
        y_cor += y_change
        x_cor += x_change
        snake_head = [x_cor, y_cor]
        snake_list.append(snake_head)

        for snake in snake_list[:-1]:
            # pygame.draw.rect(screen, BLACK, (snake[0], snake[1], snake_block, snake_block))
            body = pygame.image.load(path.join(image_dir, 'body.png'))
            body_image = pygame.transform.scale(body, (snake_block, snake_block))
            body_image.set_colorkey(WHITE)
            screen.blit(body_image, (snake[0], snake[1]))
        draw_head(i, snake_list)

        if len(snake_list) > length:
            del snake_list[0]

        if x_cor <= 0 or x_cor >= WIDTH or y_cor <= 0 or y_cor >= HEIGHT:
            run_game = False
            game_close = True
        # pygame.draw.rect(screen, GREEN, (food_x, food_y, snake_block, snake_block))
        screen.blit(food, food_rect)

        if eating_check(x_cor, y_cor, food_x, food_y):
            food_x = random.randint(0, WIDTH - snake_block)
            food_y = random.randint(0, HEIGHT - snake_block)
            length += 1
            score += 1
            apple = [
                pygame.image.load(path.join(image_dir, 'f_1.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_2.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_3.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_4.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_5.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_6.png')).convert(),
                pygame.image.load(path.join(image_dir, 'f_7.png')).convert()
            ]
            food = pygame.transform.scale(random.choice(apple), (snake_block, snake_block))
            food.set_colorkey(WHITE)
            food_rect = food.get_rect(x=food_x, y=food_y)

        for d in snake_list[:-1]:
            if d == snake_head:
                run_game = False
                game_close = True

        while game_close:

            screen.fill(BLACK)
            text('Вы проиграли!!', WHITE, 270, 230, 'comicsans', 45)
            text('Для выхода нажмите Q', WHITE, 270, 300, 'comicsans', 30)
            text('Для перезапуска нажмите R', WHITE, 240, 330, 'comicsans', 30)
            text('Для перезапуска нажмите R', WHITE, 240, 330, 'comicsans', 30)
            text(f'Ваш счёт: {score}', WHITE, 360, 360, 'comicsans', 30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_game = False
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        run_game = False
                        game_close = False
                    elif event.key == pygame.K_r:
                        run_game = False
                        game_close = False
                        game_loop()

            pygame.display.update()

        pygame.display.flip()


game_loop()
pygame.quit()
quit()
