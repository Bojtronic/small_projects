import pygame
import sys
from pygame.locals import *

from escenario import escenario


# to execute pygame
pygame.init()

# to execute the music
pygame.mixer.init()

# main screen and size
screen1 = pygame.display.set_mode((1000, 650))

# icon and name
pygame.display.set_caption("S P A C E  B A T T L E")
icon = pygame.image.load("./Imagenes/boss.png")
pygame.display.set_icon(icon)

# to start writing the name(name input)
namebox = ""

# images for backgrounds
mainscreen = ("./Imagenes/background1.png")
level1_screen = ("./Imagenes/background1.png")
level2_screen = ("./Imagenes/background2.jpg")
level3_screen = ("./Imagens/background2.jpg")
finalscreen = ("./Imagenes/background1.jpg")
instructiontext = ("./Imagenes/background1.jpg")
infoscreen = ("./Imagenes/background1.jpg")

# caracters
ship= pygame.image.load("./Imagenes/nave.png")
enemy1=pygame.image.load("./Imagenes/enemy1.png")
enemy2=pygame.image.load("./Imagenes/enemy2.png")
boss=pygame.image.load("./Imagenes/boss.png")
navedeco=pygame.image.load("./Imagenes/navedeco.png")


# first screen
def menu():
    pygame.mixer.music.load("./Imagenes/backmusic.mp3")
    pygame.mixer.music.play(-1, 0, 0)

    
    cantidad_inicial_de_enemigos = 10
    cantidad_inicial_de_vidas = 3
    rapidez_inicial_del_proyectil_enemigo = 3
    rapidez_generacion_de_enemigos = 200    

    # global for the player to write the game
    global namebox

    # loop that keeps the window active
    while True:

        # background
        background = pygame.image.load(mainscreen)
        screen1.blit(background, (0, 0))

        # font and fonts´sizes
        gamefont = pygame.font.Font("./Imagenes/spacefont.otf", 50)
        gamefont2 = pygame.font.Font("./Imagenes/spacefont.otf", 35)
        cpfont = pygame.font.Font("./Imagenes/spacefont.otf", 20)

        # caption background
        entryspace = pygame.image.load("./Imagenes/entryspace.png").convert_alpha()
        entryspace = pygame.transform.scale(entryspace, (800, 80))
        screen1.blit(entryspace, (95, 77))
        
        # displaying the name of the game
        gamename = gamefont.render("S P A C E  B A T T L E", 0, (255,255,255))
        screen1.blit(gamename, (200, 95))

        # entry space line
        entryspace = pygame.image.load("./Imagenes/entryspace.png").convert_alpha()
        entryspace = pygame.transform.scale(entryspace, (500, 5))

        # name box
        namebox1 = gamefont2.render(namebox, 0, (255, 255, 255))
        screen1.blit (namebox1, (500 - namebox1.get_width()//2, 200))

        
        # levels section
        levelsection = gamefont.render("levels", 0, (0, 140, 255))
        screen1.blit(levelsection, (160, 350))

        # about
        about = gamefont.render("about", 0, (0, 140, 255))
        screen1.blit(about, (640, 350))
        
        #imagens on menu to decorate
        screen1.blit(navedeco, (50, 180))
        screen1.blit(navedeco, (785, 180))
        screen1.blit(boss, (430, 350))

        # images of the level buttons
        buttonlevel1 = gamefont2.render("level 1", 0, (255,255,255))
        screen1.blit(buttonlevel1, (180, 400))
        buttonlevel2 = gamefont2.render("level 2", 0, (255,255,255))
        screen1.blit(buttonlevel2, (180, 450))
        buttonlevel3 = gamefont2.render("level 3", 0, (255,255,255))
        screen1.blit(buttonlevel3, (185, 500))

        ingresarNivel_1 = buttonlevel1.get_rect()
        ingresarNivel_1.x = 180
        ingresarNivel_1.y = 400
        screen1.blit(buttonlevel1, ingresarNivel_1)

        ingresarNivel_2 = buttonlevel2.get_rect()
        ingresarNivel_2.x = 180
        ingresarNivel_2.y = 450
        screen1.blit(buttonlevel2, ingresarNivel_2)

        ingresarNivel_3 = buttonlevel3.get_rect()
        ingresarNivel_3.x = 185
        ingresarNivel_3.y = 500
        screen1.blit(buttonlevel3, ingresarNivel_3)

        # checks if the player clicks the buttons
        for click in pygame.event.get():
             if click.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ingresarNivel_1.collidepoint(mouse_pos):
                    escenario(namebox, screen1, 1, cantidad_inicial_de_enemigos, cantidad_inicial_de_vidas, rapidez_inicial_del_proyectil_enemigo, rapidez_generacion_de_enemigos)
                    # El usuario ha hecho clic en el botón "level 1"
                    # ingresa al nivel 1
                elif ingresarNivel_2.collidepoint(mouse_pos):
                    escenario(namebox, screen1, 2, cantidad_inicial_de_enemigos*2, cantidad_inicial_de_vidas*2, rapidez_inicial_del_proyectil_enemigo*2, rapidez_generacion_de_enemigos/2)
                    # El usuario ha hecho clic en el botón "level 2"
                    # ingresa al nivel 2
                elif ingresarNivel_3.collidepoint(mouse_pos):
                    escenario(namebox, screen1, 3, cantidad_inicial_de_enemigos*4, cantidad_inicial_de_vidas*4, rapidez_inicial_del_proyectil_enemigo*4, rapidez_generacion_de_enemigos/4)
                    # El usuario ha hecho clic en el botón "level 3"
                    # ingresa al nivel 3
                    
             if click.type == KEYDOWN:
                if click.key == K_BACKSPACE:
                    namebox = namebox[:-1]
                else:
                    namebox += click.unicode
             if click.type == QUIT:
                 pygame.quit()
                 sys.exit()

        
        # caption background 2
        entryspace = pygame.image.load("./Imagenes/entryspace.png").convert_alpha()
        entryspace = pygame.transform.scale(entryspace, (350, 80))
        screen1.blit(entryspace, (320, 230))


        # entry name label
        entryname = gamefont.render("entry name", 0, (255,255,255))
        screen1.blit(entryname, (330, 250))



        # info button
        infobutton = gamefont2.render("information", 0, (255,255,255))
        screen1.blit(infobutton, (600, 400))

        # instructions button
        instructionsbutton = gamefont2.render("instructions", 0, (255,255,255))
        screen1.blit(instructionsbutton, (590, 450))

        # leaderboard button
        leaderboard = gamefont2.render("leaderboard", 0, (255,255,255))
        screen1.blit(leaderboard, (608, 500))

        # to make the display surface appears on the user’s monitor (changes)
        pygame.display.update()


# to start from the menu screen
menu()
  
