import pygame
import time

# ------------------------
# CONFIGURACIÓN AJUSTABLE
FRECUENCIA_DISPARO = 800  # milisegundos entre disparos (500 = cada 0.5 segundos)
# ------------------------

class VacaNPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Posición manual
        self.posicion_x = x
        self.posicion_y = y

        # Animaciones
        self.reposo_frames = [
            pygame.image.load("assets/vaca/base_mu01.png"),
            pygame.image.load("assets/vaca/base_mu02.png")
        ]
        self.ataque_frames = [
            pygame.image.load("assets/vaca/3.png"),
            pygame.image.load("assets/vaca/4.png"),
            pygame.image.load("assets/vaca/5.png")
        ]
        self.indice_animacion = 0
        self.frame_actual = self.reposo_frames[0]
        self.image = self.frame_actual
        self.rect = self.image.get_rect(topleft=(self.posicion_x, self.posicion_y))

        # Estados
        self.estado = "reposo"
        self.ultimo_cambio_frame = pygame.time.get_ticks()
        self.tiempo_entre_frames = 400  # ms entre frames de animación

        # Control de ataque
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()
        self.tiempo_espera_ataque = 5000  # cada 5 segundos ataca
        self.inicio_animacion_ataque = None
        self.esta_disparando = False
        self.tiempo_ultimo_disparo = 0

        # Disparo
        self.punto_disparo = (self.rect.centerx, self.rect.bottom - 20)  # relativo al ubre
        self.lista_disparos = pygame.sprite.Group()
        self.sprite_disparo = pygame.image.load("assets/vaca/frescoleche.png")

    def update(self):
        tiempo_actual = pygame.time.get_ticks()

        if self.estado == "reposo":
            if tiempo_actual - self.ultimo_cambio_frame > self.tiempo_entre_frames:
                self.indice_animacion = (self.indice_animacion + 1) % len(self.reposo_frames)
                self.image = self.reposo_frames[self.indice_animacion]
                self.ultimo_cambio_frame = tiempo_actual

            if tiempo_actual - self.tiempo_ultimo_ataque > self.tiempo_espera_ataque:
                self.estado = "ataque"
                self.inicio_animacion_ataque = tiempo_actual
                self.indice_animacion = 0
                self.ultimo_cambio_frame = tiempo_actual

        elif self.estado == "ataque":
            # Animar frames 3 -> 4 -> 5
            if self.indice_animacion < len(self.ataque_frames):
                if tiempo_actual - self.ultimo_cambio_frame > 200:
                    self.image = self.ataque_frames[self.indice_animacion]
                    self.indice_animacion += 1
                    self.ultimo_cambio_frame = tiempo_actual
            else:
                # Se queda en frame 5 y dispara
                self.image = self.ataque_frames[-1]

                if not self.esta_disparando:
                    self.esta_disparando = True
                    self.tiempo_ultimo_disparo = tiempo_actual

                # Usamos la variable FRECUENCIA_DISPARO
                if tiempo_actual - self.tiempo_ultimo_disparo >= FRECUENCIA_DISPARO:
                    fresco = FrescoLeche(self.punto_disparo)
                    self.lista_disparos.add(fresco)
                    self.tiempo_ultimo_disparo = tiempo_actual

                if tiempo_actual - self.inicio_animacion_ataque > 2000:
                    self.estado = "reposo"
                    self.indice_animacion = 0
                    self.esta_disparando = False
                    self.tiempo_ultimo_ataque = tiempo_actual

        # Actualizar rect y punto de disparo
        self.rect = self.image.get_rect(topleft=(self.posicion_x, self.posicion_y))
        self.punto_disparo = (self.rect.centerx, self.rect.bottom - 20)

        # Actualizar disparos
        self.lista_disparos.update()

    def draw(self, pantalla, scroll_y):
        pantalla.blit(self.image, (self.posicion_x, self.posicion_y - scroll_y))
        for disparo in self.lista_disparos:
            pantalla.blit(disparo.image, (disparo.rect.x, disparo.rect.y - scroll_y))


class FrescoLeche(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/vaca/frescoleche.png")
        self.rect = self.image.get_rect(center=pos)
        self.velocidad_x = -6  # Mueve a la izquierda (horizontal)

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.right < 0 or self.rect.left > 1280:
            self.kill()
