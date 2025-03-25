import pygame

pygame.init()


x, y = 800, 600
fps = 60
screen = pygame.display.set_mode([x, y])
pygame.display.set_caption('Paint')
timer = pygame.time.Clock()


canvas = pygame.Surface((x, y))
canvas.fill('white')

# Цвета
colors = {'blue': (0, 0, 255), 'green': (0, 255, 0), 'red': (255, 0, 0), 'eraser': (255, 255, 255)}
mode = 'blue'  
shape = 'circle'  

def menu():
    pygame.draw.rect(screen, 'gray', [0, 0, x, 70])
    blue = pygame.draw.rect(screen, (0, 0, 255), [100, 10, 30, 30])
    green = pygame.draw.rect(screen, (0, 255, 0), [150, 10, 30, 30])
    red = pygame.draw.rect(screen, (255, 0, 0), [200, 10, 30, 30])
    circle_btn = pygame.draw.rect(screen, (200, 200, 200), [300, 10, 100, 30])
    rect_btn = pygame.draw.rect(screen, (200, 200, 200), [420, 10, 100, 30])
    eraser_btn = pygame.draw.rect(screen, (200, 200, 200), [540, 10, 100, 30])
    return {'blue': blue, 'green': green, 'red': red, 'circle': circle_btn, 'rect': rect_btn, 'eraser': eraser_btn}

running = True
while running:
    timer.tick(fps)
    screen.fill('white')
    screen.blit(canvas, (0, 0))  
    buttons = menu()
    
    font = pygame.font.Font(None, 25)
    screen.blit(font.render("B", True, (0, 0, 255)), (100, 45))
    screen.blit(font.render("G", True, (0, 255, 0)), (150, 45))
    screen.blit(font.render("R", True, (255, 0, 0)), (200, 45))
    screen.blit(font.render("C - Circle", True, (0, 0, 0)), (310, 15))
    screen.blit(font.render("S - Rect", True, (0, 0, 0)), (430, 15))
    screen.blit(font.render("E - Eraser", True, (0, 0, 0)), (560, 15))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = 'red'
            elif event.key == pygame.K_g:
                mode = 'green'
            elif event.key == pygame.K_b:
                mode = 'blue'
            elif event.key == pygame.K_c:
                shape = 'circle'
            elif event.key == pygame.K_s:
                shape = 'rect'
            elif event.key == pygame.K_e:
                mode = 'eraser'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for key, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    if key in colors:
                        mode = key
                    elif key == 'circle':
                        shape = 'circle'
                    elif key == 'rect':
                        shape = 'rect'
                    elif key == 'eraser':
                        mode = 'eraser'
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if shape == 'circle':
                pygame.draw.circle(canvas, colors[mode], event.pos, 10)
            elif shape == 'rect':
                pygame.draw.rect(canvas, colors[mode], (event.pos[0] - 10, event.pos[1] - 10, 20, 20))
    
    pygame.display.update()

pygame.quit()
