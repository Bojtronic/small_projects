import pygame
import sys
from pygame.locals import *


def message_box(msg, screen):
    box_width = 600
    box_height = 200
    box_x = (screen.get_width() - box_width) / 2
    box_y = (screen.get_height() - box_height) / 2
    box_color = (255, 255, 255)
    border_width = 2
    border_color = (0, 0, 0)

    box_surface = pygame.Surface((box_width, box_height))
    box_surface.fill(box_color)
    pygame.draw.rect(box_surface, border_color, (0, 0, box_width, box_height), border_width)
    font = pygame.font.SysFont('Arial', 30)
    text_surface = font.render(msg, True, (0, 0, 0))
    text_x = (box_width - text_surface.get_width()) / 2
    text_y = (box_height - text_surface.get_height()) / 2
    box_surface.blit(text_surface, (text_x, text_y))

    yes_button = pygame.Rect(box_x + (box_width / 4) - 60, box_y + box_height - 50, 100, 40)
    no_button = pygame.Rect(box_x + (3 * box_width / 4) - 40, box_y + box_height - 50, 100, 40)

    def yes_button_action():
        return True

    def no_button_action():
        return False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button.collidepoint(mouse_pos):
                    return yes_button_action()
                elif no_button.collidepoint(mouse_pos):
                    return no_button_action()

        screen.blit(box_surface, (box_x, box_y))
        pygame.draw.rect(screen, (0, 255, 0), yes_button)
        pygame.draw.rect(screen, (255, 0, 0), no_button)

        yes_text = font.render("Si", True, (0, 0, 0))
        no_text = font.render("No", True, (0, 0, 0))

        screen.blit(yes_text, (yes_button.x + 20, yes_button.y + 10))
        screen.blit(no_text, (no_button.x + 20, no_button.y + 10))

        pygame.display.update()
