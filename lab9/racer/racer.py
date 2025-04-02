import pygame, sys, time
from pygame.locals import *
import random

pygame.init()

# colors
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)

fps = 60
FramePerSec = pygame.time.Clock()

x = 400
y = 600
speed = 5  # initial speed of enemies
score = 0

font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load('road.png')

screen = pygame.display.set_mode((x, y))
screen.fill(white)
pygame.display.set_caption('Car game')

# enemy class
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, y - 40), 0)

    def move(self):
        global speed
        self.rect.move_ip(0, speed)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

# player
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < y:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# coin class with random weights 
class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, y - 30), 0)
        self.weight = random.randint(1, 3)  # randomly coins weight between 1 and 3

    def move(self):
        self.rect.move_ip(0, 5)  # coins move down the screen at constant speed
        if self.rect.top > 600:
            self.kill()  # remove the coin when it moves out of the screen

# function for the game over screen
def game_over():
    my_font = pygame.font.SysFont('Verdana', 20)
    game_over_surface = my_font.render('Your score is: ' + str(score), True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (x / 2, y / 2)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)  # delay to display score before quitting
    pygame.quit()
    quit()

# initialize sprites
P1 = player()
E1 = enemy()
C1 = coin()

# group for all sprites
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# group for coins
coins = pygame.sprite.Group()
coins.add(C1)

# timer event to increase speed and spawn coins
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)  # increase speed every second

spawn_coin = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_coin, 2000)  # spawn coins every 2 seconds

running = True

while running:
    for event in pygame.event.get():
        if event.type == inc_speed:
            if score >= 10:  # after earning 10 coins, increase enemy speed
                speed += 1
            elif score >= 20:  # after earning 20 coins, increase enemy speed more
                speed += 2

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == spawn_coin:
            if len(coins) < 3:  # ensure we don't spawn too many coins at once
                C = coin()
                coins.add(C)
                all_sprites.add(C)

    screen.blit(background, (0, 0))  # draw the background
    scores = small_font.render(str(score), True, black)
    screen.blit(scores, (10, 10))  # display the score on the screen

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)  # draw all sprites
        entity.move()  # move the sprites

    # check if the player collected any coins
    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:
        pygame.mixer.Sound('ding.mp3').play()  # play a sound when collecting a coin
        score += collected_coin.weight  # increase score by the weight of the collected coin
        collected_coin.kill()  # remove the collected coin from the game

    # check if the player collided with any enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.mp3').play()  # play a crash sound
        time.sleep(0.5)  # pause briefly to simulate crash impact

        screen.fill(red)  # fill the screen with red on collision
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # remove all entities from the game
        game_over()  # display the game over screen

    pygame.display.update()
    FramePerSec.tick(fps)  # set the frame rate
