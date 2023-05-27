import pygame

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("./Imagenes/nave.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.health = 3

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_health(self, vidas):
        self.health = vidas

    def get_health(self):
        return self.health