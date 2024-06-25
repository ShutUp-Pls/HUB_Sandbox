import pygame

# Clase GameObject
class GameObject:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 300  # Velocidad en píxeles por segundo

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx, dy, dt):
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)