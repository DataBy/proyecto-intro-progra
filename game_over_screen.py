import pygame
import sys
import main_menu  # Asegúrate de que este archivo exista como main_menu.py

def mostrar_pantalla_gameover(screen):
    clock = pygame.time.Clock()

    # --- Cargar fondo ---
    fondo = pygame.image.load("assets/gameover.png").convert()

    # --- Botones ---
    menu_img = pygame.image.load("assets/menu.png").convert_alpha()
    menu_hover_img = pygame.image.load("assets/menu_hover.png").convert_alpha()
    exit_img = pygame.image.load("assets/exit.png").convert_alpha()
    exit_hover_img = pygame.image.load("assets/exit_hover.png").convert_alpha()

    # --- Offsets personalizables para mover en X ---
    menu_x_offset = 0      # Puedes cambiar esto a -100, 50, etc.
    exit_x_offset = 0

    # --- Rects con offset en X ---
    menu_rect = menu_img.get_rect(center=(screen.get_width() // 2 + menu_x_offset,
                                          screen.get_height() // 2 + 60))
    exit_rect = exit_img.get_rect(center=(screen.get_width() // 2 + exit_x_offset,
                                          screen.get_height() // 2 + 200))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.blit(fondo, (0, 0))

        # --- Botón Menú ---
        if menu_rect.collidepoint(mouse_pos):
            screen.blit(menu_hover_img, menu_rect.topleft)
            if click:
                return "menu"
        else:
            screen.blit(menu_img, menu_rect.topleft)

        # --- Botón Salir ---
        if exit_rect.collidepoint(mouse_pos):
            screen.blit(exit_hover_img, exit_rect.topleft)
            if click:
                pygame.quit()
                sys.exit()
        else:
            screen.blit(exit_img, exit_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    mostrar_pantalla_gameover(screen)
