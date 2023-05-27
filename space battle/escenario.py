import pygame
import sys

import pygame
import sys
import random

from ProyectilJugador import ProyectilJugador
from player import Player
from ProyectilEnemigo import ProyectilEnemigo
from Enemy import Enemy

from funciones import message_box

    
def escenario(nombre_usuario, screen, nivel, cantidad_enemigos, vidas, rapidez_inicial_del_proyectil_enemigo, rapidez_generacion_de_enemigos):
    # Configurar la pantalla
    pygame.display.set_caption("S P A C E  B A T T L E")
    
    fondo_1 = "./Imagenes/background1.png"
    fondo_2 = "./Imagenes/background2.jpg"
    fondo_3 = "./Imagenes/background3.jpg"
  

    if nivel==1:
        fondo_img=pygame.image.load(fondo_1)
    elif nivel==2:
        fondo_img=pygame.image.load(fondo_2)
    elif nivel==3:
        fondo_img=pygame.image.load(fondo_3)


    #Cargar imagen de fondo
    fondo_rect=fondo_img.get_rect()

    # Crear un jugador
    player_ship = Player(20, 300)
    

    # Variable para controlar el tiempo de disparo del proyectil del jugador
    tiempo_disparo = 0

    # Variable para controlar el tiempo de disparo del proyectil del enemigo
    tiempo_disparo_enemigo = 0

    # Crear una lista de proyectiles del jugador
    proyectiles_jugador = []

    # Crear una lista de enemigos
    enemigos = []

    # Crear una lista de proyectiles del enemigo
    proyectiles_enemigo = []

    
    #puntos y vidas del jugador
    puntos = 0
    player_ship.set_health(vidas)

    enemigos_restantes = cantidad_enemigos
  

    #fuente, tipo y tamaño de letra
    font = pygame.font.SysFont("Impact", 40)

    # Bucle principal del juego
    while True:
       
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Mover la nave hacia arriba
        if keys[pygame.K_UP]:
            player_ship.move_up()
        # Mover la nave hacia abajo
        if keys[pygame.K_DOWN]:
            player_ship.move_down()
        # Mover la nave hacia la izquierda
        if keys[pygame.K_LEFT]:
            player_ship.move_left()
        # Mover la nave hacia la derecha
        if keys[pygame.K_RIGHT]:
            player_ship.move_right()

        # Limitar el movimiento de la nave dentro de los límites de la pantalla
        if player_ship.rect.top < 0:
            player_ship.rect.top = 0
        if player_ship.rect.bottom > 650:
            player_ship.rect.bottom = 650
        if player_ship.rect.left < 0:
            player_ship.rect.left = 0
        if player_ship.rect.right > 1000:
            player_ship.rect.right = 1000

        
        # Disparar un proyectil hacia la derecha
        if keys[pygame.K_SPACE] and pygame.time.get_ticks() - tiempo_disparo > 500:
            proyectil = ProyectilJugador(player_ship.rect.right, player_ship.rect.centery)
            proyectiles_jugador.append(proyectil)
            tiempo_disparo = pygame.time.get_ticks()


        # Crear enemigos y disparar proyectiles de los enemigos
        if len(enemigos) < 10:
            # Agregar un enemigo cada 200 ticks
            if pygame.time.get_ticks() % rapidez_generacion_de_enemigos == 0:
                # Altura aleatoria
                altura_enemigo = random.randint(100, 550)
                enemigo = Enemy(1000, altura_enemigo)
                enemigos.append(enemigo)

        # Actualizar la pantalla
        screen.fill((0, 0, 0))
        screen.blit(fondo_img, fondo_rect)


        for enemigo in enemigos:
            # Disparar un proyectil del enemigo hacia la izquierda
            if pygame.time.get_ticks() - tiempo_disparo_enemigo > 1000:
                proyectil_enemigo = ProyectilEnemigo(enemigo.rect.left, enemigo.rect.centery)
                proyectil_enemigo.set_speed(rapidez_inicial_del_proyectil_enemigo)
                proyectiles_enemigo.append(proyectil_enemigo)
                tiempo_disparo_enemigo = pygame.time.get_ticks()
            enemigo.move_left()
            enemigo.draw(screen)

        
         # Detectar si un proyectil enemigo impacta al jugador
        for proyectil in proyectiles_enemigo:
            if proyectil.rect.colliderect(player_ship.rect):
                # Restar una vida al jugador
                player_ship.set_health(vidas-1)
                vidas = player_ship.get_health()
                # Eliminar el proyectil
                proyectiles_enemigo.remove(proyectil)


        # Actualizar la lista de proyectiles del enemigo y dibujarlos en la pantalla
        for proyectil in proyectiles_enemigo:
            proyectil.update()
            proyectil.draw(screen)

        if vidas == 0:
           
            salir = message_box("Perdió todas sus vidas \n¿Desea salir del juego?", screen)

            if salir==True:
                pygame.quit()
                sys.exit()
            elif salir==False:
                escenario(nombre_usuario, screen, nivel, cantidad_enemigos, vidas, rapidez_inicial_del_proyectil_enemigo, rapidez_generacion_de_enemigos)
            

        #Comprueba si algun enemigo atravezó el borde izquierdo
        for enemigo in enemigos:
                if enemigo.get_x_position() <= 0:
                    enemigos.remove(enemigo)
                    puntos = 0
                    enemigos_restantes -= 1
                    
                    
                    salir = message_box("Los enemigos entraron a su base \n¿Desea salir del juego?", screen)

                    if salir==True:
                        pygame.quit()
                        sys.exit()
                    elif salir==False:
                        escenario(nombre_usuario, screen, nivel, cantidad_enemigos, vidas, rapidez_inicial_del_proyectil_enemigo, rapidez_generacion_de_enemigos)
                    

        
       
       
        # Actualizar la lista de proyectiles del jugador y detectar colisiones con los enemigos
        proyectiles_a_eliminar = []  # lista temporal para almacenar los proyectiles a eliminar
        for proyectil in proyectiles_jugador:
            proyectil.update()
            proyectil.draw(screen)
            for enemigo in enemigos:                
                if proyectil.rect.colliderect(enemigo.rect):
                    enemigos.remove(enemigo)
                    if proyectil in proyectiles_jugador:  # verificar si el proyectil aún está en la lista
                        proyectiles_a_eliminar.append(proyectil)
                    puntos += 1
                    enemigos_restantes -= 1

        # Eliminar los proyectiles que están en la lista temporal
        for proyectil in proyectiles_a_eliminar:
            proyectiles_jugador.remove(proyectil)

                
        #si ningun enemigo atravieza el borde izquierdo y no quedan mas para atacar, gana      
        if enemigos_restantes == 0:
            texto_gano = font.render("Ha superado el nivel "+str(nivel), True, (0, 255, 0))
            screen.blit(texto_gano, (350, 300))
            pygame.display.update()
            pygame.time.wait(2000)

            if nivel == 3:
                texto_fin = font.render("* GANÓ EL JUEGO *", True, (40, 255, 80))
                screen.blit(texto_fin, (400, 400))
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                sys.exit()
                #return
            else:
                nivel += 1
                cantidad_enemigos *= 2
                vidas *= 2
                rapidez_inicial_del_proyectil_enemigo *= 2
                rapidez_generacion_de_enemigos /= 2
                escenario(nombre_usuario, screen, nivel, cantidad_enemigos, vidas, rapidez_inicial_del_proyectil_enemigo, rapidez_generacion_de_enemigos)
                    
            
                

        # Mostrar puntos y vidas durante el juego
        etiqueta_puntos = font.render("Puntos: " + str(puntos), True, (255, 255, 255))
        etiqueta_vidas = font.render("Vidas: " + str(vidas), True, (255, 255, 255))
        
        # Mostrar la cantidad de enemigos restantes
       
        etiqueta_enemigos_restantes = font.render("Enemigos restantes: " + str(enemigos_restantes), True, (255, 255, 255))
        screen.blit(etiqueta_enemigos_restantes, (20, 20))

        usuario = font.render("Usuario: " + str(nombre_usuario), True, (255, 255, 255))
        screen.blit(usuario, (500, 20))
        
        
        
        
        player_ship.draw(screen)
        screen.blit(etiqueta_puntos, (20, 70))
        screen.blit(etiqueta_vidas, (500, 70))
        # Actualizar la lista de proyectiles del jugador y dibujarlos en la pantalla
        for proyectil in proyectiles_jugador:
            proyectil.update()
            proyectil.draw(screen)

        
        
        pygame.display.flip()
