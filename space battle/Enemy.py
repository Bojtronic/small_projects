import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./Imagenes/nave_enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
    
    def move_left(self):
        self.rect.x -= self.speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_x_position(self):
        return self.rect.x
