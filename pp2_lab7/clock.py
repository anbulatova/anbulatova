import pygame
from datetime import datetime

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey's Clock")

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

right_hand = pygame.image.load("rightarm.png").convert_alpha()
left_hand = pygame.image.load("leftarm.png").convert_alpha()
clockimg = pygame.image.load('clock.jpg')
clockimg = pygame.transform.scale(clockimg, (600, 600))
right_hand = pygame.transform.scale(right_hand, (1000, 1000))
left_hand = pygame.transform.scale(left_hand,(63, 850) )

mickey_rect = clockimg.get_rect(center=(600 // 2, 600 // 2))
right_hand_center = (mickey_rect.centerx + 10, mickey_rect.centery )  
left_hand_center = (mickey_rect.centerx - 10, mickey_rect.centery )

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  

    now = datetime.now()
    minutes = now.minute
    seconds = now.second

    minute_angle = -minutes * 6  
    second_angle = -seconds * 6  

    rotated_right_hand = pygame.transform.rotate(right_hand, minute_angle)
    rotated_left_hand = pygame.transform.rotate(left_hand, second_angle)

    right_rect = rotated_right_hand.get_rect(center=(30, 30))  
    left_rect = rotated_left_hand.get_rect(center=(30, 30))  

    screen.blit(clockimg, (0, 0))
    right_hand_rotated = pygame.transform.rotate(right_hand, minute_angle)
    right_hand_rect = right_hand_rotated.get_rect(center=right_hand_center)
    screen.blit(right_hand_rotated, right_hand_rect.topleft)

    left_hand_rotated = pygame.transform.rotate(left_hand, second_angle)
    left_hand_rect = left_hand_rotated.get_rect(center=left_hand_center)
    screen.blit(left_hand_rotated, left_hand_rect.topleft)


    pygame.display.update()
