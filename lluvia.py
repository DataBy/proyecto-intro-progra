import pygame
import time
import random

class TormentaTropical:
    def __init__(self, duracion=15, fps_anim=6):
        self.ultimo_fin = 0  # marca el tiempo cuando termina la tormenta
        self.activa = False
        self.duracion = duracion
        self.inicio_tiempo = 0

        # Cargar sprites de lluvia animada
        self.frames = [
            pygame.image.load("assets/lluvia/1.png").convert_alpha(),
            pygame.image.load("assets/lluvia/2.png").convert_alpha()
        ]
        self.alpha = 180
        for frame in self.frames:
            frame.set_alpha(self.alpha)

        self.scroll_y = 0
        self.scroll_velocidad = 2

        # Animación
        self.frame_index = 0
        self.tiempo_ultimo_cambio = time.time()
        self.intervalo_cambio = 1.0 / fps_anim

        # Relámpagos
        self.ultimo_flash = 0
        self.duracion_flash = 0.1  # segundos que dura el flash
        self.mostrando_flash = False

    def activar(self):
        self.activa = True
        self.inicio_tiempo = time.time()
        self.scroll_y = 0
        self.frame_index = 0
        self.tiempo_ultimo_cambio = time.time()
        self.ultimo_flash = 0
        self.mostrando_flash = False

    def desactivar(self):
        self.activa = False
        self.mostrando_flash = False
        self.ultimo_fin = time.time()  # guardar el momento en que terminó

    def update(self, screen, scroll_y):
        if not self.activa:
            return

        tiempo_actual = time.time()
        if tiempo_actual - self.inicio_tiempo > self.duracion:
            self.desactivar()
            return

        # Animar lluvia
        if tiempo_actual - self.tiempo_ultimo_cambio > self.intervalo_cambio:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.tiempo_ultimo_cambio = tiempo_actual

        self.scroll_y += self.scroll_velocidad
        if self.scroll_y > self.frames[0].get_height() - screen.get_height():
            self.scroll_y = 0

        frame_actual = self.frames[self.frame_index]
        screen.blit(frame_actual, (0, -self.scroll_y))

        # Flash de relámpago aleatorio
        if not self.mostrando_flash and random.random() < 0.01:  # ~1% chance por frame
            self.ultimo_flash = tiempo_actual
            self.mostrando_flash = True

        if self.mostrando_flash:
            if tiempo_actual - self.ultimo_flash < self.duracion_flash:
                flash_overlay = pygame.Surface(screen.get_size())
                flash_overlay.fill((255, 255, 255))
                flash_overlay.set_alpha(150)  # intensidad del flash
                screen.blit(flash_overlay, (0, 0))
            else:
                self.mostrando_flash = False
