import pygame
import math

class VidaManager:
    def __init__(self, max_vidas=3):
        self.max_vidas = max_vidas
        self.vidas = max_vidas
        self.icono = pygame.image.load("assets/bateria/bateria.png").convert_alpha()
        self.icono = pygame.transform.scale(self.icono, (40, 40))

    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1

    def ganar_vida(self):
        if self.vidas < self.max_vidas:
            self.vidas += 1

    def dibujar(self, surface):
        for i in range(self.vidas):
            x = surface.get_width() - 50 - i * 45
            y = 10
            surface.blit(self.icono, (x, y))

    def esta_muerto(self):
        return self.vidas <= 0


class VidaFlotante(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("assets/bateria/bateria.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (40, 40))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.base_scale = 1.0
        self.scale_range = 0.2
        self.scale_speed = 2.5
        self.time = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, drone_ref):
        self.time += 0.1
        scale = self.base_scale + math.sin(self.time * self.scale_speed) * self.scale_range
        new_size = int(40 * scale)
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)

        if pygame.sprite.collide_mask(self, drone_ref):
            self.kill()
            return True  # Vida recogida
        return False
