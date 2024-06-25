import pygame
import os

# Inicialización de Pygame
pygame.init()

# Constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 30

# Configuración de la ventana
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Animación con Sprites")

# Clase para el objeto animado
class ObjetoAnimado(pygame.sprite.Sprite):
    def __init__(self, x, y, carpeta_sprites, num_sprites):
        super().__init__()
        self.x = x
        self.y = y
        self.velocidad = 5
        self.sprites = []
        for i in range(1, num_sprites + 1):
            imagen = pygame.image.load(os.path.join(carpeta_sprites, f'sprite{i}.png')).convert_alpha()
            self.sprites.append(imagen)
        self.indice_sprite = 0
        self.image = self.sprites[self.indice_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.indice_sprite += 1
        if self.indice_sprite >= len(self.sprites):
            self.indice_sprite = 0
        self.image = self.sprites[self.indice_sprite]
        self.rect.topleft = (self.x, self.y)

    def mover(self, dx, dy):
        self.x += dx * self.velocidad
        self.y += dy * self.velocidad
        self.rect.topleft = (self.x, self.y)

# Crear el grupo de sprites
todos_sprites = pygame.sprite.Group()

# Crear el objeto animado
carpeta_sprites = 'sprites'
num_sprites = 4  # Cambia esto según el número de sprites que tengas
objeto_animado = ObjetoAnimado(100, 100, carpeta_sprites, num_sprites)
todos_sprites.add(objeto_animado)

# Bucle principal
reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    teclas = pygame.key.get_pressed()
    dx, dy = 0, 0
    if teclas[pygame.K_LEFT]:
        dx = -1
    if teclas[pygame.K_RIGHT]:
        dx = 1
    if teclas[pygame.K_UP]:
        dy = -1
    if teclas[pygame.K_DOWN]:
        dy = 1

    objeto_animado.mover(dx, dy)
    todos_sprites.update()

    ventana.fill((0, 0, 0))
    todos_sprites.draw(ventana)
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit()
