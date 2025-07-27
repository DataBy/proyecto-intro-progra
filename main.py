import pygame
from npc_indio import Indio

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

drone = pygame.Rect(400, 300, 50, 50)
indios = [Indio((100 + i * 120, 100 + i * 80), drone, id=i) for i in range(5)]
all_sprites = pygame.sprite.Group(indios)

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

    pygame.display.flip()
