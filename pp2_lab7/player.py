import pygame, sys, time

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Player")

playlist = ["song1.mp3", "song2.mp3", "song3.mp3"]
index = 0

font = pygame.font.Font(None, 24)

def text(text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def play():
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def next_song():
    global index
    index = (index + 1) % len(playlist)
    play()

def previous_song():
    global index
    index = (index - 1) % len(playlist)
    play()

play()

running = True
while running:
    screen.fill((30, 30, 30))  

    text("Music Player", 150, 20, (0, 255, 0))
    text("P - Play", 150, 60)
    text("S - Stop", 150, 90)
    text("N - Next Song", 150, 120)
    text("R - Previous Song", 150, 150)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_n:
                next_song()
            elif event.key == pygame.K_r:
                previous_song()



pygame.quit()