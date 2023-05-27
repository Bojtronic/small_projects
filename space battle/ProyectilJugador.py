import pygame

class ProyectilJugador:
    def __init__(self, x, y):
        self.image = pygame.image.load("./Imagenes/bala.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        
    def update(self):
        self.rect.x += self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
