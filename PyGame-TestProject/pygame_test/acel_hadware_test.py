import pygame
import sys

pygame.init()

# Crear una ventana con aceleración de hardware
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWSURFACE)

pygame.display.set_caption('Uso de Aceleración de Hardware en PyGame')

clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Dibujar un rectángulo rojo en el centro de la pantalla
    pygame.draw.rect(screen, (255, 0, 0), (width // 2 - 50, height // 2 - 50, 100, 100))

    pygame.display.flip()

    # Limitar la velocidad de fotogramas
    clock.tick(60)
