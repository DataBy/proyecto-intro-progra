import pygame
import sys

def mostrar_instrucciones(screen):
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Cargar imágenes
    fondo = pygame.image.load("assets/instrucciones.png").convert()
    btn_normal = pygame.image.load("assets/instrucciones/1.png").convert_alpha()
    btn_hover = pygame.image.load("assets/instrucciones/2.png").convert_alpha()

    # Sonido
    sonido_grito = pygame.mixer.Sound("assets/sonidos/grito_guanacasteco.mp3")

    # Posición del botón (esquina inferior derecha)
    btn_rect = btn_normal.get_rect(bottomright=(1280 - 20, 720 - 20))

    mostrando = True
    while mostrando:
        screen.blit(fondo, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        # Detectar hover
        if btn_rect.collidepoint(mouse_pos):
            screen.blit(btn_hover, btn_rect)
            if mouse_click:
                sonido_grito.play()
                pygame.time.delay(1000)  # Esperar que suene al menos un segundo
                mostrando = False  # Salir de la pantalla
        else:
            screen.blit(btn_normal, btn_rect)

        pygame.display.update()
        clock.tick(60)
