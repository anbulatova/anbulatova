import pygame, sys, time
from pygame.locals import * 
import random

pygame.init()

#colors
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)

fps = 60
FramePerSec = pygame.time.Clock()

x = 400
y = 600
speed = 5
score = 0

font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load('road.png')

screen = pygame.display.set_mode((x, y))
screen.fill(white)
pygame.display.set_caption('Car game')

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, y - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

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
 
class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, y - 30), 0)

    def move(self):
        self.rect.move_ip(0,5)
        if (self.rect.top > 600):
            self.kill()

def game_over():
    my_font = pygame.font.SysFont('Verdana', 20)
    game_over_surface = my_font.render('Your score is: ' + str(score), True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (x / 2, y / 2)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

P1 = player()
E1 = enemy()
C1 = coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

coins = pygame.sprite.Group()
coins.add(C1)


inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

spawn_coin = pygame.USEREVENT + 2
pygame.time.set_timer(spawn_coin, 2000) 

running = True

while running:
    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 2  

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == spawn_coin:
            if len(coins) < 3:  
                C = coin()
                coins.add(C)
                all_sprites.add(C)

    screen.blit(background, (0, 0))
    scores = small_font.render(str(score), True, black)
    screen.blit(scores, (10, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    collected_coin = pygame.sprite.spritecollideany(P1, coins)
    if collected_coin:  # Проверяем, есть ли монета, с которой столкнулся игрок
        pygame.mixer.Sound('ding.mp3').play()
        score += 1
        collected_coin.kill()
        

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.mp3').play()
        time.sleep(0.5)

        screen.fill(red)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        game_over()
        pygame.quit()
        sys.exit()


    pygame.display.update()
    FramePerSec.tick(fps)
