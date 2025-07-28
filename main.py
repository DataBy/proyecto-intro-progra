import pygame
from npc_indio import Indio
from npc_tucan import Ave

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

drone = pygame.Rect(400, 300, 50, 50)

grupo_todos = pygame.sprite.Group()
grupo_proyectiles_tucan = pygame.sprite.Group()
grupo_colisionables = pygame.sprite.Group()

indios = [Indio((100 + i * 120, 100 + i * 80), drone, id=i) for i in range(5)]

aves = [
    Ave(pygame.Rect(100 + i * 120, 100 + i * 80, 100, 100), drone, grupo_todos, grupo_proyectiles_tucan, grupo_colisionables)
    for i in range(5)
]

grupo_todos.add(indios)
grupo_todos.add(aves)

all_sprites = pygame.sprite.Group(indios, aves)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    dt = clock.tick(60) / 1000
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, (0, 255, 0), drone)

    for indio in indios:
        indio.update(dt)
        indio.draw(screen, 0)
    
    for ave in aves:
        ave.update(dt)
        ave.draw(screen, 0)
    
    grupo_proyectiles_tucan.update(drone)
    for proyectil in grupo_proyectiles_tucan:
        screen.blit(proyectil.image, proyectil.rect)
    
    

    pygame.display.flip()
