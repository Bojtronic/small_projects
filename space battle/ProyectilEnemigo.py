import pygame

class ProyectilEnemigo:
    def __init__(self, x, y):
        self.image = pygame.image.load("./Imagenes/bala2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        
    def update(self):
        self.rect.x -= self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_speed(self, rapidez):
        self.speed = rapidez

    def get_speed(self):
        return self.speed
