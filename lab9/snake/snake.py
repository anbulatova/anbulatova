import pygame, time, random

# Window size
x = 600
y = 450

# Initial snake speed
speed = 10

# Colors for various game elements
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
red = pygame.Color(255, 0, 0)

# Initialize pygame and set up the display
pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Snake game')
screen = pygame.display.set_mode((600, 450))

# Load images for the game (background, snake, food)
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

# Object to control the FPS (Frames per second)
fps = pygame.time.Clock()

# Initial position of the snake (head and body)
snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

# Class for creating food items
class Food:
    def __init__(self):
        # Random position for food on the screen
        self.position = [random.randrange(1, (x // 10)) * 10,
                         random.randrange(1, (y // 10)) * 10]
        # Random weight between 5 and 15
        self.weight = random.randint(5, 15)
        # Timestamp to check how long the food has been on the screen
        self.timer = pygame.time.get_ticks()

    def move(self):
        # If the food has been on the screen for more than 5 seconds (5000 ms), it disappears
        if pygame.time.get_ticks() - self.timer > 5000:
            return False
        return True

# Initialize food item
fruit = Food()

# Snake movement direction
direction = 'RIGHT'
change_to = direction

# Variables to track score and level
score = 0
level = 1

# Function to display the current score and level
def show_result():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}  Level: {level}', True, white)
    screen.blit(score_surface, (10, 10))

# Function to display "Game Over" message
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

# Title screen function for starting the game
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

# Main game loop
running = True
while running:
    # Handle control events (key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Update direction based on user input, avoid reversing the snake
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Move the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Add new head to the snake body
    snake_body.insert(0, list(snake_position))

    # Check if the snake eats the fruit
    if snake_position[0] == fruit.position[0] and snake_position[1] == fruit.position[1]:
        sound = pygame.mixer.Sound("ding.mp3")
        pygame.mixer.Sound.play(sound)
        score += fruit.weight  # Add the weight of the food to the score
        fruit = Food()  # Spawn a new food item

    else:
        snake_body.pop()  # Remove the last part of the snake if no food is eaten

    # Increase level after eating a certain amount of food (3 fruits = level up)
    last_level = level
    if score % 30 == 0 and score > 0 and level != last_level:
        level = score // 30 + 1
        speed += 0.5  # Increase the snake speed when the level increases
        last_level = level

    # Check if the food has expired (disappeared)
    if not fruit.move():
        fruit = Food()  # Respawn the food if it disappears after 5 seconds

    # Draw everything on the screen
    screen.blit(background, (0, 0))  # Draw the background
    screen.blit(head, (snake_body[0][0], snake_body[0][1]))  # Draw snake head
    for block in snake_body[1:]:
        screen.blit(body, (block[0], block[1]))  # Draw snake body

    screen.blit(apple, (fruit.position[0], fruit.position[1]))  # Draw food

    # Check if the snake hits the boundaries (walls) or itself
    if snake_position[0] < 0 or snake_position[0] > x - 10:
        game_over()  # End game if snake hits the wall
    if snake_position[1] < 0 or snake_position[1] > y - 10:
        game_over()  # End game if snake hits the wall

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()  # End game if snake collides with itself

    show_result()  # Display current score and level

    pygame.display.update()  # Update the game screen
    fps.tick(speed)  # Control the speed of the game loop
