import pygame
class Button:
    def __init__(self, color, centre, radius, icon_path=None):
        self.color = color
        self.centre = centre
        self.radius = radius
        self.icon_path = icon_path
        self.initial = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.centre, self.radius)
        if self.icon_path:
            icon = pygame.image.load(self.icon_path)
            icon_rect = icon.get_rect(center=self.centre)
            screen.blit(icon, icon_rect)
    
    def is_clicked(self, pos):
        x, y = pos
        cx, cy = self.centre
        distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        if (distance <= self.radius):
            self.initial = not self.initial
            return True
        return False

    def update_icon(self, new_icon_path):
        self.icon_path = new_icon_path