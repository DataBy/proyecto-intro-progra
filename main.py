import pygame
import sys
import main_menu
from scenary01 import jugar_escenario  # ✅ Importamos la versión buena con todo el escenario

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Héroes del Hambre")

    while True:
        accion = main_menu.mostrar_menu(screen)
        if accion == "play":
            resultado = jugar_escenario(screen)
            if resultado == "menu":
                continue  # Vuelve al menú principal
            elif resultado == "exit":
                break     # Sale del juego
        elif accion == "exit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
