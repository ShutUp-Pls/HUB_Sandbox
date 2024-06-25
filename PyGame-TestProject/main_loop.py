### --- IMPORTACIONES --- ###
### Librerias para el systema
import os
import sys
### Oculta mensaje de bienvenida del modulo PyGame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
### Libreria para el juego
import pygame
import obj.GameObject as GmObj
### Importación de constantes
from var.constantes_sys import *

### --- MAIN FUNCTION--- ###
def main(args):
    if args.verb_info: print(f"Proyecto: {NAME_PROJECT}\nArgumentos de ejecución: {args}")

    pygame.init()

    ### Configuración de la ventana
    pygame.display.set_caption(NAME_PROJECT)
    resolution = RSL_PANTALLA(800, 600)
    window_surf = pygame.display.set_mode(resolution.tuple)

    ### --- Crear Objetos --- ###
    ### Cuadrado Rojo
    player = GmObj.GameObject(resolution.width_mid,
                            resolution.height_mid,
                            50,
                            50,
                            CLR_RED) 

    ### Cuadrado Azul
    obstacle = GmObj.GameObject(100,
                                100,
                                50,
                                50,
                                CLR_BLUE)  # Rectángulo azul

    ### Reloj del juego
    gameclock = pygame.time.Clock()

    ### Bucle principal del juego
    while True:
        dt = gameclock.tick(60) / 1000  # Tiempo transcurrido desde el último fotograma (en segundos)

        for event in pygame.event.get():
            if args.verb_events: print(event)
            if event.type == pygame.QUIT:
                if args.verb_events: print(f"event.type == {event.type}")
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        player.move(dx, dy, dt)

        # Detección de colisión
        if player.collides_with(obstacle):
            print("¡Colisión detectada!")

        # Dibujar en la pantalla
        window_surf.fill(CLR_WHITE)
        player.draw(window_surf)
        obstacle.draw(window_surf)

        pygame.display.flip()