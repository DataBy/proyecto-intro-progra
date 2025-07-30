import pygame
import time
import threading

# Ruta del archivo de sonido
RUTA_MUSICA = "assets/sonidos/background_sound.mp3"

# 🎚️ Volumen (entre 0.0 y 1.0)
VOLUMEN_MUSICA = 0.5

# Duración total y parte a enciclar
SEGUNDOS_INICIO = 0
SEGUNDOS_BUCLE_INICIO = 20
SEGUNDOS_BUCLE_FIN = 30

def reproducir_musica():
    pygame.mixer.init()
    pygame.mixer.music.load(RUTA_MUSICA)
    pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
    pygame.mixer.music.play()
    
    def loop_segmento():
        time.sleep(SEGUNDOS_BUCLE_INICIO)
        while True:
            # Si ya no está sonando, no hacer nada
            if not pygame.mixer.music.get_busy():
                break
            # Reproducir solo el segmento 20–30s en bucle
            pygame.mixer.music.load(RUTA_MUSICA)
            pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
            pygame.mixer.music.play(start=SEGUNDOS_BUCLE_INICIO)
            time.sleep(SEGUNDOS_BUCLE_FIN - SEGUNDOS_BUCLE_INICIO)
    
    threading.Thread(target=loop_segmento, daemon=True).start()
