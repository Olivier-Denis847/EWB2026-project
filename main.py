import pygame
import random
import string
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

STATE = 'title'

PLAY_BUTTON = button.Button(HIGHLIGHT_COLOR, (3*WIDTH // 4 + 50, HEIGHT // 4 + 40), 20, PLAY_ICON_PATH)
INPUT_BOX = textbox.TextBox(WIDTH // 3 + 50, HEIGHT * 2 // 3, WIDTH // 2 - 30, 50, font_main)
BACK_BUTTON_RESULTS = pygame.Rect(WIDTH // 2 - 100, HEIGHT * 2 // 3, 200, 40)
START_BUTTON = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
ROOM_CODE_BOX = textbox.TextBox(WIDTH // 2 - 100, HEIGHT * 3 // 4 - 25, 200, 40, font_main)
BACK_ARROW_MAIN = button.Button(HIGHLIGHT_COLOR, (25, 25), 20, BACK_ICON_PATH)

game_mode = 0
MODE_TEXT = font_main.render(f'Mode: {MODES[game_mode]}', True, FONT_COLOR)
MODE_BOX = pygame.Rect(WIDTH - MODE_TEXT.get_width() - 10, 10, MODE_TEXT.get_width(), MODE_TEXT.get_height())

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
room_code = ''
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
                elif BACK_ARROW_MAIN.is_clicked(event.pos):
                    song.pause()
                    PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
                    timer = 0
                    position = 0
                    PLAY_BUTTON.initial = False
                    STATE = 'title'
                    song_index = 0
            
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
                if BACK_BUTTON_RESULTS.collidepoint(event.pos):
                    STATE = 'main'
                    song_index = (song_index + 1) % len(songs)
                    song = songs[song_index]
                    song.pause()
                    position = 0
                    timer = 0
                    PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
                    PLAY_BUTTON.initial = False
        
        elif STATE == 'title':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BUTTON.collidepoint(event.pos):
                    STATE = 'main'
                    room_code = ''.join(random.choices(string.ascii_letters, k=5))
                    room_code = room_code.upper()
                elif MODE_BOX.collidepoint(event.pos):
                    game_mode = (game_mode + 1) % len(MODES)
                    MODE_TEXT = font_main.render(f'Mode: {MODES[game_mode]}', True, FONT_COLOR)
            code = ROOM_CODE_BOX.handle_event(event)
            if code is not None:
                room_code = code.upper()
                STATE = 'main'
    
    if PLAY_BUTTON.initial:
        position = (pygame.time.get_ticks() - timer) if timer else 0
        if position >= MAX_TIME:
            song.pause()
            PLAY_BUTTON.update_icon(PLAY_ICON_PATH)
            timer = 0
            position = 0
        
    screen.fill(DARK_COLOR)

    if STATE == 'main':
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

        room_text = font_small.render(f'Room Code: {room_code}', True, FONT_COLOR)
        screen.blit(room_text, (10, HEIGHT - room_text.get_height() - 10))
        
        PLAY_BUTTON.draw(screen)
        INPUT_BOX.draw(screen)
        BACK_ARROW_MAIN.draw(screen)

    elif STATE == 'results':
        answer_text = font_main.render(f'Answer: {song.answer}', True, FONT_COLOR)
        guess_text = font_main.render(f'Guess: {final_answer}', True, FONT_COLOR)
        result_text = font_main.render(f'Score: {score:.2f}', True, FONT_COLOR)
        screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, HEIGHT // 2 - answer_text.get_height() - 50))
        screen.blit(guess_text, (WIDTH // 2 - guess_text.get_width() // 2, HEIGHT // 2 - guess_text.get_height() - 20))
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, BACK_BUTTON_RESULTS, border_radius=15)
        back_text = font_main.render('Back', True, DARK_COLOR)
        screen.blit(back_text, (BACK_BUTTON_RESULTS.centerx - back_text.get_width() // 2, 
                                BACK_BUTTON_RESULTS.centery - back_text.get_height() // 2))

    elif STATE == 'title':
        title_text = font_large.render('BrainLabel', True, FONT_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3 - title_text.get_height() // 2))

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, START_BUTTON, border_radius=20)
        start_text = font_main.render('Start Game', True, DARK_COLOR)
        screen.blit(start_text, (START_BUTTON.centerx - start_text.get_width() // 2, 
                                START_BUTTON.centery - start_text.get_height() // 2))
        
        second_text = font_large.render('or', True, FONT_COLOR)
        screen.blit(second_text, (WIDTH // 2 - second_text.get_width() // 2, HEIGHT // 2 + 45))
        room_text = font_main.render('Join Room', True, FONT_COLOR)
        screen.blit(room_text, (WIDTH // 2 - room_text.get_width() // 2, HEIGHT // 2 + 85))

        ROOM_CODE_BOX.draw(screen)

        screen.blit(MODE_TEXT, (WIDTH - MODE_TEXT.get_width() - 10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
