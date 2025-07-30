import pygame 
import random
import time

class arbol_cayendo(pygame.sprite.Sprite):
    def __init__(self, x, y, dron_ref, duracion=20, fps_anim=6, distancia_activacion=150):
        super().__init__()
        self.activa = False
        self.duracion = duracion
        self.distancia_activacion = distancia_activacion
        self.dron_ref = dron_ref
        self.ha_golpeado = False 
        
        
        
        
        
        self.frames = [
            pygame.transform.flip(pygame.image.load("assets/arbol/1.png").convert_alpha(), True, False),
            pygame.transform.flip(pygame.image.load("assets/arbol/2.png").convert_alpha(), True, False),
            pygame.transform.flip(pygame.image.load("assets/arbol/3.png").convert_alpha(), True, False),
            pygame.transform.flip(pygame.image.load("assets/arbol/4.png").convert_alpha(), True, False)
        ]


        
        
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animacion_completa = False
        self.tiempo_ultimo_cambio = time.time()
        self.intervalo_cambio = 0.2  # segundos entre frames
    
    def chequear_activacion(self, jugador_pos):
        dx = self.rect.centerx - jugador_pos[0]
        dy = self.rect.centery - jugador_pos[1]
        
        distancia = (dx**2 + dy**2)**0.5

        if distancia < self.distancia_activacion and not self.activa:
            self.activa = True
            self.inicio_tiempo = time.time()
    
    def update(self):
        if self.activa and not self.animacion_completa:
            tiempo_actual = time.time()
            if tiempo_actual - self.tiempo_ultimo_cambio > self.intervalo_cambio:
                self.frame_index += 1
                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.frame_index]
                    self.tiempo_ultimo_cambio = tiempo_actual
                    
                    if self.rect.colliderect(self.dron_ref.rect) and not self.ha_golpeado:
                        self.dron_ref.vida_manager.perder_vida()
                        self.ha_golpeado = True
    
    def romper(self):
        self.animacion_completa = True
        self.kill()
    




            