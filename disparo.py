import pygame
import math

class HuevoDisparo(pygame.sprite.Sprite):
    def __init__(self, x, y, objetivo=None):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("assets/bola/huevo.png").convert_alpha(), (16, 24)
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # Movimiento hacia objetivo
        if objetivo:
            dx = objetivo[0] - x
            dy = objetivo[1] - y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1
            self.vel_x = dx / dist * 8
            self.vel_y = dy / dist * 8
        else:
            self.vel_x = 0
            self.vel_y = -8

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.bottom < 0 or self.rect.top > 3000:
            self.kill()

def manejar_colisiones_huevo(disparos, indios, aves):
    for disparo in disparos:
        for indio in indios:
            if pygame.sprite.collide_mask(disparo, indio):
                if hasattr(indio, "congelar_por"):
                    indio.congelar_por(1)
                disparo.kill()
                break
        for ave in aves:
            if pygame.sprite.collide_mask(disparo, ave):
                if hasattr(ave, "congelar_por"):
                    ave.congelar_por(1)
                disparo.kill()
                break
