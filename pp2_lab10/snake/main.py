import pygame              
import random              
import psycopg2
from insert_name import insert_data
from create import create_tables
from update import update

create_tables() # Создание таблиц в базе данных PostgreSQL

name = ""

while not name:
    name = input("Введите ник: ")
    insert_data(name)   # Вставка ника в базу данных

    
pygame.init() 

SW, SH = 600, 600 # Размер игрового поля
WW, WH = 600, 700 # Размер окна

BLOCK_SIZE = 40 # Размер блока
FONT = pygame.font.SysFont("arialполужирный", BLOCK_SIZE)    

screen = pygame.display.set_mode((WW, WH))
pygame.display.set_caption("snake")
clock = pygame.time.Clock() # Для контроля скорости игры

class Snake:  # Класс для управления змеей
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE) # Прямоугольник для головы 
        self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)] # Тело в виде сета прямоугольников
        self.dead = False # Флаг указывающий на смерть
        self.restart = False # Флаг указывающий на нажатие клавиши перезапуска

    def update(self):
        global apple, wall, golden_apple

        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y: # Проверка на столкновения головы змеи с телом
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH): # Проверка выхода из зоны
                self.dead = True
                
        # Перезапуск игры если змея мертва и перезапуск выполнен правильно
        if self.dead and self.restart:
                self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
                self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.xdir = 1
                self.ydir = 0
                self.dead = False
                self.restart = False
                apple = Apple() # Создает яблоко
                wall = Wall() # Создает стену
                golden_apple = GoldenApple(self.body, (apple.x, apple.y), [barrier for barrier in wall.barriers]) # Создает золотое яблоко
        # Обновление позиции змеи
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body.remove(self.head)

class Apple: # Класс для управления яблоками
    def __init__(self):
        self.spawn_apple()
        self.spawn_time = pygame.time.get_ticks() 
        
    # Способ создания новой позиции для яблока
    def spawn_apple(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        
    # Способ обновления положения и рисования яблока
    def update(self, snake_body): 
        if pygame.time.get_ticks() - self.spawn_time >= 5000: # 5000 => milliseconds 
            self.spawn_apple() 
            self.spawn_time = pygame.time.get_ticks()
        while (self.x, self.y) in [(square.x, square.y) for square in snake_body]:
            self.spawn_apple()
        self.new_apple = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, "red", self.new_apple)

class GoldenApple: # Класс для управления золотыми яблоками
    def __init__(self, snake_body, apple_pos, wall_barriers):
        
        # Определение времени появления золотого яблока
        self.spawn_time = pygame.time.get_ticks()
        self.golden_apple_rect = None
        if random.random() <= 0.1: # Рандомайзер золотого яблока
            self.spawn_golden_apple(snake_body, apple_pos, wall_barriers) 
            
    # Метод спавна золотых яблок
    def spawn_golden_apple(self, snake_body, apple_pos, wall_barriers):
        while True:
            self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
            
            # Проверка пересечения координат с телом змеи, яблоком или стенкой
            if (self.x, self.y) not in apple_pos and \
               (self.x, self.y) not in [(square.x, square.y) for square in snake_body] and \
               (self.x, self.y) not in [(barrier.x, barrier.y) for barrier in wall_barriers]:
                   
                # Создаем золотое яблоко
                self.golden_apple_rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                break
    # Способ обновления положения золотого яблока
    def update(self, snake_body, apple_pos, wall_barriers):
        current_time = pygame.time.get_ticks()

        if self.golden_apple_rect is not None: # Проверка существования золотого яблока
            if current_time - self.spawn_time >= 3000: # Проверка времени существования яблока
                self.golden_apple_rect = None  
        else: # если не существует, проверяет создание нового
            if random.random() <= 0.1:  
                self.spawn_golden_apple(snake_body, apple_pos, wall_barriers)
                self.spawn_time = current_time

        if self.golden_apple_rect is not None: # Рисовка золотого яблока если оно существует
            pygame.draw.rect(screen, "gold", self.golden_apple_rect)

