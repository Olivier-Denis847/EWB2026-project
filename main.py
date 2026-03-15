import pygame
import sys
import button

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
PLAY_BUTTON = button.Button((0, 255, 0), (WIDTH // 2, HEIGHT // 2), 50, 'assets/images/play_button.png')
MAX_TIME = 5000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Project")

clock = pygame.time.Clock()

running = True
timer = 0
position = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.is_clicked(event.pos):
                if not PLAY_BUTTON.initial:
                    pygame.mixer.music.load('assets/audio/Audio-Demo1.mp3')
                    pygame.mixer.music.play(-1, 80 + (position / 1000))
                    PLAY_BUTTON.update_icon('assets/images/pause_button.png')
                    timer = pygame.time.get_ticks()
                    if position:
                        timer -= position
                else:
                    pygame.mixer.music.pause()
                    PLAY_BUTTON.update_icon('assets/images/play_button.png')
                    position = pygame.time.get_ticks()
                    if timer:
                        position -= timer
    if timer:
        elapsed_time = (pygame.time.get_ticks() - timer)
        if elapsed_time >= MAX_TIME:
            pygame.mixer.music.stop()
            PLAY_BUTTON.update_icon('assets/images/play_button.png')
            timer = 0
            position = 0
        
    screen.fill((30, 30, 30))

    PLAY_BUTTON.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
