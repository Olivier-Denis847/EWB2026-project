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
            big_icon = pygame.image.load(self.icon_path).convert_alpha()
            icon = pygame.transform.smoothscale(big_icon, (self.radius * 1.5, self.radius * 1.5))
            icon_rect = icon.get_rect(center=self.centre)
            screen.blit(icon, icon_rect)
    
    def is_clicked(self, pos):
        x, y = pos
        cx, cy = self.centre
        distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        return distance <= self.radius

    def update_icon(self, new_icon_path):
        self.icon_path = new_icon_path
        self.initial = not self.initial