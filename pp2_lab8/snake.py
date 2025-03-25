import pygame, time, random

#windows size
x = 600
y = 450

#initial snale speed
speed = 10

#colors
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
red = pygame.Color(255, 0, 0)

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Snake game')
screen = pygame.display.set_mode((600, 450))

#images
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (600, 450))

head = pygame.image.load('head.png')
head = pygame.transform.scale(head, (10, 10))

body = pygame.image.load('snake_part.png')
body = pygame.transform.scale(body, (10, 10))

apple = pygame.image.load('apple.png')
apple = pygame.transform.scale(apple, (10, 10))

title = pygame.image.load('title.png')
title = pygame.transform.scale(title, (600, 450))

#object for controllinf FPS
fps = pygame.time.Clock()

#initial sneke coordinates
snake_position = [100, 50]
snake_body = [[100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ]

#generate food
fruit_position = [ random.randrange(1, (x // 10)) * 10,
                  random.randrange(1, (y // 10)) * 10]

fruit_spawn = True

#snake movement direction
direction = 'RIGHT'
change_to = direction

#variables for score and level
score = 0
level = 1

#function to display score and level
def show_result():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}  Level: {level}', True, white)
    screen.blit(score_surface, (10, 10))

#function to end the game
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your score is: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (x / 2, y / 2)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def title_start():
    screen.blit(title, (0, 0))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

title_start()

running = True
while running:
    #control events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key  == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #move the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    #add new head to the body list
    snake_body.insert(0, list(snake_position))
    #check if the snake eats the fruit
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        sound = pygame.mixer.Sound("ding.mp3")
        pygame.mixer.Sound.play(sound)
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    last_level = level
    #increase level every 3 fruits
    if score % 30 == 0 and score > 0 and level != last_level:
        level = score // 30 + 1
        speed += 0.5 #increase snake speed
        last_level = level
    

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (x // 10)) * 10,
                          random.randrange(1, (y // 10)) * 10]
    
    fruit_spawn = True
    screen.blit(background, (0, 0))

    screen.blit(head, (snake_body[0][0], snake_body[0][1]))
    for block in snake_body[1:]:
        screen.blit(body, (block[0], block[1]))

    screen.blit(apple, (fruit_position[0], fruit_position[1]))

    if snake_position[0] < 0 or snake_position[0] > x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1]  == block[1]:
            game_over()

    show_result()
    

    pygame.display.update()
    fps.tick(speed)