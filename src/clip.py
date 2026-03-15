import pygame
class Clip:
    def __init__(self, path, offset, answer):
        self.path = path
        self.offset = offset
        self.answer = answer
    
    def play(self, start=0):
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.play(-1, self.offset + start)
    
    def pause(self):
        pygame.mixer.music.pause()

    def compare_guess(self, guess):
        score = 0
        parsed_guess = guess.strip().lower().split()
        parsed_answer = self.answer.strip().lower().split()

        for i in range(min(len(parsed_guess), len(parsed_answer))):
            if parsed_answer[i] == parsed_guess[i]:
                score += 1
            elif parsed_guess[i] in parsed_answer:
                score += 0.5
        score = score - max(0, len(parsed_guess) - len(parsed_answer))
        score = max(score, 0)
        return score/len(self.answer.split())