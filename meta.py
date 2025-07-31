import pygame
import math

class MetaFinal(pygame.sprite.Sprite):
    def __init__(self, x_mundo, y_mundo):
        super().__init__()
        self.image = self.generar_diana()
        self.rect = self.image.get_rect(topleft=(x_mundo, y_mundo))
        self.start_time = pygame.time.get_ticks()

    def generar_diana(self):
        size = 100
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        radios = [45, 30, 15]
        colores = [(200, 0, 0), (255, 255, 255)]

        for i, radio in enumerate(radios):
            pygame.draw.circle(surf, colores[i % 2], (center, center), radio)

        return surf

    def update(self):
        # (Opcional) animación flotante
        t = (pygame.time.get_ticks() - self.start_time) / 1000
        self.offset = math.sin(t * 2) * 4  # desplazamiento vertical animado

    def draw(self, screen, scroll_y):
        screen.blit(self.image, (self.rect.x, self.rect.y - scroll_y + self.offset))

    def check_colision(self, dron_rect):
        return self.rect.colliderect(dron_rect)