class Wall: # Класс для управления стенами
    def __init__(self):
        self.barriers = []
        
    # Способ создания новых стен
    def spawn_barrier(self, snake_body, apple_pos, snake_head_pos):
        while True:
            self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
            new_barrier = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
             
            # Условие гарантирует, что новая стенка не столкнется с частью тела змеи и не совпадет с положением яблока
            if new_barrier.collidelist(snake_body) == -1 and new_barrier.collidepoint(apple_pos) == False:
                # Условие гарантирует, что новая стенка не будет расположена слишком близко к голове змеи. (минимум 3 клетки от головы змеи)  
                if abs(snake_head_pos[0] - new_barrier.x) > 3 * BLOCK_SIZE or abs(snake_head_pos[1] - new_barrier.y) > 3 * BLOCK_SIZE:
                    self.barriers.append(new_barrier)
                    break  
                  
    # Способ обновления стен
    def update(self, snake_body, apple_pos, snake_head_pos, eaten_fruits):
        for barrier in self.barriers:
            pygame.draw.rect(screen, "blue", barrier)
            if barrier.colliderect(snake_head_pos): # Проверка на столкновение со стенками
                snake.dead = True

        eaten_fruits = eaten_fruits // 2 # После каждого второго съеденного фрукта добавляется новая стенка
        if eaten_fruits > len(self.barriers):
            for _ in range(eaten_fruits - len(self.barriers)):
                self.spawn_barrier(snake_body, apple_pos, snake_head_pos)
                
def drawGrid():  # Функция для рисования игровой сетки
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (60, 60, 60), rect, 1)

# Инициализация переменных очков, скорости и съеденных фруктов
score = speed = eaten_fruits = 0
scoretxt = speedtxt = leveltxt = FONT.render("0", True, "white")
score_rect = scoretxt.get_rect(center=(20, 620))
speed_rect = speedtxt.get_rect(center=(20, 660))
level_rect = leveltxt.get_rect(center=(480, 620))

drawGrid()
# Создание объектов 
snake = Snake()
apple = Apple()
wall = Wall()
golden_apple = GoldenApple(snake.body, (apple.x, apple.y), [barrier for barrier in wall.barriers])

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Выход из игры
                done = True
            elif event.key == pygame.K_SPACE: # Рестарт игры
                snake.restart = True
                score = speed = eaten_fruits = 0
            if event.key == pygame.K_DOWN: 
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()

    screen.fill("black")

    drawGrid()

    wall.update(snake.body, (apple.x, apple.y), snake.head, eaten_fruits)

    apple.update(snake.body)

    golden_apple.update(snake.body, (apple.x, apple.y), [barrier for barrier in wall.barriers])

    pygame.draw.rect(screen, (0, 255, 0), snake.head) # Рисование головы змеи
    pygame.draw.rect(screen, (42, 42, 42), [0, SH, WW, WH]) # Рисование поверхности для отображения некоторых стат данных
    
    # Отображение текущих значений очков, скорости и уровня 
    scoretxt = FONT.render(f"score: {score}", True, (138, 154, 91)) 
    speedtxt = FONT.render(f"speed: {speed + 5}", True, (96, 130, 182))
    leveltxt = FONT.render(f"level: {eaten_fruits//2}", True, (207, 159, 255))
    
    # Отображение результата, скорости и уровня на экране
    screen.blit(scoretxt, score_rect)
    screen.blit(speedtxt, speed_rect)
    screen.blit(leveltxt, level_rect)

    # Рисование тела змеи
    for square in snake.body:
        pygame.draw.rect(screen, (0, 65, 0), square)

    # Проверка золотого яблока на экране и x,y головы == x,y яблока
    if golden_apple.golden_apple_rect is not None and snake.head.colliderect(golden_apple.golden_apple_rect): # Работает как яблоко но с 3х очками
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
        golden_apple = GoldenApple(snake.body, (apple.x, apple.y), [barrier for barrier in wall.barriers])
        eaten_fruits += 1
        score += 3
        if (len(snake.body)-1) % 5 == 0: 
            speed += 0.5

    # Проверка если x,y головыв == x,y яблока
    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE)) 
        apple = Apple() # Создание нового яблока после съедение прошлого 
        eaten_fruits += 1
        score += 1
        if (len(snake.body)-1) % 5 == 0: # Увеличение скорости после каждого второго яблока
            speed += 0.5

    # Проверка что новое яблоко не будет создано на существующей стенке
    for barrier in wall.barriers:
        if apple.x == barrier[0] and apple.y == barrier[1]: # Иначе новая генерация яблока
            apple.spawn_apple()

    # Game over когда змея умирает
    if snake.dead and not snake.restart:
        answer = ""
        update(nickname=name, score=score)
        screen.fill("black")
        endtxt = FONT.render(f"your score: {score}", True, "red") 
        end_rect = endtxt.get_rect(center=(SW/2, SH/2))
        screen.blit(endtxt, end_rect)
        while not answer:
            answer = input(f"Ты набрал {score} очков? хочешь поменять на свой же рекорд? (y/n):   ")
            if answer == "y":
                update(nickname=name, score=score)
            elif answer == "n":
                break
            else:
                answer = ""
        break

    pygame.display.update() # Обновление экрана
    clock.tick(5 + speed) # Фпс для контроля скорости игры