import pygame
import sys
from src import button
from src import textbox
from src import user
from src import clip
from settings import *
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Project")

clock = pygame.time.Clock()
font_main = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 30, bold=True)
font_small = pygame.font.SysFont('Arial', 18)

STATE = 'main'

PLAY_BUTTON = button.Button(HIGHLIGHT_COLOR, (3*WIDTH // 4 + 50, HEIGHT // 4 + 40), 20, PLAY_ICON_PATH)
INPUT_BOX = textbox.TextBox(WIDTH // 3 + 50, HEIGHT * 2 // 3, WIDTH // 2 - 30, 50, font_main)
BACK_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT * 2 // 3, 200, 40)

songs = []
with open('audio_clips.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        path, offset, answer = line.strip().split(',')
        song = clip.Clip(path, float(offset), answer)
        songs.append(song)
song_index = 0
song = songs[song_index]
users = [user.User("Player 1"), user.User("Player 2")]

running = True
timer = 0
position = 0
score = 0
final_answer = ''
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if STATE == 'main':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.is_clicked(event.pos):
                    if not PLAY_BUTTON.initial:
                        song.play(position/1000)
                        PLAY_BUTTON.update_icon(PAUSE_ICON_PATH)
                        timer = pygame.time.get_ticks() - position
                    else:
                        song.pause()
                        PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
                        position = pygame.time.get_ticks() - timer
            
            guess = INPUT_BOX.handle_event(event)
            if guess is not None:
                song.pause()
                with open('guesses.txt', 'a') as f:
                    f.write(guess + '\n')
                score = song.compare_guess(guess)
                users[0].update_score(score)
                STATE = 'results'
                final_answer = guess
        elif STATE == 'results':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.collidepoint(event.pos):
                    STATE = 'main'
                    song_index = (song_index + 1) % len(songs)
                    song = songs[song_index]
                    song.pause()
                    position = 0
                    timer = 0
                    PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
                    PLAY_BUTTON.initial = False
    
    if PLAY_BUTTON.initial:
        position = (pygame.time.get_ticks() - timer) if timer else 0
        if position >= MAX_TIME:
            song.pause()
            PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
            timer = 0
            position = 0
        
    screen.fill(DARK_COLOR)

    if STATE == 'main':
        PLAY_BUTTON.draw(screen)
        INPUT_BOX.draw(screen)

        pygame.draw.rect(screen, BACKGROUND_COLOR, 
                        (0, 0, WIDTH // 3 - 25, HEIGHT))
        pygame.draw.rect(screen, FONT_COLOR, 
                         (0, 50, WIDTH // 3 - 25, 2))
        for x, player in enumerate(users):
            user_text = font_main.render(f'{player.name}', True, FONT_COLOR)
            score_text = font_small.render(f'{player.score:.2f}', True, FONT_COLOR)
            screen.blit(user_text, (10, 60 + x * 60))
            screen.blit(score_text, (10, 85 + x * 60))
            pygame.draw.rect(screen, FONT_COLOR, (0, 110 + x * 60, WIDTH // 3 - 25, 2))
        progress = min(position / MAX_TIME, 1)
        pygame.draw.rect(screen, FONT_COLOR, 
                        (WIDTH // 3 + 50, PLAY_BUTTON.centre[1] - (PLAY_BUTTON.radius // 1.5),
                        WIDTH // 3, int(1.5 * PLAY_BUTTON.radius)),
                        border_radius=15)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR,
                        (WIDTH // 3 + 50, PLAY_BUTTON.centre[1] - (PLAY_BUTTON.radius // 1.5), 
                        int((WIDTH / 3) * progress), int(1.5 * PLAY_BUTTON.radius)),
                        border_radius=15)
        
        game_text = font_large.render('What does this say?', True, FONT_COLOR)
        prompt_text = font_large.render('Input your guess:', True, FONT_COLOR)
        screen.blit(game_text, (WIDTH*5 // 8 - game_text.get_width() // 2, HEIGHT // 4 - 100))
        screen.blit(prompt_text, (WIDTH*5 // 8 - prompt_text.get_width() // 2, HEIGHT // 2))

    elif STATE == 'results':
        answer_text = font_main.render(f'Answer: {song.answer}', True, FONT_COLOR)
        guess_text = font_main.render(f'Guess: {final_answer}', True, FONT_COLOR)
        result_text = font_main.render(f'Score: {score:.2f}', True, FONT_COLOR)
        screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, HEIGHT // 2 - answer_text.get_height() - 50))
        screen.blit(guess_text, (WIDTH // 2 - guess_text.get_width() // 2, HEIGHT // 2 - guess_text.get_height() - 20))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, BACK_BUTTON, border_radius=20)
        back_text = font_main.render('Back', True, DARK_COLOR)
        screen.blit(back_text, 
                    (BACK_BUTTON.centerx - back_text.get_width() // 2, BACK_BUTTON.centery - back_text.get_height() // 2))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
